import redis
from config.setting import settings
import traceback

def test_redis_connection():
    print("Testing Redis connection...")
    print(f"Redis URL: {settings.REDIS_URL}")
    
    try:
        # Create Redis client
        client = redis.from_url(settings.REDIS_URL)
        
        # Test connection
        print("\nTesting connection...")
        client.ping()
        print("Successfully connected to Redis")
        
        # Test basic operations
        print("\nTesting basic operations...")
        test_key = "test_key"
        test_value = "test_value"
        
        # Set value
        print(f"Setting {test_key} = {test_value}")
        client.set(test_key, test_value)
        
        # Get value
        value = client.get(test_key)
        print(f"Getting {test_key} = {value}")
        
        # Delete test key
        print(f"Deleting {test_key}")
        client.delete(test_key)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Full error details:")
        traceback.print_exc()

if __name__ == "__main__":
    test_redis_connection() 