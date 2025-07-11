from minio import Minio
from minio.error import S3Error
import os
import uuid
from pathlib import Path
from config.setting import settings
import structlog
from datetime import timedelta
import traceback
import tempfile
logger = structlog.get_logger()

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        try:
            logger.info("Checking if bucket exists", bucket=settings.BUCKET_NAME)
            if not self.client.bucket_exists(settings.BUCKET_NAME):
                logger.info("Creating bucket", bucket=settings.BUCKET_NAME)
                self.client.make_bucket(settings.BUCKET_NAME)
                logger.info("Bucket created successfully", bucket=settings.BUCKET_NAME)
            else:
                logger.info("Bucket already exists", bucket=settings.BUCKET_NAME)
        except S3Error as e:
            logger.error("Failed to create bucket", error=str(e))
            traceback.print_exc()
            raise
    
    async def save_file(self, file_content: bytes, filename: str) -> str:
        """Save file and return the file path"""
        file_id = str(uuid.uuid4())
        file_extension = Path(filename).suffix
        object_name = f"{file_id}{file_extension}"
        
        try:
            # Save to local temp first using system temp directory
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(temp_dir, object_name)
            logger.info("Saving temporary file", temp_path=temp_path)
            
            with open(temp_path, "wb") as f:
                f.write(file_content)
            
            # Upload to MinIO
            logger.info("Uploading to MinIO", bucket=settings.BUCKET_NAME, object=object_name)
            self.client.fput_object(
                settings.BUCKET_NAME,
                object_name,
                temp_path
            )
            
            # Clean up temp file
            logger.info("Cleaning up temporary file", temp_path=temp_path)
            os.remove(temp_path)
            
            return object_name
            
        except S3Error as e:
            logger.error("Failed to save file", filename=filename, error=str(e))
            traceback.print_exc()  # Print the full traceback to the console
            raise
    
    def get_file_url(self, object_name: str) -> str:
        """Get presigned URL for file access"""
        try:
            return self.client.presigned_get_object(
                settings.BUCKET_NAME,
                object_name,
                expires=timedelta(hours=1)
            )
        except S3Error as e:
            logger.error("Failed to get file URL", object_name=object_name, error=str(e))
            raise