import redis
import sys
import os
import json
from typing import Optional, Any, Union
import structlog

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.setting import settings

logger = structlog.get_logger()

class RedisService:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
    
    def set_key(self, key: str, value: Any, expire_seconds: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis
        :param key: The key to set
        :param value: The value to set (will be JSON serialized)
        :param expire_seconds: Optional expiration time in seconds
        :return: True if successful
        """
        try:
            serialized_value = json.dumps(value)
            if expire_seconds:
                return self.redis_client.setex(key, expire_seconds, serialized_value)
            return self.redis_client.set(key, serialized_value)
        except Exception as e:
            logger.error("Error setting Redis key", key=key, error=str(e))
            return False
    
    def get_key(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis
        :param key: The key to get
        :return: The deserialized value or None if not found
        """
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error("Error getting Redis key", key=key, error=str(e))
            return None
    
    def delete_key(self, key: str) -> bool:
        """
        Delete a key from Redis
        :param key: The key to delete
        :return: True if successful
        """
        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error("Error deleting Redis key", key=key, error=str(e))
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis
        :param key: The key to check
        :return: True if the key exists
        """
        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error("Error checking Redis key", key=key, error=str(e))
            return False
    
    def set_hash(self, name: str, mapping: dict) -> bool:
        """
        Set a hash in Redis
        :param name: The hash name
        :param mapping: Dictionary of key-value pairs
        :return: True if successful
        """
        try:
            serialized_mapping = {k: json.dumps(v) for k, v in mapping.items()}
            return bool(self.redis_client.hset(name, mapping=serialized_mapping))
        except Exception as e:
            logger.error("Error setting Redis hash", name=name, error=str(e))
            return False
    
    def get_hash(self, name: str) -> Optional[dict]:
        """
        Get a hash from Redis
        :param name: The hash name
        :return: Dictionary of key-value pairs or None if not found
        """
        try:
            hash_data = self.redis_client.hgetall(name)
            if hash_data:
                return {k.decode(): json.loads(v) for k, v in hash_data.items()}
            return None
        except Exception as e:
            logger.error("Error getting Redis hash", name=name, error=str(e))
            return None

# Create a singleton instance
redis_service = RedisService() 