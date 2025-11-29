import redis
import sys
import os
import json
from typing import Optional, Any, Union
import structlog

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.config.settings import settings
except ImportError:
    from app.config.setting import settings

logger = structlog.get_logger()


class RedisService:
    """Redis service with Redis Cloud support (NO SSL - uses username/password)"""
    
    def __init__(self):
        provider = getattr(settings, "REDIS_PROVIDER", "redis").lower()
        
        # Check if using Redis Cloud (NO SSL - uses username/password)
        if provider == "redis_cloud":
            # Use Redis Cloud settings
            if settings.REDIS_CLOUD_ENDPOINT:
                host = settings.REDIS_CLOUD_ENDPOINT
                port = settings.REDIS_CLOUD_PORT or 14497
                username = settings.REDIS_CLOUD_USERNAME or "default"
                password = settings.REDIS_CLOUD_PASSWORD
            elif settings.REDIS_URL:
                # Parse from URL if provided
                from urllib.parse import urlparse
                parsed = urlparse(settings.REDIS_URL)
                host = parsed.hostname
                port = parsed.port or 14497
                username = parsed.username or "default"
                password = parsed.password
            else:
                raise ValueError("Redis Cloud requires REDIS_CLOUD_ENDPOINT or REDIS_URL")
            
            if not password:
                raise ValueError("REDIS_CLOUD_PASSWORD is required for Redis Cloud")
            
            # Create Redis Cloud client (NO SSL - uses username/password)
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                username=username,
                password=password,
                decode_responses=False,  # Keep False for compatibility
                socket_connect_timeout=10
            )
            logger.info("Using Redis Cloud", host=host, port=port, username=username)
        
        elif settings.REDIS_URL:
            # Use provided REDIS_URL (for standard Redis)
            self.redis_client = redis.Redis.from_url(
                settings.REDIS_URL,
                decode_responses=False
            )
            logger.info("Using Redis from REDIS_URL", url=settings.REDIS_URL.split("@")[-1] if "@" in settings.REDIS_URL else "local")
        
        else:
            # Fallback to individual settings
            host = settings.REDIS_HOST or "localhost"
            port = settings.REDIS_PORT or 6379
            password = settings.REDIS_PASSWORD
            username = getattr(settings, "REDIS_USERNAME", None)
            
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                password=password,
                username=username,
                decode_responses=False
            )
            logger.info("Using Redis from individual settings", host=host, port=port)
        
        # Test connection
        try:
            self.redis_client.ping()
            logger.info("Redis connection successful")
        except Exception as e:
            logger.error("Redis connection failed", error=str(e))
            raise
    
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
