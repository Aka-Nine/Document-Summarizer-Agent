from celery import Celery
from sqlalchemy.orm import Session
# Try relative import first, then absolute import
try:
    from ..models.database import SessionLocal, Document, ProcessingStatus
    from ..core.document_processor import DocumentProcessor
    from ..services.storage_service import StorageService
    from ..config.setting import settings
except ImportError:
    from models.database import SessionLocal, Document, ProcessingStatus
    from core.document_processor import DocumentProcessor
    from services.storage_service import StorageService
    from config.setting import settings
from typing import List
import tempfile
import os
import json
import structlog

logger = structlog.get_logger()

# Initialize Celery
celery_app = Celery(
    "document_processor",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task(name="process_document_task")
def process_document_task(document_id: int, questions: List[str] = None):
    db: Session = SessionLocal()

    try:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            logger.error("Document not found", document_id=document_id)
            return

        doc.status = ProcessingStatus.PROCESSING
        try:
            db.commit()
        except Exception as e:
            logger.error("Failed to mark document as processing", error=str(e))
            db.rollback()

        # Download file from MinIO
        storage = StorageService()
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, doc.file_path)

        try:
            storage.client.fget_object(settings.BUCKET_NAME, doc.file_path, temp_file_path)
            logger.info("Downloaded file from MinIO", temp_file_path=temp_file_path)
        except Exception as e:
            logger.error("Failed to download file from MinIO", error=str(e))
            doc.status = ProcessingStatus.FAILED
            doc.error_message = f"Download error: {str(e)}"
            try:
                db.commit()
            except:
                db.rollback()
            return

        # Run document processor
        processor = DocumentProcessor(settings.GROQ_API_KEY)
        try:
            result = processor.process_document(file_path=temp_file_path, questions=questions or [])
            logger.info("DocumentProcessor returned", result=result)

            doc.summary = result.get("summary", "")
            doc.qa_results = json.dumps(result.get("answers", {}))
            doc.processing_time = int(result["metadata"].get("processing_time", 0))
            doc.status = ProcessingStatus.COMPLETED
        except Exception as e:
            doc.status = ProcessingStatus.FAILED
            doc.error_message = str(e)
            logger.error("Document processing failed", error=str(e), document_id=document_id)

        try:
            db.commit()
        except Exception as e:
            logger.error("DB commit failed after processing", error=str(e))
            db.rollback()

        # Clean up temp file
        try:
            os.remove(temp_file_path)
            logger.info("Temporary file deleted", path=temp_file_path)
        except Exception as e:
            logger.warning("Failed to delete temp file", error=str(e))

    except Exception as e:
        logger.exception("Unhandled exception in Celery task", error=str(e))
        if 'doc' in locals() and doc:
            doc.status = ProcessingStatus.FAILED
            doc.error_message = str(e)
            try:
                db.commit()
            except:
                db.rollback()

    finally:
        db.close()
