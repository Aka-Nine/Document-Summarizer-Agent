#!/usr/bin/env python3
"""
Test all connections and configurations
"""
import sys
import os

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

def test_mongodb():
    """Test MongoDB connection"""
    try:
        from app.models.mongodb_database import get_database, create_indexes
        db = get_database()
        db.command("ping")
        print("\u2705 MongoDB: Connected")
        create_indexes()
        return True
    except Exception as e:
        print(f"\u274c MongoDB: Failed - {e}")
        return False

def test_redis():
    """Test Redis connection"""
    try:
        from app.services.redis_service import RedisService
        redis = RedisService()
        redis.set_key("test_setup", "hello")
        result = redis.get_key("test_setup")
        redis.delete_key("test_setup")
        if result == "hello":
            print("\u2705 Redis: Connected")
            return True
        else:
            print("\u274c Redis: Connection test failed")
            return False
    except Exception as e:
        print(f"\u274c Redis: Failed - {e}")
        return False

def test_llm():
    """Test LLM configuration"""
    try:
        from app.config.settings import settings
        from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
        
        provider = settings.LLM_PROVIDER.lower()
        if provider == "groq" and settings.GROQ_API_KEY:
            processor = EnterpriseDocumentProcessor()
            print(f"\u2705 LLM ({provider}): Configured")
            return True
        elif provider == "gemini" and settings.GEMINI_API_KEY:
            processor = EnterpriseDocumentProcessor()
            print(f"\u2705 LLM ({provider}): Configured")
            return True
        else:
            print(f"\u26a0\ufe0f  LLM: Provider '{provider}' not fully configured")
            return False
    except Exception as e:
        print(f"\u274c LLM: Failed - {e}")
        return False

def test_storage():
    """Test cloud storage"""
    try:
        from app.services.cloud_storage import CloudStorageService
        storage = CloudStorageService.create()
        print("\u2705 Cloud Storage: Configured")
        return True
    except Exception as e:
        print(f"\u274c Cloud Storage: Failed - {e}")
        print("   \u26a0\ufe0f  You need to configure cloud storage (AWS S3 or MinIO)")
        return False

def test_rag():
    """Test RAG configuration (optional)"""
    try:
        from app.config.settings import settings
        if not settings.RAG_ENABLED:
            print("\u2139\ufe0f  RAG: Disabled (optional)")
            return True
        
        from app.services.vector_db_service import VectorDBService
        from app.services.embeddings_service import EmbeddingsService
        
        vector_db = VectorDBService.create()
        embeddings = EmbeddingsService.create()
        print("\u2705 RAG: Configured")
        return True
    except Exception as e:
        print(f"\u26a0\ufe0f  RAG: Not configured - {e}")
        print("   \u2139\ufe0f  RAG is optional, you can disable it with RAG_ENABLED=false")
        return True  # RAG is optional

def main():
    """Run all tests"""
    print("=" * 60)
    print("SYSTEM CONNECTION TEST")
    print("=" * 60)
    print()
    
    results = {
        "MongoDB": test_mongodb(),
        "Redis": test_redis(),
        "LLM": test_llm(),
        "Cloud Storage": test_storage(),
        "RAG": test_rag()
    }
    
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    required = ["MongoDB", "Redis", "LLM", "Cloud Storage"]
    optional = ["RAG"]
    
    required_ok = all(results[k] for k in required)
    optional_ok = results.get("RAG", True)
    
    if required_ok:
        print("\u2705 All required services are ready!")
        if not optional_ok:
            print("\u2139\ufe0f  RAG is optional and not configured")
        print()
        print("\ud83d\ude80 You can start the application:")
        print("   python run.py")
    else:
        print("\u274c Some required services are not configured")
        print()
        print("Missing:")
        for service in required:
            if not results[service]:
                print(f"  - {service}")
        print()
        print("Please check your .env file and configuration")

if __name__ == "__main__":
    main()
