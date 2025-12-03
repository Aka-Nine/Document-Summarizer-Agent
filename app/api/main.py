"""
Enterprise Document Intelligence Platform - Main API
Production-ready FastAPI application with RAG support
"""
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from typing import Optional
import structlog
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import traceback
import uuid

# Import settings with fallback
try:
    from app.config.settings import settings
except ImportError:
    from app.config.settings import settings

from app.models.mongodb_database import get_database, get_users_collection, create_indexes
from app.services.redis_service import RedisService
from app.middleware.production import setup_production_middleware

logger = structlog.get_logger()

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Document Intelligence Platform with RAG (Retrieval Augmented Generation)",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Setup production middleware
setup_production_middleware(app)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include versioned routes (MongoDB version)
try:
    from app.api.v1.routes_mongodb import router as v1_mongodb_router
    app.include_router(v1_mongodb_router)
    logger.info("MongoDB API routes loaded")
except ImportError as e:
    logger.warning("MongoDB routes not available", error=str(e))
    # Try SQL version as fallback
    try:
        from app.api.v1.routes_mongodb import router as v1_router
        app.include_router(v1_router)
        logger.info("SQL API routes loaded as fallback")
    except ImportError:
        logger.error("No API routes available")

# Serve frontend static files (if frontend directory exists)
try:
    frontend_path = Path(__file__).parent.parent.parent / "frontend"
    if frontend_path.exists() and frontend_path.is_dir():
        app.mount("/frontend", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
        logger.info("Frontend static files mounted at /frontend")
except Exception as e:
    logger.warning("Frontend static files not available", error=str(e))

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    try:
        # Initialize non-blocking DB setup: run ping and index creation in a background thread
        import asyncio
        import os

        # If no MONGODB_URL is provided, skip DB initialization to allow the app to start in minimal mode
        mongo_url = os.getenv("MONGODB_URL", getattr(settings, "MONGODB_URL", None))
        if not mongo_url:
            logger.warning("MONGODB_URL not set - skipping database initialization (app will run in degraded mode)")
            return

        async def _init_db():
            try:
                loop = asyncio.get_running_loop()
                # run blocking DB calls in threadpool to avoid blocking event loop
                await loop.run_in_executor(None, lambda: get_database().command("ping"))
                await loop.run_in_executor(None, create_indexes)
                logger.info("Background DB initialization completed")
            except Exception as e:
                logger.error("Background DB initialization failed", error=str(e))

        asyncio.create_task(_init_db())
        logger.info("Application startup initiated", version=settings.APP_VERSION, environment=settings.ENVIRONMENT)
    except Exception as e:
        logger.error("Startup failed", error=str(e))


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        "Unhandled exception",
        error=str(exc),
        traceback=traceback.format_exc(),
        path=request.url.path,
        method=request.method,
        request_id=request_id
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Helper functions (exported for v1 routes)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
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


# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "dependencies": {
            "database": False,
            "redis": False,
            "storage": False,
            "vector_db": False
        }
    }
    
    # Check database
    try:
        db = get_database()
        db.command("ping")
        health["dependencies"]["database"] = True
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
    
    # Check Redis
    try:
        redis = RedisService()
        redis.set_key("health_check", "ok", expire_seconds=10)
        health["dependencies"]["redis"] = True
    except Exception as e:
        logger.error("Redis health check failed", error=str(e))
    
    # Check storage
    try:
        from app.services.cloud_storage import CloudStorageService
        storage = CloudStorageService.create()
        health["dependencies"]["storage"] = True
    except Exception as e:
        logger.error("Storage health check failed", error=str(e))
    
    # Check vector DB (if RAG enabled). Use a safe factory that falls back to an in-memory store
    if settings.RAG_ENABLED:
        try:
            from app.services.vector_db_service import create_vector_db_service_safe
            vector_db = create_vector_db_service_safe()
            await vector_db.get_stats()
            health["dependencies"]["vector_db"] = True
        except Exception as e:
            # If vector DB fails, mark it as unavailable but don't necessarily fail the whole service
            logger.error("Vector DB health check failed (vector DB will be considered degraded)", error=str(e))
    
    # Determine overall status
    # Treat database, redis and storage as core dependencies; vector_db is optional and will mark the service as 'degraded' but not necessarily return 503
    core_deps = ["database", "redis", "storage"]
    core_healthy = all(health["dependencies"].get(d, False) for d in core_deps)

    if not core_healthy:
        health["status"] = "degraded"
        status_code = 503
    else:
        # Core deps are healthy. If only vector_db is false, return 200 but indicate degraded status.
        if settings.RAG_ENABLED and not health["dependencies"].get("vector_db", False):
            health["status"] = "degraded"
            status_code = 200
        else:
            health["status"] = "healthy"
            status_code = 200

    return JSONResponse(content=health, status_code=status_code)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "api": settings.API_V1_PREFIX
    }


# File serving endpoint for filesystem storage
@app.get("/files/{file_path:path}")
async def serve_file(file_path: str):
    """Serve files from filesystem storage"""
    try:
        from pathlib import Path
        
        storage_path = Path(settings.FILESYSTEM_STORAGE_PATH)
        file_path_obj = storage_path / file_path
        
        # Security: Ensure file is within storage directory
        try:
            file_path_obj.resolve().relative_to(storage_path.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="Access denied")
        
        if not file_path_obj.exists() or not file_path_obj.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            path=str(file_path_obj),
            filename=file_path_obj.name
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to serve file", error=str(e), file_path=file_path)
        raise HTTPException(status_code=500, detail="Failed to serve file")

# Test endpoint
@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {
        "message": "Enterprise Document Intelligence Platform is running",
        "timestamp": datetime.utcnow().isoformat(),
        "rag_enabled": settings.RAG_ENABLED,
        "llm_provider": settings.LLM_PROVIDER,
        "cloud_provider": settings.CLOUD_PROVIDER.value if hasattr(settings.CLOUD_PROVIDER, 'value') else str(settings.CLOUD_PROVIDER)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
