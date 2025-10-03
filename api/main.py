from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pathlib import Path
import traceback
import uuid
from pydantic import BaseModel, EmailStr
from tenacity import retry, stop_after_attempt, wait_exponential
import filetype  # windows-compatible filetype lib
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import json
# Try relative import first, then absolute import
try:
    from ..config.setting import settings
    from ..models.database import SessionLocal, User, Document, ProcessingStatus, create_tables
    from ..services.storage_service import StorageService
    from ..services.aws_cache_service import get_aws_cache_service
    from ..services.aws_task_service import aws_task_service
except ImportError:
    from config.setting import settings
    from models.database import SessionLocal, User, Document, ProcessingStatus, create_tables
    from services.storage_service import StorageService
    from services.aws_cache_service import get_aws_cache_service
    from services.aws_task_service import aws_task_service

logger = structlog.get_logger()

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Document Processing API",
    description="Scalable document processing with LLM-powered summarization and Q&A",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def startup_event():
    create_tables()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception",
                 error=str(exc),
                 traceback=traceback.format_exc(),
                 path=request.url.path,
                 method=request.method)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=3600,
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def save_file_with_retry(storage: StorageService, file_content: bytes, filename: str) -> str:
    return await storage.save_file(file_content, filename)

@app.post("/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
            raise HTTPException(status_code=400, detail="Username or email already registered")
        db_user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Registration failed", error=str(e))
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(status_code=500, detail="Login failed")

@app.post("/upload")
@limiter.limit("2/minute")
async def upload_document(
    request: Request,
    file: UploadFile = File(...),
    questions: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        file_content = await file.read()
        kind = filetype.guess(file_content)
        if not kind or kind.mime != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="File extension not supported")

        storage = StorageService()
        file_path = await save_file_with_retry(storage, file_content, file.filename)
        db_document = Document(
            user_id=current_user.id,
            filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            status=ProcessingStatus.PENDING
        )
        db.add(db_document)
        db.commit()
        db.refresh(db_document)

        question_list = [q.strip() for q in questions.split('\n') if q.strip()] if questions else []
        
        # Send task to AWS SQS
        task_id = aws_task_service.send_task(
            task_name="process_document_task",
            task_args=[db_document.id, question_list]
        )

        return {
            "document_id": db_document.id,
            "status": "uploaded",
            "message": "Document uploaded successfully and queued for processing"
        }
    except Exception as e:
        logger.error("Upload failed", error=str(e))
        raise HTTPException(status_code=500, detail="Upload failed")

@app.get("/documents")
async def list_documents(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        documents = db.query(Document).filter(Document.user_id == current_user.id).all()
        return [ 
            {
                "id": doc.id,
                "filename": doc.filename,
                "status": doc.status.value,
                "created_at": doc.created_at,
                "processing_time": doc.processing_time
            } for doc in documents
        ]
    except Exception as e:
        logger.error("Failed to list documents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to list documents")


@app.get("/documents/{document_id}")
async def get_document(document_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        doc = db.query(Document).filter(Document.id == document_id, Document.user_id == current_user.id).first()
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")

        # Fix: Ensure qa_results is parsed correctly
        if isinstance(doc.qa_results, str):
            try:
                qa_results = json.loads(doc.qa_results)
            except json.JSONDecodeError:
                qa_results = {}
        else:
            qa_results = doc.qa_results or {}

        return {
            "id": doc.id,
            "filename": doc.filename,
            "status": doc.status.value,
            "summary": doc.summary,
            "qa_results": qa_results,
            "processing_time": doc.processing_time,
            "error_message": doc.error_message,
            "created_at": doc.created_at,
            "updated_at": doc.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get document", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get document")


@app.get("/health")
async def health_check():
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "dependencies": {
            "database": False,
            "cache": False,
            "s3": False
        }
    }
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        health["dependencies"]["database"] = True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
    try:
        cache = get_aws_cache_service()
        if cache:
            cache.set_key("health_check", "ok", expire_seconds=10)
        health["dependencies"]["cache"] = True
    except Exception as e:
        logger.error("Cache health check failed", error=str(e))
    try:
        storage = StorageService()
        # Check S3 bucket access
        storage.client.head_bucket(Bucket=settings.S3_BUCKET_NAME)
        health["dependencies"]["s3"] = True
    except Exception as e:
        logger.error("S3 health check failed", error=str(e))
    health["status"] = "healthy" if all(health["dependencies"].values()) else "degraded"
    return health

@app.post("/test")
async def test_endpoint():
    return {"message": "Test endpoint working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
