"""
Enterprise Document Intelligence Platform - API v1 Routes
Production-ready API endpoints with RAG support
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import structlog
import filetype
from pathlib import Path
import uuid
from datetime import datetime

# Import with fallback for compatibility
try:
    from app.config.settings import settings
except ImportError:
    from app.config.setting import settings

from app.models.database import SessionLocal, User, Document, ProcessingStatus, DocumentQuery
from app.services.cloud_storage import CloudStorageService
from app.services.redis_service import RedisService
from app.tasks.celery_tasks import process_document_task, query_document_task
# Import helper functions (defined in api/main.py but used here)
from app.models.database import SessionLocal, User
from app.config.settings import settings
from datetime import timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

# Security setup
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper functions
def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta=None):
    """Create JWT access token"""
    from datetime import datetime
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
from tenacity import retry, stop_after_attempt, wait_exponential

logger = structlog.get_logger()

router = APIRouter(prefix=settings.API_V1_PREFIX, tags=["v1"])


# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class DocumentQueryRequest(BaseModel):
    query: str
    document_id: int
    top_k: Optional[int] = None


class DocumentQueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    response_time: float


# Authentication endpoints
@router.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
            raise HTTPException(status_code=400, detail="Username or email already registered")
        
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info("User registered", user_id=db_user.id, username=user.username)
        return {"message": "User registered successfully", "user_id": db_user.id}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error("Registration failed", error=str(e))
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """Login and get JWT token"""
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not db_user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        token = create_access_token(
            data={"sub": db_user.username},
            expires_delta=None  # Uses default from settings
        )
        
        db_user.last_login = datetime.utcnow()
        db.commit()
        
        logger.info("User logged in", user_id=db_user.id, username=user.username)
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(status_code=500, detail="Login failed")


# Document endpoints
@router.post("/documents/upload")
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    questions: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    try:
        # Validate file size
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File too large. Max size: {settings.MAX_FILE_SIZE} bytes")
        
        # Validate file type
        kind = filetype.guess(file_content)
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File extension not supported. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        if kind and kind.mime not in settings.ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"MIME type not supported. Detected: {kind.mime}"
            )
        
        # Upload to cloud storage
        storage = CloudStorageService.create()
        file_id = str(uuid.uuid4())
        object_key = f"{current_user.id}/{file_id}{file_extension}"
        
        try:
            await storage.upload_file(
                file_content=file_content,
                object_key=object_key,
                content_type=kind.mime if kind else "application/octet-stream"
            )
            logger.info("File uploaded to cloud storage", object_key=object_key, user_id=current_user.id)
        except Exception as e:
            logger.error("Cloud storage upload failed", error=str(e))
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
        # Create database record
        db_document = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_path=object_key,
            file_size=file_size,
            file_type=file_extension[1:] if file_extension.startswith('.') else file_extension,
            mime_type=kind.mime if kind else None,
            status=ProcessingStatus.PENDING,
            rag_enabled=settings.RAG_ENABLED
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        
        # Parse questions
        question_list = []
        if questions:
            question_list = [q.strip() for q in questions.split('\n') if q.strip()]
        
        # Queue processing task
        process_document_task.delay(db_document.id, question_list)
        
        logger.info(
            "Document uploaded and queued",
            document_id=db_document.id,
            filename=file.filename,
            user_id=current_user.id
        )
        
        return {
            "document_id": db_document.id,
            "status": "uploaded",
            "message": "Document uploaded successfully and queued for processing",
            "rag_enabled": settings.RAG_ENABLED
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Upload failed", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/documents")
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List user's documents"""
    try:
        documents = db.query(Document).filter(
            Document.user_id == current_user.id
        ).order_by(Document.created_at.desc()).offset(skip).limit(limit).all()
        
        return [
            {
                "id": doc.id,
                "filename": doc.filename,
                "status": doc.status.value,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "rag_enabled": doc.rag_enabled,
                "chunks_indexed": doc.chunks_indexed,
                "created_at": doc.created_at.isoformat() if doc.created_at else None,
                "processed_at": doc.processed_at.isoformat() if doc.processed_at else None,
                "processing_time": doc.processing_time
            }
            for doc in documents
        ]
    except Exception as e:
        logger.error("Failed to list documents", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.get("/documents/{document_id}")
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get document details and processing results"""
    try:
        doc = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        ).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Parse Q&A results
        qa_results = {}
        if doc.qa_results:
            if isinstance(doc.qa_results, str):
                import json
                try:
                    qa_results = json.loads(doc.qa_results)
                except:
                    qa_results = {}
            else:
                qa_results = doc.qa_results
        
        return {
            "id": doc.id,
            "filename": doc.filename,
            "status": doc.status.value,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "summary": doc.summary,
            "qa_results": qa_results,
            "rag_enabled": doc.rag_enabled,
            "chunks_indexed": doc.chunks_indexed,
            "vector_db_indexed": doc.vector_db_indexed,
            "processing_time": doc.processing_time,
            "error_message": doc.error_message,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
            "processed_at": doc.processed_at.isoformat() if doc.processed_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get document", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to get document")


@router.post("/documents/{document_id}/query")
async def query_document(
    document_id: int,
    query_request: DocumentQueryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Query a document using RAG"""
    try:
        # Verify document access
        doc = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        ).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if doc.status != ProcessingStatus.COMPLETED:
            raise HTTPException(status_code=400, detail="Document not yet processed")
        
        if not settings.RAG_ENABLED:
            raise HTTPException(status_code=400, detail="RAG is not enabled")
        
        if not doc.vector_db_indexed:
            raise HTTPException(status_code=400, detail="Document not indexed in vector database")
        
        # Queue query task
        task = query_document_task.delay(
            document_id=document_id,
            query=query_request.query,
            user_id=current_user.id
        )
        
        # Wait for result (with timeout)
        try:
            result = task.get(timeout=30)
            if result.get("status") == "error":
                raise HTTPException(status_code=500, detail=result.get("message", "Query failed"))
            return result
        except Exception as e:
            logger.error("Query task failed", error=str(e), document_id=document_id)
            raise HTTPException(status_code=500, detail="Query processing failed")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Document query failed", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get("/documents/{document_id}/queries")
async def get_document_queries(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50
):
    """Get query history for a document"""
    try:
        # Verify document access
        doc = db.query(Document).filter(
            Document.id == document_id,
            Document.user_id == current_user.id
        ).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        queries = db.query(DocumentQuery).filter(
            DocumentQuery.document_id == document_id,
            DocumentQuery.user_id == current_user.id
        ).order_by(DocumentQuery.created_at.desc()).offset(skip).limit(limit).all()
        
        return [
            {
                "id": q.id,
                "query": q.query,
                "answer": q.answer,
                "response_time": q.response_time,
                "context_chunks_used": q.context_chunks_used,
                "created_at": q.created_at.isoformat() if q.created_at else None
            }
            for q in queries
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get queries", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to get queries")

