#!/usr/bin/env python3
"""
Test script to verify Document Summarizer Agent setup
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config.setting import settings
        print("✅ Settings imported successfully")
    except Exception as e:
        print(f"❌ Failed to import settings: {e}")
        return False
    
    try:
        from models.database import SessionLocal, User, Document, ProcessingStatus
        print("✅ Database models imported successfully")
    except Exception as e:
        print(f"❌ Failed to import database models: {e}")
        return False
    
    try:
        from services.storage_service import StorageService
        print("✅ Storage service imported successfully")
    except Exception as e:
        print(f"❌ Failed to import storage service: {e}")
        return False
    
    try:
        from core.document_processor import DocumentProcessor
        print("✅ Document processor imported successfully")
    except Exception as e:
        print(f"❌ Failed to import document processor: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration loading"""
    print("\n🔧 Testing configuration...")
    
    try:
        from config.setting import settings
        
        # Check if required settings are defined
        required_settings = [
            'SECRET_KEY', 'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
            'S3_BUCKET_NAME', 'DATABASE_URL', 'GROQ_API_KEY'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not hasattr(settings, setting) or getattr(settings, setting) == f"your_{setting.lower()}_here":
                missing_settings.append(setting)
        
        if missing_settings:
            print(f"⚠️  Missing or default settings: {', '.join(missing_settings)}")
            print("   Please update your .env file with actual values")
        else:
            print("✅ All required settings are configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️  Testing database connection...")
    
    try:
        from models.database import SessionLocal, create_tables
        
        # Try to create tables
        create_tables()
        print("✅ Database tables created/verified successfully")
        
        # Try to create a session
        db = SessionLocal()
        db.close()
        print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Please check your DATABASE_URL in .env file")
        return False

def test_aws_services():
    """Test AWS services configuration"""
    print("\n☁️  Testing AWS services...")
    
    try:
        from services.storage_service import StorageService
        from services.aws_cache_service import get_aws_cache_service
        from services.aws_task_service import AWSTaskService
        
        print("✅ AWS services imported successfully")
        
        # Do not instantiate cache or task service here to avoid credential failures
        print("ℹ️  Skipping AWS live calls; will validate at /health")
        
        return True
    except Exception as e:
        print(f"❌ AWS services test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API endpoints...")
    
    try:
        from api.main import app
        print("✅ FastAPI app created successfully")
        
        # Check if app has required endpoints
        routes = [route.path for route in app.routes]
        required_routes = ['/health', '/register', '/login', '/upload', '/documents']
        
        missing_routes = []
        for route in required_routes:
            if not any(route in r for r in routes):
                missing_routes.append(route)
        
        if missing_routes:
            print(f"⚠️  Missing routes: {', '.join(missing_routes)}")
        else:
            print("✅ All required API endpoints are available")
        
        return True
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Document Summarizer Agent setup...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_database_connection,
        test_aws_services,
        test_api_endpoints
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\n🚀 To start the application, run:")
        print("   python run.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 Common fixes:")
        print("1. Make sure .env file exists and has correct values")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Set up your database and AWS services")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
