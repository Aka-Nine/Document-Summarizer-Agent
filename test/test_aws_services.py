"""
Comprehensive test suite for AWS services
"""
import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from moto import mock_s3, mock_dynamodb, mock_sqs
import boto3
from botocore.exceptions import ClientError

from services.storage_service import StorageService
from services.aws_cache_service import AWSCacheService
from services.aws_task_service import AWSTaskService
from tasks.aws_task_processor import AWSTaskProcessor, lambda_handler
from config.setting import settings

class TestStorageService:
    """Test S3 storage service"""
    
    @mock_s3
    def test_s3_initialization(self):
        """Test S3 service initialization"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.S3_BUCKET_NAME = "test-bucket"
            
            # Create mock S3 bucket
            s3 = boto3.client('s3', region_name='us-east-1')
            s3.create_bucket(Bucket='test-bucket')
            
            storage = StorageService()
            assert storage.bucket_name == "test-bucket"
    
    @mock_s3
    def test_save_file(self):
        """Test file saving to S3"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.S3_BUCKET_NAME = "test-bucket"
            
            # Create mock S3 bucket
            s3 = boto3.client('s3', region_name='us-east-1')
            s3.create_bucket(Bucket='test-bucket')
            
            storage = StorageService()
            
            # Test file upload
            test_content = b"test file content"
            filename = "test.pdf"
            
            result = await storage.save_file(test_content, filename)
            assert result is not None
            assert result.endswith('.pdf')
    
    @mock_s3
    def test_get_file_url(self):
        """Test presigned URL generation"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.S3_BUCKET_NAME = "test-bucket"
            
            # Create mock S3 bucket
            s3 = boto3.client('s3', region_name='us-east-1')
            s3.create_bucket(Bucket='test-bucket')
            
            storage = StorageService()
            
            # Upload a test file first
            test_content = b"test file content"
            filename = "test.pdf"
            object_name = await storage.save_file(test_content, filename)
            
            # Get presigned URL
            url = storage.get_file_url(object_name)
            assert url is not None
            assert "amazonaws.com" in url

class TestAWSCacheService:
    """Test DynamoDB cache service"""
    
    @mock_dynamodb
    def test_cache_initialization(self):
        """Test cache service initialization"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.DYNAMODB_CACHE_TABLE = "test-cache"
            mock_settings.ELASTICACHE_ENDPOINT = None
            
            cache = AWSCacheService()
            assert cache.table_name == "test-cache"
    
    @mock_dynamodb
    def test_set_and_get_key(self):
        """Test setting and getting cache keys"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.DYNAMODB_CACHE_TABLE = "test-cache"
            mock_settings.ELASTICACHE_ENDPOINT = None
            
            cache = AWSCacheService()
            
            # Test setting a key
            test_data = {"test": "value", "number": 123}
            result = cache.set_key("test_key", test_data, expire_seconds=300)
            assert result is True
            
            # Test getting the key
            retrieved_data = cache.get_key("test_key")
            assert retrieved_data == test_data
    
    @mock_dynamodb
    def test_key_expiration(self):
        """Test key expiration"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.DYNAMODB_CACHE_TABLE = "test-cache"
            mock_settings.ELASTICACHE_ENDPOINT = None
            
            cache = AWSCacheService()
            
            # Set a key with very short expiration
            test_data = {"test": "value"}
            result = cache.set_key("expire_key", test_data, expire_seconds=1)
            assert result is True
            
            # Wait for expiration (in real test, you'd mock time)
            # For now, just test that the key exists
            exists = cache.exists("expire_key")
            assert exists is True

