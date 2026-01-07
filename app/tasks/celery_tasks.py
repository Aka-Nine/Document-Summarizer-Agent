"""
Enterprise Document Intelligence Platform - Celery Tasks
Production-ready background task processing with RAG
"""
from celery import Celery
from app.models.mongodb_database import (
    get_documents_collection, get_queries_collection,
    DocumentModel, DocumentQueryModel, ProcessingStatus
)
from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
from app.services.cloud_storage import CloudStorageService
import asyncio
import tempfile
import os
import json
import structlog
import traceback
from typing import List, Optional
from datetime import datetime

# Import settings with fallback
from app.config.settings import settings

logger = structlog.get_logger()

# Get Redis URL for Celery
def get_celery_redis_url():
    """Get Redis URL for Celery (supports Redis Cloud)"""
    # Use explicit broker URL if set
    if settings.CELERY_BROKER_URL:
        return settings.CELERY_BROKER_URL
    
    # Check if using Redis Cloud
    if getattr(settings, "REDIS_PROVIDER", "redis").lower() == "redis_cloud":
        if settings.REDIS_CLOUD_ENDPOINT and settings.REDIS_CLOUD_PASSWORD:
            # Use redis:// (not rediss://) as Redis Cloud doesn't require SSL for this setup
            # Format: redis://username:password@host:port
            username = settings.REDIS_CLOUD_USERNAME or "default"
            return (
                f"redis://{username}:{settings.REDIS_CLOUD_PASSWORD}@"
                f"{settings.REDIS_CLOUD_ENDPOINT}:{settings.REDIS_CLOUD_PORT}"
            )
    
    # Use REDIS_URL if available
    if settings.REDIS_URL:
        return settings.REDIS_URL
    
    # In production we require a real broker; in dev allow caller to fall back
    if settings.ENVIRONMENT.lower() == "production":
        raise ValueError("Redis configuration required in production. Set REDIS_URL or Redis Cloud settings")
    
    raise ValueError("Redis configuration required. Set REDIS_URL or Redis Cloud settings")

# Initialize Celery with production settings
# Avoid raising at import time when Redis isn't configured (development machines)
try:
    celery_redis_url = get_celery_redis_url()
except Exception as e:
    logger.warning("Redis not configured for Celery at import time; using in-memory broker (dev only)", error=str(e))
    celery_redis_url = "memory://"

# Use cache+memory as backend when using memory broker to avoid None backend
if celery_redis_url == "memory://":
    celery_backend = "cache+memory://"
else:
    celery_backend = celery_redis_url

celery_app = Celery(
    "enterprise_document_processor",
    broker=celery_redis_url,
    backend=celery_backend
)

# Backwards-compatible alias expected by some test and tooling code
app = celery_app

# Celery configuration
import sys

# Windows compatibility: use solo pool to avoid multiprocessing issues
# On Windows, multiprocessing with 'spawn' causes permission errors
worker_pool = 'solo' if sys.platform == 'win32' else 'prefork'

celery_app.conf.update(
    task_serializer=settings.CELERY_TASK_SERIALIZER,
    result_serializer=settings.CELERY_RESULT_SERIALIZER,
    accept_content=settings.CELERY_ACCEPT_CONTENT,
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=settings.CELERY_ENABLE_UTC,
    task_track_started=settings.CELERY_TASK_TRACK_STARTED,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    # Windows compatibility
    worker_pool=worker_pool,
    # Explicitly include tasks to ensure they're registered
    include=['app.tasks.celery_tasks'],
    # Auto-discover tasks in this module
    autodiscover_tasks=False,  # We're defining tasks explicitly
)


