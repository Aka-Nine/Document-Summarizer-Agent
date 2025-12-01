#!/usr/bin/env python3
"""
Comprehensive Distributed System Test Suite
Tests all components and logs results
"""
import sys
import os
import traceback
from datetime import datetime
from pathlib import Path
import json

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Log file
log_file = logs_dir / f"system_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(message, level="INFO"):
    """Log message to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry, flush=True)
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
            f.flush()
    except Exception as e:
        print(f"Warning: Could not write to log file: {e}", flush=True)

def test_mongodb():
    """Test MongoDB connection"""
    log("Testing MongoDB connection...")
    try:
        from app.models.mongodb_database import get_database, create_indexes
        db = get_database()
        db.command("ping")
        create_indexes()
        log("\u2705 MongoDB: Connected and indexes created", "SUCCESS")
        return {"status": "success", "message": "MongoDB connected"}
    except Exception as e:
        error_msg = f"MongoDB connection failed: {str(e)}"
        log(f"\u274c {error_msg}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return {"status": "error", "message": error_msg, "error": str(e)}

def test_redis():
    """Test Redis connection"""
    log("Testing Redis connection...")
    try:
        from app.services.redis_service import RedisService
        redis = RedisService()
        test_key = "test_distributed_system"
        redis.set_key(test_key, "hello", expire_seconds=10)
        result = redis.get_key(test_key)
        redis.delete_key(test_key)
        if result == "hello":
            log("\u2705 Redis: Connected and working", "SUCCESS")
            return {"status": "success", "message": "Redis connected"}
        else:
            error_msg = "Redis connection test failed - value mismatch"
            log(f"\u274c {error_msg}", "ERROR")
            return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Redis connection failed: {str(e)}"
        log(f"\u274c {error_msg}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return {"status": "error", "message": error_msg, "error": str(e)}

def test_storage():
    """Test cloud storage"""
    log("Testing Cloud Storage...")
    try:
        from app.services.cloud_storage import CloudStorageService
        storage = CloudStorageService.create()
        log(f"\u2705 Cloud Storage: Configured ({type(storage).__name__})", "SUCCESS")
        return {"status": "success", "message": f"Storage configured: {type(storage).__name__}"}
    except Exception as e:
        error_msg = f"Cloud Storage failed: {str(e)}"
        log(f"\u274c {error_msg}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return {"status": "error", "message": error_msg, "error": str(e)}

def test_llm():
    """Test LLM configuration"""
    log("Testing LLM configuration...")
    try:
        from app.config.settings import settings
        from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
        
        provider = settings.LLM_PROVIDER.lower()
        if provider == "groq" and settings.GROQ_API_KEY:
            processor = EnterpriseDocumentProcessor()
            log(f"\u2705 LLM ({provider}): Configured", "SUCCESS")
            return {"status": "success", "message": f"LLM ({provider}) configured"}
        elif provider == "gemini" and settings.GEMINI_API_KEY:
            processor = EnterpriseDocumentProcessor()
            log(f"\u2705 LLM ({provider}): Configured", "SUCCESS")
            return {"status": "success", "message": f"LLM ({provider}) configured"}
        else:
            error_msg = f"LLM provider '{provider}' not fully configured"
            log(f"\u26a0\ufe0f  {error_msg}", "WARNING")
            return {"status": "warning", "message": error_msg}
    except Exception as e:
        error_msg = f"LLM configuration failed: {str(e)}"
        log(f"\u274c {error_msg}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return {"status": "error", "message": error_msg, "error": str(e)}

def test_rag():
    """Test RAG configuration"""
    log("Testing RAG configuration...")
    try:
        from app.config.settings import settings
        if not settings.RAG_ENABLED:
            log("\u2139\ufe0f  RAG: Disabled (optional)", "INFO")
            return {"status": "skipped", "message": "RAG is disabled"}
        
        from app.services.vector_db_service import VectorDBService
        from app.services.embeddings_service import EmbeddingsService
        
        vector_db = VectorDBService.create()
        embeddings = EmbeddingsService.create()
        log("\u2705 RAG: Configured", "SUCCESS")
        return {"status": "success", "message": "RAG configured"}
    except Exception as e:
        error_msg = f"RAG configuration failed: {str(e)}"
        log(f"\u26a0\ufe0f  {error_msg} (RAG is optional)", "WARNING")
        return {"status": "warning", "message": error_msg, "error": str(e)}

def test_celery():
    """Test Celery configuration"""
    log("Testing Celery configuration...")
    try:
        from app.tasks.celery_tasks import app as celery_app
        from app.config.settings import settings
        
        # Check if Celery app is configured
        if celery_app:
            log("\u2705 Celery: App configured", "SUCCESS")
            return {"status": "success", "message": "Celery app configured"}
        else:
            error_msg = "Celery app not configured"
            log(f"\u274c {error_msg}", "ERROR")
            return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"Celery configuration failed: {str(e)}"
        log(f"\u274c {error_msg}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return {"status": "error", "message": error_msg, "error": str(e)}

def test_api():
    """Test API imports and configuration"""
    log("Testing API configuration...")
    try:
        from app.api.main import app
        from app.config.settings import settings
        
        if app:
            log("\u2705 API: FastAPI app configured", "SUCCESS")
            return {"status": "success", "message": "FastAPI app configured"}
        else:
            error_msg = "FastAPI app not configured"
            log(f"\u274c {error_msg}", "ERROR")
            return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"API configuration failed: {str(e)}"
        log(f"\u274c {error_msg}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        return {"status": "error", "message": error_msg, "error": str(e)}

def test_imports():
    """Test all critical imports"""
    log("Testing critical imports...")
    imports_to_test = [
        ("app.config.settings", "settings"),
        ("app.models.mongodb_database", "get_database"),
        ("app.services.redis_service", "RedisService"),
        ("app.services.cloud_storage", "CloudStorageService"),
        ("app.core.enterprise_document_processor", "EnterpriseDocumentProcessor"),
        ("app.tasks.celery_tasks", "app"),
    ]
    
    results = []
    for module_name, item_name in imports_to_test:
        try:
            module = __import__(module_name, fromlist=[item_name])
            getattr(module, item_name)
            log(f"\u2705 Import: {module_name}.{item_name}", "SUCCESS")
            results.append({"module": module_name, "item": item_name, "status": "success"})
        except Exception as e:
            error_msg = f"Import failed: {module_name}.{item_name} - {str(e)}"
            log(f"\u274c {error_msg}", "ERROR")
            results.append({"module": module_name, "item": item_name, "status": "error", "error": str(e)})
    
    if all(r["status"] == "success" for r in results):
        return {"status": "success", "message": "All imports successful", "details": results}
    else:
        failed = [r for r in results if r["status"] != "success"]
        return {"status": "error", "message": f"{len(failed)} imports failed", "details": results}

def main():
    """Run all tests"""
    log("=" * 80)
    log("DISTRIBUTED SYSTEM TEST SUITE")
    log("=" * 80)
    log(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Log file: {log_file}")
    log("")
    
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {}
    }
    
    # Run all tests
    test_results["tests"]["imports"] = test_imports()
    log("")
    
    test_results["tests"]["api"] = test_api()
    log("")
    
    test_results["tests"]["mongodb"] = test_mongodb()
    log("")
    
    test_results["tests"]["redis"] = test_redis()
    log("")
    
    test_results["tests"]["storage"] = test_storage()
    log("")
    
    test_results["tests"]["llm"] = test_llm()
    log("")
    
    test_results["tests"]["rag"] = test_rag()
    log("")
    
    test_results["tests"]["celery"] = test_celery()
    log("")
    
    # Summary
    log("=" * 80)
    log("TEST SUMMARY")
    log("=" * 80)
    
    required_tests = ["mongodb", "redis", "storage", "llm", "api"]
    optional_tests = ["rag"]
    
    required_results = [test_results["tests"][t] for t in required_tests if t in test_results["tests"]]
    optional_results = [test_results["tests"][t] for t in optional_tests if t in test_results["tests"]]
    
    required_passed = all(r.get("status") == "success" for r in required_results)
    optional_passed = all(r.get("status") in ["success", "skipped", "warning"] for r in optional_results)
    
    # Count results
    success_count = sum(1 for r in test_results["tests"].values() if r.get("status") == "success")
    error_count = sum(1 for r in test_results["tests"].values() if r.get("status") == "error")
    warning_count = sum(1 for r in test_results["tests"].values() if r.get("status") in ["warning", "skipped"])
    
    log(f"Total Tests: {len(test_results['tests'])}")
    log(f"\u2705 Passed: {success_count}")
    log(f"\u274c Failed: {error_count}")
    log(f"\u26a0\ufe0f  Warnings/Skipped: {warning_count}")
    log("")
    
    if required_passed:
        log("\u2705 All required services are ready!", "SUCCESS")
        if not optional_passed:
            log("\u2139\ufe0f  Some optional services (RAG) are not configured", "INFO")
        log("")
        log("\ud83d\ude80 System is ready to run:")
        log("   python run.py")
        log("   celery -A app.tasks.celery_tasks worker --loglevel=info")
    else:
        log("\u274c Some required services failed", "ERROR")
        log("")
        log("Failed services:")
        for test_name in required_tests:
            if test_name in test_results["tests"]:
                result = test_results["tests"][test_name]
                if result.get("status") != "success":
                    log(f"  - {test_name}: {result.get('message', 'Unknown error')}", "ERROR")
        log("")
        log("Please check your .env file and configuration")
    
    # Save results to JSON
    results_file = logs_dir / f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_file, "w", encoding="utf-8") as f:
        json.dump(test_results, f, indent=2, default=str)
    
    log(f"")
    log(f"Results saved to: {results_file}")
    log(f"Full log saved to: {log_file}")
    log("=" * 80)
    
    return 0 if required_passed else 1
 
if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        log("Test interrupted by user", "WARNING")
        sys.exit(1)
    except Exception as e:
        log(f"Fatal error: {str(e)}", "ERROR")
        log(f"Traceback: {traceback.format_exc()}", "ERROR")
        sys.exit(1)