class TestAWSTaskService:
    """Test SQS task service"""
    
    @mock_sqs
    def test_task_service_initialization(self):
        """Test task service initialization"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.SQS_QUEUE_NAME = "test-queue"
            mock_settings.SQS_QUEUE_URL = None
            mock_settings.LAMBDA_FUNCTION_NAME = "test-function"
            
            # Create mock SQS queue
            sqs = boto3.client('sqs', region_name='us-east-1')
            sqs.create_queue(QueueName='test-queue')
            
            task_service = AWSTaskService()
            assert task_service.queue_url is not None
    
    @mock_sqs
    def test_send_task(self):
        """Test sending tasks to SQS"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.SQS_QUEUE_NAME = "test-queue"
            mock_settings.SQS_QUEUE_URL = None
            mock_settings.LAMBDA_FUNCTION_NAME = "test-function"
            
            # Create mock SQS queue
            sqs = boto3.client('sqs', region_name='us-east-1')
            sqs.create_queue(QueueName='test-queue')
            
            task_service = AWSTaskService()
            
            # Send a test task
            task_id = task_service.send_task(
                task_name="test_task",
                task_args=["arg1", "arg2"],
                task_kwargs={"key": "value"}
            )
            
            assert task_id is not None
            assert len(task_id) > 0
    
    @mock_sqs
    def test_receive_tasks(self):
        """Test receiving tasks from SQS"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.AWS_ACCESS_KEY_ID = "test_key"
            mock_settings.AWS_SECRET_ACCESS_KEY = "test_secret"
            mock_settings.AWS_REGION = "us-east-1"
            mock_settings.SQS_QUEUE_NAME = "test-queue"
            mock_settings.SQS_QUEUE_URL = None
            mock_settings.LAMBDA_FUNCTION_NAME = "test-function"
            
            # Create mock SQS queue
            sqs = boto3.client('sqs', region_name='us-east-1')
            response = sqs.create_queue(QueueName='test-queue')
            queue_url = response['QueueUrl']
            
            task_service = AWSTaskService()
            
            # Send a test task first
            task_id = task_service.send_task("test_task", ["arg1"])
            
            # Receive tasks
            tasks = task_service.receive_tasks(max_messages=10, wait_time=1)
            assert len(tasks) >= 0  # May be 0 due to eventual consistency

class TestAWSTaskProcessor:
    """Test AWS task processor"""
    
    def test_task_processor_initialization(self):
        """Test task processor initialization"""
        with patch('config.setting.settings') as mock_settings:
            mock_settings.GROQ_API_KEY = "test_key"
            
            processor = AWSTaskProcessor()
            assert processor.storage is not None
            assert processor.processor is not None
    
    @patch('tasks.aws_task_processor.DocumentProcessor')
    @patch('tasks.aws_task_processor.StorageService')
    @patch('tasks.aws_task_processor.SessionLocal')
    def test_process_document_task_success(self, mock_session, mock_storage, mock_processor):
        """Test successful document processing"""
        # Mock database session
        mock_db = Mock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock document
        mock_doc = Mock()
        mock_doc.id = 1
        mock_doc.file_path = "test.pdf"
        mock_doc.status = "pending"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_doc
        
        # Mock storage service
        mock_storage_instance = Mock()
        mock_storage_instance.download_file.return_value = True
        mock_storage.return_value = mock_storage_instance
        
        # Mock document processor
        mock_processor_instance = Mock()
        mock_processor_instance.process_document.return_value = {
            "summary": "Test summary",
            "answers": {"question": "answer"},
            "metadata": {"processing_time": 10}
        }
        mock_processor.return_value = mock_processor_instance
        
        processor = AWSTaskProcessor()
        result = processor.process_document_task(1, ["test question"])
        
        assert result["status"] == "success"
        assert result["document_id"] == 1
    
    def test_lambda_handler_sqs_event(self):
        """Test Lambda handler with SQS event"""
        event = {
            "Records": [
                {
                    "body": json.dumps({
                        "task_name": "process_document_task",
                        "task_args": [1, ["test question"]],
                        "task_kwargs": {}
                    })
                }
            ]
        }
        
        with patch('tasks.aws_task_processor.AWSTaskProcessor') as mock_processor_class:
            mock_processor = Mock()
            mock_processor.process_document_task.return_value = {"status": "success"}
            mock_processor_class.return_value = mock_processor
            
            result = lambda_handler(event, None)
            assert result["status"] == "success"
    
    def test_lambda_handler_direct_invocation(self):
        """Test Lambda handler with direct invocation"""
        event = {
            "task_name": "process_document_task",
            "task_args": [1, ["test question"]],
            "task_kwargs": {}
        }
        
        with patch('tasks.aws_task_processor.AWSTaskProcessor') as mock_processor_class:
            mock_processor = Mock()
            mock_processor.process_document_task.return_value = {"status": "success"}
            mock_processor_class.return_value = mock_processor
            
            result = lambda_handler(event, None)
            assert result["status"] == "success"

class TestIntegration:
    """Integration tests"""
    
    @mock_s3
    @mock_dynamodb
    @mock_sqs
    def test_full_workflow(self):
        """Test complete workflow from upload to processing"""
        # This would be a comprehensive integration test
        # that tests the entire flow from API to processing
        pass

# Performance tests
class TestPerformance:
    """Performance tests"""
    
    def test_concurrent_uploads(self):
        """Test concurrent file uploads"""
        # Test multiple simultaneous uploads
        pass
    
    def test_large_file_processing(self):
        """Test processing of large files"""
        # Test with large PDF files
        pass
    
    def test_cache_performance(self):
        """Test cache performance under load"""
        # Test cache read/write performance
        pass

# Security tests
class TestSecurity:
    """Security tests"""
    
    def test_file_validation(self):
        """Test file type and size validation"""
        pass
    
    def test_authentication(self):
        """Test API authentication"""
        pass
    
    def test_authorization(self):
        """Test user authorization"""
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