@celery_app.task(name="process_document_task", bind=True, max_retries=3)
def process_document_task(self, document_id: str, questions: Optional[List[str]] = None):
    """
    Process document with enterprise RAG capabilities
    
    Args:
        document_id: MongoDB document ID (string)
        questions: Optional list of questions to answer
    """
    # Initialize LangSmith tracing in Celery worker process
    # This is needed because Celery workers run in separate processes
    if settings.LANGCHAIN_TRACING_V2 and settings.LANGCHAIN_API_KEY:
        import os
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
        if settings.LANGCHAIN_ENDPOINT:
            os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
        logger.info("LangSmith tracing enabled in Celery worker", project=settings.LANGCHAIN_PROJECT)
    
    from bson import ObjectId
    temp_file_path = None
    documents_collection = None
    doc_id_obj = None
    doc = None
    
    try:
        documents_collection = get_documents_collection()
        
        # Get document
        try:
            doc_id_obj = ObjectId(document_id)
        except:
            logger.error("Invalid document ID format", document_id=document_id)
            return {"status": "error", "message": "Invalid document ID"}
        
        doc = documents_collection.find_one({"_id": doc_id_obj})
        if not doc:
            logger.error("Document not found", document_id=document_id)
            return {"status": "error", "message": "Document not found"}
        
        # Update status to processing
        documents_collection.update_one(
            {"_id": doc_id_obj},
            {"$set": {"status": ProcessingStatus.PROCESSING.value, "updated_at": datetime.utcnow()}}
        )
        
        # Download file from cloud storage
        storage = CloudStorageService.create()
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"doc_{document_id}_{os.path.basename(doc.get('file_path', 'file'))}")
        
        try:
            file_content = asyncio.run(storage.download_file(doc["file_path"]))
            with open(temp_file_path, 'wb') as f:
                f.write(file_content)
            logger.info("File downloaded from cloud storage", document_id=document_id, path=temp_file_path)
        except Exception as e:
            logger.error("Failed to download file", error=str(e), document_id=document_id)
            documents_collection.update_one(
                {"_id": doc_id_obj},
                {"$set": {
                    "status": ProcessingStatus.FAILED.value,
                    "error_message": f"Download error: {str(e)}",
                    "error_traceback": traceback.format_exc(),
                    "updated_at": datetime.utcnow()
                }}
            )
            return {"status": "error", "message": f"Download failed: {str(e)}"}
        
        # Process document with enterprise processor
        try:
            processor = EnterpriseDocumentProcessor(document_id=document_id)
            
            # Prepare metadata
            # MongoDB documents are dicts, use dictionary access
            metadata = {
                "filename": doc.get("filename", ""),
                "file_type": doc.get("file_type", ""),
                "user_id": doc.get("user_id", ""),
                "document_id": document_id
            }
            
            # Process document (async)
            result = asyncio.run(processor.process_document(
                file_path=temp_file_path,
                questions=questions,
                metadata=metadata
            ))
            
            # Update document with results
            chunks_indexed = result.get("metadata", {}).get("chunks_indexed", 0)
            processing_time = result.get("metadata", {}).get("processing_time", 0)
            
            update_data = {
                "summary": result.get("summary", ""),
                "qa_results": result.get("answers", {}),
                "processing_time": processing_time,
                "chunks_indexed": chunks_indexed,
                "vector_db_indexed": chunks_indexed > 0,
                "rag_enabled": settings.RAG_ENABLED,
                "status": ProcessingStatus.COMPLETED.value,
                "processed_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            documents_collection.update_one(
                {"_id": doc_id_obj},
                {"$set": update_data}
            )
            
            logger.info(
                "Document processing completed",
                document_id=document_id,
                processing_time=processing_time,
                chunks_indexed=chunks_indexed
            )
            
        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()
            logger.error(
                "Document processing failed",
                error=error_msg,
                document_id=document_id,
                traceback=error_trace
            )
            documents_collection.update_one(
                {"_id": doc_id_obj},
                {"$set": {
                    "status": ProcessingStatus.FAILED.value,
                    "error_message": error_msg,
                    "error_traceback": error_trace,
                    "updated_at": datetime.utcnow()
                }}
            )
        
        # Clean up temp file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.info("Temporary file deleted", path=temp_file_path)
            except Exception as e:
                logger.warning("Failed to delete temp file", error=str(e))
        
        # Get updated document for return
        updated_doc = documents_collection.find_one({"_id": doc_id_obj})
        return {
            "status": "success",
            "document_id": document_id,
            "processing_time": updated_doc.get("processing_time") if updated_doc else 0,
            "chunks_indexed": updated_doc.get("chunks_indexed", 0) if updated_doc else 0
        }
        
    except Exception as e:
        logger.exception("Unhandled exception in Celery task", error=str(e), document_id=document_id)
        # Only update document status if we have both the collection and document ID
        if documents_collection is not None and doc_id_obj is not None:
            try:
                documents_collection.update_one(
                    {"_id": doc_id_obj},
                    {"$set": {
                        "status": ProcessingStatus.FAILED.value,
                        "error_message": str(e),
                        "error_traceback": traceback.format_exc(),
                        "updated_at": datetime.utcnow()
                    }}
                )
            except Exception as update_error:
                logger.warning("Failed to update document status on error", error=str(update_error))
        raise
    
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass


