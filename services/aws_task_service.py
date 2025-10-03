import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import json
import structlog
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
# Try relative import first, then absolute import
try:
    from ..config.setting import settings
except ImportError:
    from config.setting import settings

logger = structlog.get_logger()

class AWSTaskService:
    """
    AWS-based task queue service using SQS for message queuing
    and Lambda for task processing (or ECS for long-running tasks)
    """
    
    def __init__(self):
        try:
            # Initialize SQS client
            self.sqs = boto3.client(
                'sqs',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            # Initialize Lambda client for task processing
            self.lambda_client = boto3.client(
                'lambda',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            
            self.queue_url = settings.SQS_QUEUE_URL
            self.lambda_function_name = settings.LAMBDA_FUNCTION_NAME
            
            # Create queue if it doesn't exist
            self._ensure_queue_exists()
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error("Failed to initialize AWS task service", error=str(e))
            raise
    
    def _ensure_queue_exists(self):
        """Create SQS queue if it doesn't exist"""
        try:
            # Try to get queue URL
            response = self.sqs.get_queue_url(QueueName=settings.SQS_QUEUE_NAME)
            self.queue_url = response['QueueUrl']
            logger.info("SQS queue exists", queue_url=self.queue_url)
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                logger.info("Creating SQS queue", queue_name=settings.SQS_QUEUE_NAME)
                try:
                    response = self.sqs.create_queue(
                        QueueName=settings.SQS_QUEUE_NAME,
                        Attributes={
                            'VisibilityTimeoutSeconds': '300',  # 5 minutes
                            'MessageRetentionPeriod': '1209600',  # 14 days
                            'ReceiveMessageWaitTimeSeconds': '20'  # Long polling
                        }
                    )
                    self.queue_url = response['QueueUrl']
                    logger.info("SQS queue created successfully", queue_url=self.queue_url)
                except ClientError as create_error:
                    logger.error("Failed to create SQS queue", error=str(create_error))
                    raise
            else:
                logger.error("Failed to check SQS queue", error=str(e))
                raise
    
    def send_task(self, task_name: str, task_args: List[Any], task_kwargs: Dict[str, Any] = None) -> str:
        """
        Send a task to the queue
        :param task_name: Name of the task to execute
        :param task_args: Positional arguments for the task
        :param task_kwargs: Keyword arguments for the task
        :return: Task ID
        """
        try:
            task_id = str(uuid.uuid4())
            task_message = {
                'task_id': task_id,
                'task_name': task_name,
                'task_args': task_args or [],
                'task_kwargs': task_kwargs or {},
                'created_at': datetime.utcnow().isoformat(),
                'retry_count': 0
            }
            
            response = self.sqs.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(task_message),
                MessageAttributes={
                    'task_name': {
                        'StringValue': task_name,
                        'DataType': 'String'
                    },
                    'task_id': {
                        'StringValue': task_id,
                        'DataType': 'String'
                    }
                }
            )
            
            logger.info("Task sent to SQS", task_id=task_id, task_name=task_name)
            return task_id
            
        except Exception as e:
            logger.error("Failed to send task", task_name=task_name, error=str(e))
            raise
    
    def send_lambda_task(self, task_name: str, task_args: List[Any], task_kwargs: Dict[str, Any] = None) -> str:
        """
        Send a task directly to Lambda function
        :param task_name: Name of the task to execute
        :param task_args: Positional arguments for the task
        :param task_kwargs: Keyword arguments for the task
        :return: Task ID
        """
        try:
            task_id = str(uuid.uuid4())
            payload = {
                'task_id': task_id,
                'task_name': task_name,
                'task_args': task_args or [],
                'task_kwargs': task_kwargs or {},
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.lambda_client.invoke(
                FunctionName=self.lambda_function_name,
                InvocationType='Event',  # Async invocation
                Payload=json.dumps(payload)
            )
            
            logger.info("Task sent to Lambda", task_id=task_id, task_name=task_name)
            return task_id
            
        except Exception as e:
            logger.error("Failed to send Lambda task", task_name=task_name, error=str(e))
            raise
    
    def receive_tasks(self, max_messages: int = 10, wait_time: int = 20) -> List[Dict[str, Any]]:
        """
        Receive tasks from the queue
        :param max_messages: Maximum number of messages to receive
        :param wait_time: Long polling wait time
        :return: List of task messages
        """
        try:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time,
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            tasks = []
            
            for message in messages:
                try:
                    task_data = json.loads(message['Body'])
                    task_data['receipt_handle'] = message['ReceiptHandle']
                    tasks.append(task_data)
                except json.JSONDecodeError as e:
                    logger.error("Failed to parse task message", error=str(e))
                    # Delete malformed message
                    self.delete_message(message['ReceiptHandle'])
            
            logger.debug("Received tasks from SQS", count=len(tasks))
            return tasks
            
        except Exception as e:
            logger.error("Failed to receive tasks", error=str(e))
            return []
    
    def delete_message(self, receipt_handle: str) -> bool:
        """
        Delete a message from the queue
        :param receipt_handle: Receipt handle of the message to delete
        :return: True if successful
        """
        try:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.debug("Message deleted from SQS", receipt_handle=receipt_handle)
            return True
        except Exception as e:
            logger.error("Failed to delete message", error=str(e))
            return False
    
    def get_queue_attributes(self) -> Dict[str, Any]:
        """
        Get queue attributes
        :return: Queue attributes
        """
        try:
            response = self.sqs.get_queue_attributes(
                QueueUrl=self.queue_url,
                AttributeNames=['All']
            )
            return response['Attributes']
        except Exception as e:
            logger.error("Failed to get queue attributes", error=str(e))
            return {}
    
    def purge_queue(self) -> bool:
        """
        Purge all messages from the queue
        :return: True if successful
        """
        try:
            self.sqs.purge_queue(QueueUrl=self.queue_url)
            logger.info("Queue purged successfully")
            return True
        except Exception as e:
            logger.error("Failed to purge queue", error=str(e))
            return False

# Create a singleton instance
aws_task_service = AWSTaskService()

