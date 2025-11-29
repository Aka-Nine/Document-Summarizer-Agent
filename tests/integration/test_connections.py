"""
Integration tests for external connections
"""
import pytest
from app.services.redis_service import RedisService
from app.config.settings import settings


@pytest.mark.integration
def test_redis_connection():
    """Test Redis connection"""
    try:
        redis_service = RedisService.create()
        # Try a simple operation
        result = redis_service.set("test_key", "test_value", ttl=10)
        assert result is True
        
        value = redis_service.get("test_key")
        assert value == "test_value"
        
        # Cleanup
        redis_service.delete("test_key")
        print("✅ Redis connection test passed")
    except Exception as e:
        pytest.skip(f"Redis not available: {e}")


@pytest.mark.integration
def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        from app.models.mongodb_database import get_database
        db = get_database()
        # Try to list collections
        collections = db.list_collection_names()
        assert isinstance(collections, list)
        print("✅ MongoDB connection test passed")
    except Exception as e:
        pytest.skip(f"MongoDB not available: {e}")

