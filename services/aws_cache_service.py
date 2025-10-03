import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import json
import structlog
from typing import Optional, Any, Dict
from datetime import datetime, timedelta
import os
# Try relative import first, then absolute import
try:
    from ..config.setting import settings
except ImportError:
    from config.setting import settings

logger = structlog.get_logger()

class AWSCacheService:
    """
    AWS-based caching service using DynamoDB for persistent cache
    and ElastiCache (Redis) for high-performance caching
    """
    
    def __init__(self):
        try:
            # Initialize DynamoDB for persistent caching
            self.dynamodb = boto3.client(
                'dynamodb',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.table_name = settings.DYNAMODB_CACHE_TABLE
            
            # Initialize ElastiCache Redis if available
            if hasattr(settings, 'ELASTICACHE_ENDPOINT') and settings.ELASTICACHE_ENDPOINT:
                import redis
                self.redis_client = redis.Redis(
                    host=settings.ELASTICACHE_ENDPOINT,
                    port=6379,
                    decode_responses=True
                )
            else:
                self.redis_client = None
                logger.warning("ElastiCache not configured, using DynamoDB only")
            
            self._ensure_table_exists()
            
        except NoCredentialsError:
            logger.error("AWS credentials not found")
            raise
        except Exception as e:
            logger.error("Failed to initialize AWS cache service", error=str(e))
            raise
    
    def _ensure_table_exists(self):
        """Create DynamoDB table if it doesn't exist"""
        try:
            self.dynamodb.describe_table(TableName=self.table_name)
            logger.info("DynamoDB cache table exists", table=self.table_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.info("Creating DynamoDB cache table", table=self.table_name)
                try:
                    self.dynamodb.create_table(
                        TableName=self.table_name,
                        KeySchema=[
                            {'AttributeName': 'cache_key', 'KeyType': 'HASH'}
                        ],
                        AttributeDefinitions=[
                            {'AttributeName': 'cache_key', 'AttributeType': 'S'}
                        ],
                        BillingMode='PAY_PER_REQUEST'
                    )
                    # Wait for table to be created
                    waiter = self.dynamodb.get_waiter('table_exists')
                    waiter.wait(TableName=self.table_name)
                    logger.info("DynamoDB cache table created successfully", table=self.table_name)
                except ClientError as create_error:
                    logger.error("Failed to create DynamoDB table", error=str(create_error))
                    raise
            else:
                logger.error("Failed to check DynamoDB table", error=str(e))
                raise
    
    def set_key(self, key: str, value: Any, expire_seconds: Optional[int] = None) -> bool:
        """
        Set a key-value pair in cache
        :param key: The key to set
        :param value: The value to set (will be JSON serialized)
        :param expire_seconds: Optional expiration time in seconds
        :return: True if successful
        """
        try:
            serialized_value = json.dumps(value)
            ttl = None
            if expire_seconds:
                ttl = int((datetime.utcnow() + timedelta(seconds=expire_seconds)).timestamp())
            
            # Try Redis first if available
            if self.redis_client:
                try:
                    if expire_seconds:
                        result = self.redis_client.setex(key, expire_seconds, serialized_value)
                    else:
                        result = self.redis_client.set(key, serialized_value)
                    if result:
                        logger.debug("Key set in Redis", key=key)
                        return True
                except Exception as e:
                    logger.warning("Redis set failed, falling back to DynamoDB", error=str(e))
            
            # Fallback to DynamoDB
            item = {
                'cache_key': {'S': key},
                'value': {'S': serialized_value},
                'created_at': {'N': str(int(datetime.utcnow().timestamp()))}
            }
            
            if ttl:
                item['ttl'] = {'N': str(ttl)}
            
            self.dynamodb.put_item(TableName=self.table_name, Item=item)
            logger.debug("Key set in DynamoDB", key=key)
            return True
            
        except Exception as e:
            logger.error("Error setting cache key", key=key, error=str(e))
            return False
    
    def get_key(self, key: str) -> Optional[Any]:
        """
        Get a value from cache
        :param key: The key to get
        :return: The deserialized value or None if not found
        """
        try:
            # Try Redis first if available
            if self.redis_client:
                try:
                    value = self.redis_client.get(key)
                    if value:
                        logger.debug("Key found in Redis", key=key)
                        return json.loads(value)
                except Exception as e:
                    logger.warning("Redis get failed, falling back to DynamoDB", error=str(e))
            
            # Fallback to DynamoDB
            response = self.dynamodb.get_item(
                TableName=self.table_name,
                Key={'cache_key': {'S': key}}
            )
            
            if 'Item' in response:
                item = response['Item']
                
                # Check TTL
                if 'ttl' in item:
                    ttl = int(item['ttl']['N'])
                    if datetime.utcnow().timestamp() > ttl:
                        logger.debug("Key expired in DynamoDB", key=key)
                        self.delete_key(key)
                        return None
                
                value = item['value']['S']
                logger.debug("Key found in DynamoDB", key=key)
                return json.loads(value)
            
            return None
            
        except Exception as e:
            logger.error("Error getting cache key", key=key, error=str(e))
            return None
    
    def delete_key(self, key: str) -> bool:
        """
        Delete a key from cache
        :param key: The key to delete
        :return: True if successful
        """
        try:
            # Try Redis first if available
            if self.redis_client:
                try:
                    result = self.redis_client.delete(key)
                    if result:
                        logger.debug("Key deleted from Redis", key=key)
                except Exception as e:
                    logger.warning("Redis delete failed, falling back to DynamoDB", error=str(e))
            
            # Fallback to DynamoDB
            self.dynamodb.delete_item(
                TableName=self.table_name,
                Key={'cache_key': {'S': key}}
            )
            logger.debug("Key deleted from DynamoDB", key=key)
            return True
            
        except Exception as e:
            logger.error("Error deleting cache key", key=key, error=str(e))
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in cache
        :param key: The key to check
        :return: True if the key exists
        """
        try:
            # Try Redis first if available
            if self.redis_client:
                try:
                    result = self.redis_client.exists(key)
                    if result:
                        logger.debug("Key exists in Redis", key=key)
                        return True
                except Exception as e:
                    logger.warning("Redis exists check failed, falling back to DynamoDB", error=str(e))
            
            # Fallback to DynamoDB
            response = self.dynamodb.get_item(
                TableName=self.table_name,
                Key={'cache_key': {'S': key}}
            )
            
            if 'Item' in response:
                # Check TTL
                item = response['Item']
                if 'ttl' in item:
                    ttl = int(item['ttl']['N'])
                    if datetime.utcnow().timestamp() > ttl:
                        logger.debug("Key expired in DynamoDB", key=key)
                        self.delete_key(key)
                        return False
                
                logger.debug("Key exists in DynamoDB", key=key)
                return True
            
            return False
            
        except Exception as e:
            logger.error("Error checking cache key", key=key, error=str(e))
            return False
    
    def set_hash(self, name: str, mapping: Dict[str, Any]) -> bool:
        """
        Set a hash in cache
        :param name: The hash name
        :param mapping: Dictionary of key-value pairs
        :return: True if successful
        """
        try:
            serialized_mapping = {k: json.dumps(v) for k, v in mapping.items()}
            
            # Try Redis first if available
            if self.redis_client:
                try:
                    result = self.redis_client.hset(name, mapping=serialized_mapping)
                    if result is not None:
                        logger.debug("Hash set in Redis", name=name)
                        return True
                except Exception as e:
                    logger.warning("Redis hash set failed, falling back to DynamoDB", error=str(e))
            
            # Fallback to DynamoDB - store as individual items
            for field, value in serialized_mapping.items():
                key = f"{name}:{field}"
                self.set_key(key, value)
            
            logger.debug("Hash set in DynamoDB", name=name)
            return True
            
        except Exception as e:
            logger.error("Error setting cache hash", name=name, error=str(e))
            return False
    
    def get_hash(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a hash from cache
        :param name: The hash name
        :return: Dictionary of key-value pairs or None if not found
        """
        try:
            # Try Redis first if available
            if self.redis_client:
                try:
                    hash_data = self.redis_client.hgetall(name)
                    if hash_data:
                        result = {k: json.loads(v) for k, v in hash_data.items()}
                        logger.debug("Hash found in Redis", name=name)
                        return result
                except Exception as e:
                    logger.warning("Redis hash get failed, falling back to DynamoDB", error=str(e))
            
            # Fallback to DynamoDB - get all items with prefix
            # This is a simplified implementation
            # In production, you might want to use a different approach
            logger.warning("Hash get from DynamoDB not fully implemented for production")
            return None
            
        except Exception as e:
            logger.error("Error getting cache hash", name=name, error=str(e))
            return None

# Create a singleton instance
aws_cache_service = AWSCacheService()

