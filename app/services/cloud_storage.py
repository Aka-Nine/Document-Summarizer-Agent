"""
Enterprise Cloud Storage Service
Supports AWS S3, Azure Blob Storage, GCP Cloud Storage, and MinIO
"""
from abc import ABC, abstractmethod
from typing import Optional, BinaryIO
import structlog
import os
import shutil
from pathlib import Path
from datetime import timedelta
from app.config.settings import settings, CloudProvider
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from minio import Minio
from minio.error import S3Error

logger = structlog.get_logger()


class CloudStorageInterface(ABC):
    """Abstract interface for cloud storage operations"""
    
    @abstractmethod
    async def upload_file(self, file_content: bytes, object_key: str, content_type: str = "application/octet-stream") -> str:
        """Upload file to cloud storage"""
        pass
    
    @abstractmethod
    async def download_file(self, object_key: str) -> bytes:
        """Download file from cloud storage"""
        pass
    
    @abstractmethod
    def get_presigned_url(self, object_key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL for file access"""
        pass
    
    @abstractmethod
    def delete_file(self, object_key: str) -> bool:
        """Delete file from cloud storage"""
        pass
    
    @abstractmethod
    def file_exists(self, object_key: str) -> bool:
        """Check if file exists"""
        pass


class S3StorageService(CloudStorageInterface):
    """AWS S3 Storage Service"""
    
    def __init__(self):
        self.bucket_name = settings.AWS_S3_BUCKET_NAME or settings.BUCKET_NAME
        self.s3_client = boto3.client(
            's3',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.AWS_S3_ENDPOINT_URL
        )
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure bucket exists, create if not"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info("S3 bucket exists", bucket=self.bucket_name)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            if error_code == '404':
                try:
                    if settings.AWS_REGION:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': settings.AWS_REGION}
                        )
                    else:
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    logger.info("S3 bucket created", bucket=self.bucket_name)
                except ClientError as create_error:
                    logger.error("Failed to create S3 bucket", error=str(create_error))
                    raise
            else:
                logger.error("Failed to check S3 bucket", error=str(e))
                raise
    
    async def upload_file(self, file_content: bytes, object_key: str, content_type: str = "application/octet-stream") -> str:
        """Upload file to S3"""
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=object_key,
                Body=file_content,
                ContentType=content_type
            )
            logger.info("File uploaded to S3", bucket=self.bucket_name, key=object_key)
            return object_key
        except (ClientError, BotoCoreError) as e:
            logger.error("S3 upload failed", error=str(e), key=object_key)
            raise
    
    async def download_file(self, object_key: str) -> bytes:
        """Download file from S3"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=object_key)
            return response['Body'].read()
        except (ClientError, BotoCoreError) as e:
            logger.error("S3 download failed", error=str(e), key=object_key)
            raise
    
    def get_presigned_url(self, object_key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL"""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': object_key},
                ExpiresIn=expires_in
            )
            return url
        except (ClientError, BotoCoreError) as e:
            logger.error("Failed to generate presigned URL", error=str(e))
            raise
    
    def delete_file(self, object_key: str) -> bool:
        """Delete file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_key)
            logger.info("File deleted from S3", key=object_key)
            return True
        except (ClientError, BotoCoreError) as e:
            logger.error("S3 delete failed", error=str(e), key=object_key)
            return False
    
    def file_exists(self, object_key: str) -> bool:
        """Check if file exists in S3"""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=object_key)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise


class MinIOStorageService(CloudStorageInterface):
    """MinIO Storage Service (S3-compatible)"""
    
    def __init__(self):
        self.bucket_name = settings.BUCKET_NAME
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure bucket exists"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info("MinIO bucket created", bucket=self.bucket_name)
            else:
                logger.info("MinIO bucket exists", bucket=self.bucket_name)
        except S3Error as e:
            logger.error("MinIO bucket operation failed", error=str(e))
            raise
    
    async def upload_file(self, file_content: bytes, object_key: str, content_type: str = "application/octet-stream") -> str:
        """Upload file to MinIO"""
        import tempfile
        import os
        
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(file_content)
                tmp_path = tmp_file.name
            
            self.client.fput_object(
                self.bucket_name,
                object_key,
                tmp_path,
                content_type=content_type
            )
            os.remove(tmp_path)
            logger.info("File uploaded to MinIO", key=object_key)
            return object_key
        except S3Error as e:
            logger.error("MinIO upload failed", error=str(e), key=object_key)
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            raise
    
    async def download_file(self, object_key: str) -> bytes:
        """Download file from MinIO"""
        import tempfile
        import os
        
        try:
            tmp_path = tempfile.mktemp()
            self.client.fget_object(self.bucket_name, object_key, tmp_path)
            
            with open(tmp_path, 'rb') as f:
                content = f.read()
            
            os.remove(tmp_path)
            return content
        except S3Error as e:
            logger.error("MinIO download failed", error=str(e), key=object_key)
            raise
    
    def get_presigned_url(self, object_key: str, expires_in: int = 3600) -> str:
        """Generate presigned URL"""
        try:
            from datetime import timedelta
            url = self.client.presigned_get_object(
                self.bucket_name,
                object_key,
                expires=timedelta(seconds=expires_in)
            )
            return url
        except S3Error as e:
            logger.error("Failed to generate presigned URL", error=str(e))
            raise
    
    def delete_file(self, object_key: str) -> bool:
        """Delete file from MinIO"""
        try:
            self.client.remove_object(self.bucket_name, object_key)
            logger.info("File deleted from MinIO", key=object_key)
            return True
        except S3Error as e:
            logger.error("MinIO delete failed", error=str(e), key=object_key)
            return False
    
    def file_exists(self, object_key: str) -> bool:
        """Check if file exists"""
        try:
            self.client.stat_object(self.bucket_name, object_key)
            return True
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return False
            raise


