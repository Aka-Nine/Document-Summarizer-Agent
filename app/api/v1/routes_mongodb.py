"""
Enterprise Document Intelligence Platform - API v1 Routes (MongoDB)
Production-ready API endpoints with MongoDB and RAG support
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel, EmailStr
import structlog
import filetype
from pathlib import Path
import uuid
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
from bson.errors import InvalidId

from app.config.settings import settings
from app.core.rate_limit import limiter

from app.models.mongodb_database import (
    get_users_collection, get_documents_collection, get_queries_collection,
    UserModel, DocumentModel, DocumentQueryModel, ProcessingStatus, create_indexes
)
from app.services.cloud_storage import CloudStorageService
from app.services.redis_service import RedisService
from app.tasks.celery_tasks import process_document_task, query_document_task

logger = structlog.get_logger()

# Use an `/auth` sub-prefix for authentication endpoints so tests and clients
# calling `/api/v1/auth/*` will match. Other document/search routes remain
# under the main API v1 prefix.
router = APIRouter(prefix=f"{settings.API_V1_PREFIX}/auth", tags=["v1"])

# Security setup
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta=None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Get current authenticated user"""
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        users_collection = get_users_collection()
        user = users_collection.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        
        if not user.get("is_active", True):
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


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
    document_id: str
    top_k: Optional[int] = None


