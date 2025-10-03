import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from botocore.config import Config
import os
import uuid
from pathlib import Path
# Try relative import first, then absolute import
try:
    from ..config.setting import settings
except ImportError:
    from config.setting import settings
import structlog
from datetime import timedelta
import traceback
import tempfile
import io
from typing import Optional
logger = structlog.get_logger()

class StorageService:
    def __init__(self):
        try:
            # Initialize S3-compatible client (MinIO by default)
            endpoint = getattr(settings, "MINIO_ENDPOINT", None)
            access_key = getattr(settings, "MINIO_ACCESS_KEY", None)
            secret_key = getattr(settings, "MINIO_SECRET_KEY", None)
            bucket_name = getattr(settings, "BUCKET_NAME", None) or getattr(settings, "S3_BUCKET_NAME", None)

            self.client = boto3.client(
                's3',
                endpoint_url=f"http://{endpoint}" if endpoint and not endpoint.startswith("http") else endpoint,
                aws_access_key_id=access_key or settings.AWS_ACCESS_KEY_ID or None,
                aws_secret_access_key=secret_key or settings.AWS_SECRET_ACCESS_KEY or None,
                region_name=getattr(settings, "AWS_REGION", "us-east-1"),
                config=Config(s3={"addressing_style": "path"})
            )
            self.bucket_name = bucket_name
            self._ensure_bucket_exists()
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error("Failed to initialize S3 client", error=str(e))
            raise
    
    def _ensure_bucket_exists(self):
        try:
            logger.info("Checking if S3 bucket exists", bucket=self.bucket_name)
            self.client.head_bucket(Bucket=self.bucket_name)
            logger.info("S3 bucket exists", bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404':
                logger.info("Creating S3 bucket", bucket=self.bucket_name)
                try:
                    if settings.AWS_REGION == 'us-east-1':
                        # us-east-1 doesn't need LocationConstraint
                        self.client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION}
                        )
                    logger.info("S3 bucket created successfully", bucket=self.bucket_name)
                except ClientError as create_error:
                    logger.error("Failed to create S3 bucket", error=str(create_error))
                    raise
            else:
                logger.error("Failed to check S3 bucket", error=str(e))
                raise
    
    async def save_file(self, file_content: bytes, filename: str) -> str:
        """Save file and return the file path"""
        file_id = str(uuid.uuid4())
        file_extension = Path(filename).suffix
        object_name = f"{file_id}{file_extension}"
        
        try:
            logger.info("Uploading to S3", bucket=self.bucket_name, object=object_name)
            
            # Upload directly to S3 using put_object
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_content,
                ContentType='application/pdf' if file_extension == '.pdf' else 'application/octet-stream'
            )
            
            logger.info("File uploaded successfully to S3", object=object_name)
            return object_name
            
        except ClientError as e:
            logger.error("Failed to save file to S3", filename=filename, error=str(e))
            traceback.print_exc()
            raise
    
    def get_file_url(self, object_name: str, expiration: int = 3600) -> str:
        """Get presigned URL for file access"""
        try:
            return self.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=expiration
            )
        except ClientError as e:
            logger.error("Failed to get file URL", object_name=object_name, error=str(e))
            raise
    
    def download_file(self, object_name: str, local_path: str) -> bool:
        """Download file from S3 to local path"""
        try:
            logger.info("Downloading file from S3", object=object_name, local_path=local_path)
            self.client.download_file(self.bucket_name, object_name, local_path)
            logger.info("File downloaded successfully", object=object_name)
            return True
        except ClientError as e:
            logger.error("Failed to download file from S3", object_name=object_name, error=str(e))
            return False
    
    def delete_file(self, object_name: str) -> bool:
        """Delete file from S3"""
        try:
            logger.info("Deleting file from S3", object=object_name)
            self.client.delete_object(Bucket=self.bucket_name, Key=object_name)
            logger.info("File deleted successfully", object=object_name)
            return True
        except ClientError as e:
            logger.error("Failed to delete file from S3", object_name=object_name, error=str(e))
            return False