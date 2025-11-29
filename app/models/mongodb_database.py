"""
Enterprise Document Intelligence Platform - MongoDB Database Models
Production-ready MongoDB models with RAG support
"""
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
import structlog
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.config.settings import settings
except ImportError:
    from app.config.setting import settings

logger = structlog.get_logger()


class ProcessingStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    INDEXED = "indexed"


# MongoDB Connection
class MongoDBService:
    """MongoDB connection service"""
    
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None
    
    @classmethod
    def get_client(cls) -> MongoClient:
        """Get MongoDB client (singleton)"""
        if cls._client is None:
            mongo_url = os.getenv("MONGODB_URL", getattr(settings, "MONGODB_URL", None))
            if not mongo_url:
                raise ValueError("MONGODB_URL is required")
            
            cls._client = MongoClient(
                mongo_url,
                maxPoolSize=settings.DATABASE_POOL_SIZE,
                minPoolSize=1,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            logger.info("MongoDB client initialized")
        return cls._client
    
    @classmethod
    def get_database(cls) -> Database:
        """Get database instance"""
        if cls._db is None:
            db_name = os.getenv("MONGODB_DB_NAME", getattr(settings, "MONGODB_DB_NAME", "doc_intelligence"))
            cls._db = cls.get_client()[db_name]
            logger.info("MongoDB database accessed", database=db_name)
        return cls._db
    
    @classmethod
    def close(cls):
        """Close MongoDB connection"""
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("MongoDB connection closed")


# Database instance
def get_database() -> Database:
    """Get database instance"""
    return MongoDBService.get_database()


# Collections
def get_users_collection() -> Collection:
    """Get users collection"""
    return get_database()["users"]


def get_documents_collection() -> Collection:
    """Get documents collection"""
    return get_database()["documents"]


def get_queries_collection() -> Collection:
    """Get document queries collection"""
    return get_database()["document_queries"]


def get_metrics_collection() -> Collection:
    """Get system metrics collection"""
    return get_database()["system_metrics"]


# Create indexes
def create_indexes():
    """Create MongoDB indexes for performance"""
    try:
        db = get_database()
        
        # Users indexes
        users = get_users_collection()
        users.create_index("email", unique=True)
        users.create_index("username", unique=True)
        users.create_index("created_at")
        
        # Documents indexes
        documents = get_documents_collection()
        documents.create_index("user_id")
        documents.create_index([("user_id", 1), ("status", 1)])
        documents.create_index("created_at")
        documents.create_index("file_path")
        documents.create_index([("user_id", 1), ("created_at", -1)])
        
        # Queries indexes
        queries = get_queries_collection()
        queries.create_index("document_id")
        queries.create_index("user_id")
        queries.create_index([("document_id", 1), ("created_at", -1)])
        queries.create_index("created_at")
        
        # Metrics indexes
        metrics = get_metrics_collection()
        metrics.create_index([("metric_name", 1), ("timestamp", -1)])
        metrics.create_index("timestamp")
        
        logger.info("MongoDB indexes created successfully")
    except Exception as e:
        logger.error("Failed to create MongoDB indexes", error=str(e))
        raise


# Document Models (Pydantic-like structure for validation)
class UserModel:
    """User model for MongoDB"""
    
    @staticmethod
    def create(username: str, email: str, hashed_password: str) -> Dict[str, Any]:
        """Create user document"""
        return {
            "username": username,
            "email": email,
            "hashed_password": hashed_password,
            "is_active": True,
            "is_admin": False,
            "created_at": datetime.utcnow(),
            "updated_at": None,
            "last_login": None
        }
    
    @staticmethod
    def to_dict(user_doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert user document to dict"""
        return {
            "id": str(user_doc["_id"]),
            "username": user_doc.get("username"),
            "email": user_doc.get("email"),
            "is_active": user_doc.get("is_active", True),
            "is_admin": user_doc.get("is_admin", False),
            "created_at": user_doc.get("created_at"),
            "updated_at": user_doc.get("updated_at"),
            "last_login": user_doc.get("last_login")
        }


class DocumentModel:
    """Document model for MongoDB"""
    
    @staticmethod
    def create(
        user_id: str,
        filename: str,
        file_path: str,
        file_size: int,
        file_type: Optional[str] = None,
        mime_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create document"""
        return {
            "user_id": user_id,
            "filename": filename,
            "file_path": file_path,
            "file_size": file_size,
            "file_type": file_type,
            "mime_type": mime_type,
            "status": ProcessingStatus.PENDING.value,
            "summary": None,
            "qa_results": None,
            "rag_enabled": True,
            "chunks_indexed": 0,
            "vector_db_indexed": False,
            "processing_time": None,
            "error_message": None,
            "error_traceback": None,
            "created_at": datetime.utcnow(),
            "updated_at": None,
            "processed_at": None
        }
    
    @staticmethod
    def to_dict(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert document to dict"""
        return {
            "id": str(doc["_id"]),
            "user_id": str(doc.get("user_id", "")),
            "filename": doc.get("filename"),
            "file_path": doc.get("file_path"),
            "file_size": doc.get("file_size"),
            "file_type": doc.get("file_type"),
            "mime_type": doc.get("mime_type"),
            "status": doc.get("status"),
            "summary": doc.get("summary"),
            "qa_results": doc.get("qa_results"),
            "rag_enabled": doc.get("rag_enabled", True),
            "chunks_indexed": doc.get("chunks_indexed", 0),
            "vector_db_indexed": doc.get("vector_db_indexed", False),
            "processing_time": doc.get("processing_time"),
            "error_message": doc.get("error_message"),
            "error_traceback": doc.get("error_traceback"),
            "created_at": doc.get("created_at"),
            "updated_at": doc.get("updated_at"),
            "processed_at": doc.get("processed_at")
        }


class DocumentQueryModel:
    """Document query model for MongoDB"""
    
    @staticmethod
    def create(
        document_id: str,
        user_id: str,
        query: str,
        answer: Optional[str] = None,
        context_chunks_used: int = 0,
        similarity_scores: Optional[List[float]] = None,
        retrieval_method: str = "vector_search",
        response_time: Optional[float] = None,
        tokens_used: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create query document"""
        return {
            "document_id": document_id,
            "user_id": user_id,
            "query": query,
            "answer": answer,
            "context_chunks_used": context_chunks_used,
            "similarity_scores": similarity_scores or [],
            "retrieval_method": retrieval_method,
            "response_time": response_time,
            "tokens_used": tokens_used,
            "created_at": datetime.utcnow()
        }
    
    @staticmethod
    def to_dict(query_doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert query document to dict"""
        return {
            "id": str(query_doc["_id"]),
            "document_id": str(query_doc.get("document_id", "")),
            "user_id": str(query_doc.get("user_id", "")),
            "query": query_doc.get("query"),
            "answer": query_doc.get("answer"),
            "context_chunks_used": query_doc.get("context_chunks_used", 0),
            "similarity_scores": query_doc.get("similarity_scores", []),
            "retrieval_method": query_doc.get("retrieval_method", "vector_search"),
            "response_time": query_doc.get("response_time"),
            "tokens_used": query_doc.get("tokens_used"),
            "created_at": query_doc.get("created_at")
        }