class FilesystemStorageService(CloudStorageInterface):
    """Local filesystem storage service (no Docker needed)"""
    
    def __init__(self):
        self.storage_path = Path(settings.FILESYSTEM_STORAGE_PATH)
        self.base_url = settings.FILESYSTEM_BASE_URL
        
        # Create storage directory if it doesn't exist
        self.storage_path.mkdir(parents=True, exist_ok=True)
        logger.info("Filesystem storage initialized", path=str(self.storage_path))
    
    def _get_file_path(self, object_key: str) -> Path:
        """Get full file path for object key"""
        return self.storage_path / object_key
    
    async def upload_file(self, file_content: bytes, object_key: str, content_type: str = "application/octet-stream") -> str:
        """Upload file to local filesystem"""
        try:
            file_path = self._get_file_path(object_key)
            
            # Create parent directories if needed
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            logger.info("File uploaded to filesystem", key=object_key, path=str(file_path))
            return object_key
        except Exception as e:
            logger.error("Filesystem upload failed", error=str(e), key=object_key)
            raise
    
    async def download_file(self, object_key: str) -> bytes:
        """Download file from local filesystem"""
        try:
            file_path = self._get_file_path(object_key)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {object_key}")
            
            with open(file_path, "rb") as f:
                content = f.read()
            
            logger.info("File downloaded from filesystem", key=object_key)
            return content
        except FileNotFoundError:
            logger.error("File not found in filesystem", key=object_key)
            raise
        except Exception as e:
            logger.error("Filesystem download failed", error=str(e), key=object_key)
            raise
    
    def get_presigned_url(self, object_key: str, expires_in: int = 3600) -> str:
        """Generate URL for file access (filesystem uses direct URL)"""
        # For filesystem, we return a direct URL
        # In production, you might want to serve files through FastAPI
        file_path = self._get_file_path(object_key)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {object_key}")
        
        # Return URL that can be served by FastAPI
        url = f"{self.base_url}/{object_key}"
        logger.info("Generated filesystem URL", key=object_key, url=url)
        return url
    
    def delete_file(self, object_key: str) -> bool:
        """Delete file from local filesystem"""
        try:
            file_path = self._get_file_path(object_key)
            
            if file_path.exists():
                file_path.unlink()
                logger.info("File deleted from filesystem", key=object_key)
                return True
            else:
                logger.warning("File not found for deletion", key=object_key)
                return False
        except Exception as e:
            logger.error("Filesystem delete failed", error=str(e), key=object_key)
            return False
    
    def file_exists(self, object_key: str) -> bool:
        """Check if file exists in filesystem"""
        try:
            file_path = self._get_file_path(object_key)
            exists = file_path.exists() and file_path.is_file()
            return exists
        except Exception as e:
            logger.error("Filesystem exists check failed", error=str(e), key=object_key)
            return False


class CloudStorageService:
    """Factory for cloud storage services"""
    
    @staticmethod
    def create() -> CloudStorageInterface:
        """Create appropriate storage service based on configuration"""
        provider = settings.CLOUD_PROVIDER
        
        if provider == CloudProvider.AWS:
            if not settings.AWS_S3_BUCKET_NAME and not settings.BUCKET_NAME:
                raise ValueError("AWS_S3_BUCKET_NAME or BUCKET_NAME must be set")
            return S3StorageService()
        
        elif provider == CloudProvider.LOCAL:
            if not all([settings.MINIO_ENDPOINT, settings.MINIO_ACCESS_KEY, settings.MINIO_SECRET_KEY, settings.BUCKET_NAME]):
                raise ValueError("MinIO configuration incomplete")
            return MinIOStorageService()
        
        elif provider == CloudProvider.FILESYSTEM:
            # Filesystem storage - no Docker needed!
            return FilesystemStorageService()
        
        # TODO: Add Azure and GCP implementations
        elif provider == CloudProvider.AZURE:
            raise NotImplementedError("Azure Blob Storage not yet implemented")
        
        elif provider == CloudProvider.GCP:
            raise NotImplementedError("GCP Cloud Storage not yet implemented")
        
        else:
            raise ValueError(f"Unsupported cloud provider: {provider}")