# Authentication endpoints
@router.post("/register")
@limiter.limit(lambda: f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def register(request: Request, user: UserCreate):
    """Register a new user"""
    try:
        users_collection = get_users_collection()
        
        # Check if user exists
        if users_collection.find_one({"$or": [{"username": user.username}, {"email": user.email}]}):
            raise HTTPException(status_code=400, detail="Username or email already registered")
        
        # Create user
        user_doc = UserModel.create(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        result = users_collection.insert_one(user_doc)
        
        logger.info("User registered", user_id=str(result.inserted_id), username=user.username)
        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login")
@limiter.limit(lambda: f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def login(request: Request, user: UserLogin):
    """Login and get JWT token"""
    try:
        users_collection = get_users_collection()
        db_user = users_collection.find_one({"username": user.username})
        
        if not db_user or not verify_password(user.password, db_user.get("hashed_password", "")):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        if not db_user.get("is_active", True):
            raise HTTPException(status_code=403, detail="User account is inactive")
        
        token = create_access_token(data={"sub": db_user["username"]})
        
        # Update last login
        users_collection.update_one(
            {"_id": db_user["_id"]},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        
        logger.info("User logged in", user_id=str(db_user["_id"]), username=user.username)
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(status_code=500, detail="Login failed")


# Document endpoints
@router.post("/documents/upload")
@limiter.limit(lambda: f"{settings.RATE_LIMIT_UPLOAD_PER_MINUTE}/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    questions: Optional[str] = Form(None),
    current_user: dict = Depends(get_current_user)
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
        object_key = f"{str(current_user['_id'])}/{file_id}{file_extension}"
        
        try:
            await storage.upload_file(
                file_content=file_content,
                object_key=object_key,
                content_type=kind.mime if kind else "application/octet-stream"
            )
            logger.info("File uploaded to cloud storage", object_key=object_key, user_id=str(current_user["_id"]))
        except Exception as e:
            logger.error("Cloud storage upload failed", error=str(e))
            raise HTTPException(status_code=500, detail="Failed to upload file to storage")
        
        # Create database record
        user_id = str(current_user["_id"])
        document_doc = DocumentModel.create(
            user_id=user_id,
            filename=file.filename,
            file_path=object_key,
            file_size=file_size,
            file_type=file_extension[1:] if file_extension.startswith('.') else file_extension,
            mime_type=kind.mime if kind else None
        )
        
        documents_collection = get_documents_collection()
        result = documents_collection.insert_one(document_doc)
        document_id = str(result.inserted_id)
        
        # Parse questions
        question_list = []
        if questions:
            question_list = [q.strip() for q in questions.split('\n') if q.strip()]
        
        # Queue processing task
        process_document_task.delay(document_id, question_list)
        
        logger.info(
            "Document uploaded and queued",
            document_id=document_id,
            filename=file.filename,
            user_id=user_id
        )
        
        return {
            "document_id": document_id,
            "status": "uploaded",
            "message": "Document uploaded successfully and queued for processing",
            "rag_enabled": settings.RAG_ENABLED
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Upload failed", error=str(e), user_id=str(current_user.get("_id", "")))
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/documents")
@limiter.limit(lambda: f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def list_documents(
    request: Request,
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """List user's documents"""
    try:
        documents_collection = get_documents_collection()
        user_id = str(current_user["_id"])
        
        documents = documents_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).skip(skip).limit(limit)
        
        return [
            {
                "id": str(doc["_id"]),
                "filename": doc.get("filename"),
                "status": doc.get("status"),
                "file_type": doc.get("file_type"),
                "file_size": doc.get("file_size"),
                "summary": doc.get("summary"),  # Added for frontend display
                "rag_enabled": doc.get("rag_enabled", True),
                "chunks_indexed": doc.get("chunks_indexed", 0),
                "vector_db_indexed": doc.get("vector_db_indexed", False),  # Added for frontend filtering
                "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
                "processed_at": doc.get("processed_at").isoformat() if doc.get("processed_at") else None,
                "processing_time": doc.get("processing_time"),
                "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None
            }
            for doc in documents
        ]
    except Exception as e:
        logger.error("Failed to list documents", error=str(e), user_id=str(current_user.get("_id", "")))
        raise HTTPException(status_code=500, detail="Failed to list documents")


@router.get("/documents/{document_id}")
@limiter.limit(lambda: f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def get_document(
    request: Request,
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get document details and processing results"""
    try:
        documents_collection = get_documents_collection()
        user_id = str(current_user["_id"])
        
        try:
            doc_id_obj = ObjectId(document_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid document ID format")
        
        doc = documents_collection.find_one({
            "_id": doc_id_obj,
            "user_id": user_id
        })
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {
            "id": str(doc["_id"]),
            "filename": doc.get("filename"),
            "status": doc.get("status"),
            "file_type": doc.get("file_type"),
            "file_size": doc.get("file_size"),
            "summary": doc.get("summary"),
            "qa_results": doc.get("qa_results"),
            "rag_enabled": doc.get("rag_enabled", True),
            "chunks_indexed": doc.get("chunks_indexed", 0),
            "vector_db_indexed": doc.get("vector_db_indexed", False),
            "processing_time": doc.get("processing_time"),
            "error_message": doc.get("error_message"),
            "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
            "updated_at": doc.get("updated_at").isoformat() if doc.get("updated_at") else None,
            "processed_at": doc.get("processed_at").isoformat() if doc.get("processed_at") else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get document", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to get document")


@router.post("/documents/{document_id}/query")
@limiter.limit(lambda : f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def query_document(
    request: Request,
    document_id: str,
    query_request: DocumentQueryRequest,
    current_user: dict = Depends(get_current_user)
):
    """Query a document using RAG"""
    try:
        documents_collection = get_documents_collection()
        user_id = str(current_user["_id"])
        
        try:
            doc_id_obj = ObjectId(document_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid document ID format")
        
        # Verify document access
        doc = documents_collection.find_one({
            "_id": doc_id_obj,
            "user_id": user_id
        })
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        if doc.get("status") != ProcessingStatus.COMPLETED.value:
            raise HTTPException(status_code=400, detail="Document not yet processed")
        
        if not settings.RAG_ENABLED:
            raise HTTPException(status_code=400, detail="RAG is not enabled")
        
        if not doc.get("vector_db_indexed", False):
            raise HTTPException(status_code=400, detail="Document not indexed in vector database")
        
        # Queue query task
        task = query_document_task.delay(
            document_id=document_id,
            query=query_request.query,
            user_id=user_id
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
    document_id: str,
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """Get query history for a document"""
    try:
        documents_collection = get_documents_collection()
        queries_collection = get_queries_collection()
        user_id = str(current_user["_id"])
        
        try:
            doc_id_obj = ObjectId(document_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid document ID format")
        
        # Verify document access
        doc = documents_collection.find_one({
            "_id": doc_id_obj,
            "user_id": user_id
        })
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        queries = queries_collection.find({
            "document_id": document_id,
            "user_id": user_id
        }).sort("created_at", -1).skip(skip).limit(limit)
        
        return [
            {
                "id": str(q["_id"]),
                "query": q.get("query"),
                "answer": q.get("answer"),
                "response_time": q.get("response_time"),
                "context_chunks_used": q.get("context_chunks_used", 0),
                "created_at": q.get("created_at").isoformat() if q.get("created_at") else None
            }
            for q in queries
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get queries", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to get queries")

