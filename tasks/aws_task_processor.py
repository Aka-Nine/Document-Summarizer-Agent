"""
AWS-based task processor for document processing
Replaces Celery with AWS SQS + Lambda/ECS
"""
import json
import os
import tempfile
import traceback
from typing import Dict, Any, List
from sqlalchemy.orm import Session
# Try relative import first, then absolute import
try:
    from ..models.database import SessionLocal, Document, ProcessingStatus
    from ..core.document_processor import DocumentProcessor
    from ..services.storage_service import StorageService
    from ..services.aws_cache_service import aws_cache_service
    from ..config.setting import settings
except ImportError:
    from models.database import SessionLocal, Document, ProcessingStatus
    from core.document_processor import DocumentProcessor
    from services.storage_service import StorageService
    from services.aws_cache_service import aws_cache_service
    from config.setting import settings
import structlog

logger = structlog.get_logger()

class AWSTaskProcessor:
    """Process tasks from AWS SQS queue"""
    
    def __init__(self):
        self.storage = StorageService()
        self.processor = DocumentProcessor(settings.GROQ_API_KEY)
    
    def process_document_task(self, document_id: int, questions: List[str] = None) -> Dict[str, Any]:
        """
        Process a document task
        :param document_id: ID of the document to process
        :param questions: List of custom questions
        :return: Processing result
        """
        db: Session = SessionLocal()
        
        try:
            # Get document from database
            doc = db.query(Document).filter(Document.id == document_id).first()
            if not doc:
                logger.error("Document not found", document_id=document_id)
                return {"status": "error", "message": "Document not found"}
            
            # Update status to processing
            doc.status = ProcessingStatus.PROCESSING
            try:
                db.commit()
            except Exception as e:
                logger.error("Failed to mark document as processing", error=str(e))
                db.rollback()
                return {"status": "error", "message": "Database error"}
            
            # Download file from S3
            temp_dir = tempfile.gettempdir()
            temp_file_path = os.path.join(temp_dir, doc.file_path)
            
            try:
                success = self.storage.download_file(doc.file_path, temp_file_path)
                if not success:
                    raise Exception("Failed to download file from S3")
                logger.info("Downloaded file from S3", temp_file_path=temp_file_path)
            except Exception as e:
                logger.error("Failed to download file from S3", error=str(e))
                doc.status = ProcessingStatus.FAILED
                doc.error_message = f"Download error: {str(e)}"
                try:
                    db.commit()
                except:
                    db.rollback()
                return {"status": "error", "message": "File download failed"}
            
            # Process document with AI
            try:
                result = self.processor.process_document(
                    file_path=temp_file_path, 
                    questions=questions or []
                )
                logger.info("Document processing completed", result=result)
                
                # Update document with results
                doc.summary = result.get("summary", "")
                doc.qa_results = json.dumps(result.get("answers", {}))
                doc.processing_time = int(result["metadata"].get("processing_time", 0))
                doc.status = ProcessingStatus.COMPLETED
                
            except Exception as e:
                logger.error("Document processing failed", error=str(e))
                doc.status = ProcessingStatus.FAILED
                doc.error_message = str(e)
            
            # Save results to database
            try:
                db.commit()
                logger.info("Document processing results saved", document_id=document_id)
            except Exception as e:
                logger.error("Failed to save processing results", error=str(e))
                db.rollback()
                return {"status": "error", "message": "Database save failed"}
            
            # Clean up temp file
            try:
                os.remove(temp_file_path)
                logger.info("Temporary file deleted", path=temp_file_path)
            except Exception as e:
                logger.warning("Failed to delete temp file", error=str(e))
            
            return {
                "status": "success", 
                "document_id": document_id,
                "summary": doc.summary,
                "qa_results": doc.qa_results
            }
            
        except Exception as e:
            logger.exception("Unhandled exception in task processor", error=str(e))
            if 'doc' in locals() and doc:
                doc.status = ProcessingStatus.FAILED
                doc.error_message = str(e)
                try:
                    db.commit()
                except:
                    db.rollback()
            return {"status": "error", "message": str(e)}
        
        finally:
            db.close()

def lambda_handler(event, context):
    """
    AWS Lambda handler for processing tasks
    """
    try:
        logger.info("Lambda task received", event=event)
        
        # Parse the event
        if 'Records' in event:
            # SQS event
            for record in event['Records']:
                try:
                    message_body = json.loads(record['body'])
                    task_name = message_body.get('task_name')
                    task_args = message_body.get('task_args', [])
                    task_kwargs = message_body.get('task_kwargs', {})
                    
                    processor = AWSTaskProcessor()
                    
                    if task_name == "process_document_task":
                        result = processor.process_document_task(*task_args, **task_kwargs)
                        logger.info("Task completed", result=result)
                    else:
                        logger.error("Unknown task name", task_name=task_name)
                        
                except Exception as e:
                    logger.error("Failed to process SQS record", error=str(e))
                    traceback.print_exc()
        else:
            # Direct invocation
            task_name = event.get('task_name')
            task_args = event.get('task_args', [])
            task_kwargs = event.get('task_kwargs', {})
            
            processor = AWSTaskProcessor()
            
            if task_name == "process_document_task":
                result = processor.process_document_task(*task_args, **task_kwargs)
                logger.info("Task completed", result=result)
                return result
            else:
                logger.error("Unknown task name", task_name=task_name)
                return {"status": "error", "message": "Unknown task"}
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error("Lambda handler failed", error=str(e))
        traceback.print_exc()
        return {"status": "error", "message": str(e)}

def process_sqs_messages():
    """
    Process messages from SQS queue (for ECS or local processing)
    """
    # Try relative import first, then absolute import
    try:
        from ..services.aws_task_service import aws_task_service
    except ImportError:
        from services.aws_task_service import aws_task_service
    
    logger.info("Starting SQS message processing")
    
    while True:
        try:
            # Receive messages from SQS
            tasks = aws_task_service.receive_tasks(max_messages=10, wait_time=20)
            
            if not tasks:
                logger.debug("No tasks received, continuing...")
                continue
            
            processor = AWSTaskProcessor()
            
            for task in tasks:
                try:
                    task_name = task.get('task_name')
                    task_args = task.get('task_args', [])
                    task_kwargs = task.get('task_kwargs', {})
                    receipt_handle = task.get('receipt_handle')
                    
                    logger.info("Processing task", task_name=task_name, task_id=task.get('task_id'))
                    
                    if task_name == "process_document_task":
                        result = processor.process_document_task(*task_args, **task_kwargs)
                        logger.info("Task completed", result=result)
                    else:
                        logger.error("Unknown task name", task_name=task_name)
                    
                    # Delete message from queue after successful processing
                    if receipt_handle:
                        aws_task_service.delete_message(receipt_handle)
                        logger.debug("Message deleted from queue")
                    
                except Exception as e:
                    logger.error("Failed to process task", error=str(e))
                    traceback.print_exc()
                    # Message will be retried or moved to DLQ
                    
        except KeyboardInterrupt:
            logger.info("SQS processing stopped by user")
            break
        except Exception as e:
            logger.error("SQS processing error", error=str(e))
            traceback.print_exc()

if __name__ == "__main__":
    # Run SQS message processor
    process_sqs_messages()

