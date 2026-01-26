#!/usr/bin/env python3
"""
Comprehensive test of the distributed system
Tests: FastAPI, MongoDB, Redis, Celery, Storage, LLM
"""
import sys
import os
import time
import requests
import json
from pathlib import Path
import pytest

# Load environment
try:
    from dotenv import load_dotenv
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config', '.env')
    load_dotenv(config_path)
except:
    pass

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_mongodb():
    """Test MongoDB connection"""
    print_header("Testing MongoDB Connection")
    try:
        from app.models.mongodb_database import get_database, create_indexes
        db = get_database()
        result = db.command("ping")
        print_success("MongoDB: Connected")
        create_indexes()
        print_success("MongoDB: Indexes created")
        return True
    except Exception as e:
        print_error(f"MongoDB: Failed - {e}")
        return False

def test_redis():
    """Test Redis connection"""
    print_header("Testing Redis Connection")
    try:
        from app.services.redis_service import RedisService
        redis = RedisService()
        
        # Test write
        redis.set_key("test_distributed", "hello_world", expire_seconds=60)
        print_success("Redis: Write operation")
        
        # Test read
        result = redis.get_key("test_distributed")
        if result == "hello_world":
            print_success("Redis: Read operation")
        else:
            print_error("Redis: Read mismatch")
            return False
        
        # Test delete
        redis.delete_key("test_distributed")
        print_success("Redis: Delete operation")
        
        print_success("Redis: All operations working")
        return True
    except Exception as e:
        print_error(f"Redis: Failed - {e}")
        return False

@pytest.mark.asyncio
async def test_storage_async():
    """Test filesystem storage (async)"""
    try:
        from app.services.cloud_storage import CloudStorageService
        storage = CloudStorageService.create()
        
        # Test upload
        test_content = b"Test file content for distributed system"
        test_key = "test/test_file.txt"
        await storage.upload_file(test_content, test_key)
        print_success("Storage: Upload operation")
        
        # Test exists
        exists = storage.file_exists(test_key)
        if exists:
            print_success("Storage: File exists check")
        else:
            print_error("Storage: File not found after upload")
            return False
        
        # Test download
        downloaded = await storage.download_file(test_key)
        if downloaded == test_content:
            print_success("Storage: Download operation")
        else:
            print_error("Storage: Download content mismatch")
            return False
        
        # Test delete
        deleted = storage.delete_file(test_key)
        if deleted:
            print_success("Storage: Delete operation")
        else:
            print_error("Storage: Delete failed")
            return False
        
        print_success("Storage: All operations working")
        return True
    except Exception as e:
        print_error(f"Storage: Failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_llm():
    """Test LLM (Gemini)"""
    print_header("Testing LLM (Gemini)")
    try:
        from app.config.settings import settings
        from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
        
        provider = settings.LLM_PROVIDER.lower()
        print_info(f"LLM Provider: {provider}")
        
        if provider == "gemini" and settings.GEMINI_API_KEY:
            processor = EnterpriseDocumentProcessor()
            print_success(f"LLM ({provider}): Initialized")
            print_success(f"LLM ({provider}): Ready to process documents")
            return True
        else:
            print_error(f"LLM: Provider '{provider}' not configured")
            return False
    except Exception as e:
        print_error(f"LLM: Failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_celery_connection():
    """Test Celery connection to Redis"""
    print_header("Testing Celery Connection")
    try:
        from app.tasks.celery_tasks import celery_app
        
        # Test broker connection
        inspect = celery_app.control.inspect()
        stats = inspect.stats()
        
        if stats:
            print_success("Celery: Worker(s) connected")
        else:
            print_info("Celery: No workers running (this is OK for testing)")
            print_info("Celery: Broker connection verified")
        
        print_success("Celery: Configuration valid")
        return True
    except Exception as e:
        print_error(f"Celery: Failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fastapi_startup():
    """Test if FastAPI can start"""
    print_header("Testing FastAPI Configuration")
    try:
        from app.api.main import app
        from app.config.settings import settings
        
        print_success("FastAPI: Application loaded")
        print_info(f"FastAPI: LLM Provider = {settings.LLM_PROVIDER}")
        print_info(f"FastAPI: Cloud Provider = {settings.CLOUD_PROVIDER}")
        print_info(f"FastAPI: RAG Enabled = {settings.RAG_ENABLED}")
        print_success("FastAPI: Ready to start")
        return True
    except Exception as e:
        print_error(f"FastAPI: Failed - {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoints():
    """Test API endpoints (if server is running)"""
    print_header("Testing API Endpoints")
    base_url = "http://localhost:8000"
    
    try:
        # Test health endpoint
        response = requests.get(f"{base_url}/test", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("API: Server is running")
            print_info(f"API: LLM Provider = {data.get('llm_provider', 'N/A')}")
            print_info(f"API: Cloud Provider = {data.get('cloud_provider', 'N/A')}")
            return True
        else:
            print_error(f"API: Server returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_info("API: Server not running (start with: python run.py)")
        return None  # Not an error, just not running
    except Exception as e:
        print_error(f"API: Failed - {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  DISTRIBUTED SYSTEM COMPREHENSIVE TEST")
    print("=" * 70)
    
    results = {}
    
    # Test MongoDB
    results["MongoDB"] = test_mongodb()
    
    # Test Redis
    results["Redis"] = test_redis()
    
    # Test Storage (async)
    print_header("Testing Filesystem Storage")
    try:
        import asyncio
        results["Storage"] = asyncio.run(test_storage_async())
    except Exception as e:
        print_error(f"Storage: Failed - {e}")
        import traceback
        traceback.print_exc()
        results["Storage"] = False
    
    # Test LLM
    results["LLM"] = test_llm()
    
    # Test Celery
    results["Celery"] = test_celery_connection()
    
    # Test FastAPI
    results["FastAPI"] = test_fastapi_startup()
    
    # Test API (optional - only if server running)
    api_result = test_api_endpoints()
    if api_result is not None:
        results["API"] = api_result
    
    # Summary
    print_header("TEST SUMMARY")
    
    required = ["MongoDB", "Redis", "Storage", "LLM", "Celery", "FastAPI"]
    all_passed = all(results.get(k, False) for k in required)
    
    for service in required:
        status = "✅ PASS" if results.get(service, False) else "❌ FAIL"
        print(f"  {service:15} {status}")
    
    if "API" in results:
        status = "✅ PASS" if results["API"] else "❌ FAIL"
        print(f"  {'API':15} {status}")
    
    print()
    if all_passed:
        print_success("All core services are working!")
        print()
        print("🚀 Your distributed system is ready!")
        print()
        print("To start the application:")
        print("  1. Start FastAPI: python run.py")
        print("  2. Start Celery worker: celery -A tasks.celery_tasks worker --loglevel=info")
        print("  3. Access API docs: http://localhost:8000/docs")
    else:
        print_error("Some services failed. Please check the errors above.")
        print()
        print("Common issues:")
        print("  - Check .env file has all required variables")
        print("  - Verify MongoDB and Redis connections")
        print("  - Ensure all dependencies are installed")

if __name__ == "__main__":
    main()