@celery_app.task(name="query_document_task", bind=True)
def query_document_task(
    self,
    document_id: str,
    query: str,
    user_id: str
) -> dict:
    """
    Query a document using RAG
    
    Args:
        document_id: MongoDB document ID (string)
        query: Query string
        user_id: User ID making the query (string)
    
    Returns:
        Query results with answer and context
    """
    # Initialize LangSmith tracing in Celery worker process
    if settings.LANGCHAIN_TRACING_V2 and settings.LANGCHAIN_API_KEY:
        import os
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
        os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
        if settings.LANGCHAIN_ENDPOINT:
            os.environ["LANGCHAIN_ENDPOINT"] = settings.LANGCHAIN_ENDPOINT
    
    from bson import ObjectId
    start_time = datetime.utcnow()
    
    try:
        documents_collection = get_documents_collection()
        queries_collection = get_queries_collection()
        
        # Get document
        try:
            doc_id_obj = ObjectId(document_id)
            user_id_obj = ObjectId(user_id)
        except:
            logger.error("Invalid ID format", document_id=document_id, user_id=user_id)
            return {"status": "error", "message": "Invalid ID format"}
        
        doc = documents_collection.find_one({
            "_id": doc_id_obj,
            "user_id": user_id
        })
        
        if not doc:
            logger.error("Document not found or access denied", document_id=document_id, user_id=user_id)
            return {"status": "error", "message": "Document not found"}
        
        if doc.get("status") != ProcessingStatus.COMPLETED.value:
            return {"status": "error", "message": "Document not yet processed"}
        
        if not settings.RAG_ENABLED:
            return {"status": "error", "message": "RAG is not enabled"}
        
        # Process query
        processor = EnterpriseDocumentProcessor(document_id=document_id)
        result = asyncio.run(processor.query_document(query=query, document_id=document_id))
        
        # Calculate response time
        response_time = (datetime.utcnow() - start_time).total_seconds()
        
        # Save query to history
        query_doc = DocumentQueryModel.create(
            document_id=document_id,
            user_id=user_id,
            query=query,
            answer=result.get("answer", ""),
            context_chunks_used=len(result.get("context", [])),
            similarity_scores=[r.get("score", 0) for r in result.get("context", [])],
            retrieval_method="vector_search",
            response_time=response_time
        )
        queries_collection.insert_one(query_doc)
        
        logger.info(
            "Document query completed",
            document_id=document_id,
            query=query[:50],
            response_time=response_time
        )
        
        return {
            "status": "success",
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
            "response_time": response_time
        }
        
    except Exception as e:
        logger.error("Document query failed", error=str(e), document_id=document_id, query=query)
        return {"status": "error", "message": str(e)}
