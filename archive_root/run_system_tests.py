#!/usr/bin/env python3
"""
+System Test Runner with Comprehensive Logging
+
+Tests all distributed system components
+
+"""
+import sys
+import os
+import traceback
+from datetime import datetime
+from pathlib import Path
+import json
+
+# Ensure UTF-8 output
+if hasattr(sys.stdout, 'reconfigure'):
+    sys.stdout.reconfigure(encoding='utf-8')
+
+# Setup
+logs_dir = Path("logs")
+logs_dir.mkdir(exist_ok=True)
+timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
+log_file = logs_dir / f"system_test_{timestamp}.log"
+results_file = logs_dir / f"test_results_{timestamp}.json"
+
+results = {
+    "timestamp": datetime.now().isoformat(),
+    "tests": {}
+}
+
+def write_log(msg, level="INFO"):
+    """Write to both console and log file"""
+    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
+    log_msg = f"[{timestamp_str}] [{level}] {msg}"
+    print(log_msg, flush=True)
+    try:
+        with open(log_file, "a", encoding="utf-8") as f:
+            f.write(log_msg + "\n")
+            f.flush()
+    except Exception as e:
+        print(f"Log write error: {e}", flush=True)
+
+def test_component(name, test_func):
+    """Run a test and record results"""
+    write_log(f"\n{'='*60}")
+    write_log(f"Testing: {name}")
+    write_log(f"{'='*60}")
+    try:
+        result = test_func()
+        if result.get("status") == "success":
+            write_log(f"\u2705 {name}: PASSED", "SUCCESS")
+        else:
+            write_log(f"\u26a0\ufe0f  {name}: {result.get('message', 'WARNING')}", "WARNING")
+        results["tests"][name] = result
+        return result
+    except Exception as e:
+        error_msg = f"{name} failed: {str(e)}"
+        write_log(f"\u274c {error_msg}", "ERROR")
+        write_log(traceback.format_exc(), "ERROR")
+        results["tests"][name] = {
+            "status": "error",
+            "message": error_msg,
+            "error": str(e),
+            "traceback": traceback.format_exc()
+        }
+        return results["tests"][name]
+
+def main():
+    """Main test runner"""
+    write_log("="*60)
+    write_log("DISTRIBUTED SYSTEM TEST SUITE")
+    write_log("="*60)
+    write_log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
+    write_log(f"Log file: {log_file}")
+    
#!/usr/bin/env python3
"""
System Test Runner with Comprehensive Logging

Tests all distributed system components

"""
import sys
import os
import traceback
from datetime import datetime
from pathlib import Path
import json

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
	sys.stdout.reconfigure(encoding='utf-8')

# Setup
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = logs_dir / f"system_test_{timestamp}.log"
results_file = logs_dir / f"test_results_{timestamp}.json"

results = {
	"timestamp": datetime.now().isoformat(),
	"tests": {}
}

def write_log(msg, level="INFO"):
	"""Write to both console and log file"""
	timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	log_msg = f"[{timestamp_str}] [{level}] {msg}"
	print(log_msg, flush=True)
	try:
		with open(log_file, "a", encoding="utf-8") as f:
			f.write(log_msg + "\n")
			f.flush()
	except Exception as e:
		print(f"Log write error: {e}", flush=True)

def test_component(name, test_func):
	"""Run a test and record results"""
	write_log(f"\n{'='*60}")
	write_log(f"Testing: {name}")
	write_log(f"{'='*60}")
	try:
		result = test_func()
		if result.get("status") == "success":
			write_log(f"\u2705 {name}: PASSED", "SUCCESS")
		else:
			write_log(f"\u26a0\ufe0f  {name}: {result.get('message', 'WARNING')}", "WARNING")
		results["tests"][name] = result
		return result
	except Exception as e:
		error_msg = f"{name} failed: {str(e)}"
		write_log(f"\u274c {error_msg}", "ERROR")
		write_log(traceback.format_exc(), "ERROR")
		results["tests"][name] = {
			"status": "error",
			"message": error_msg,
			"error": str(e),
			"traceback": traceback.format_exc()
		}
		return results["tests"][name]

def main():
	"""Main test runner"""
	write_log("="*60)
	write_log("DISTRIBUTED SYSTEM TEST SUITE")
	write_log("="*60)
	write_log(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	write_log(f"Log file: {log_file}")
    
	# Load environment
	try:
		from dotenv import load_dotenv
		load_dotenv()
		write_log("Environment variables loaded")
	except:
		write_log("Warning: Could not load .env file", "WARNING")
    
	# Test 1: Imports
	def test_imports():
		write_log("Checking critical imports...")
		imports = [
			"app.config.settings",
			"app.models.mongodb_database",
			"app.services.redis_service",
			"app.services.cloud_storage",
			"app.core.enterprise_document_processor",
			"app.tasks.celery_tasks",
			"app.api.main"
		]
		failed = []
		for imp in imports:
			try:
				__import__(imp)
				write_log(f"  \u2713 {imp}")
			except Exception as e:
				write_log(f"  \u2717 {imp}: {e}", "ERROR")
				failed.append(imp)
        
		if failed:
			return {"status": "error", "message": f"Failed imports: {', '.join(failed)}"}
		return {"status": "success", "message": "All imports successful"}
    
	# Test 2: MongoDB
	def test_mongodb():
		from app.models.mongodb_database import get_database, create_indexes
		db = get_database()
		db.command("ping")
		create_indexes()
		return {"status": "success", "message": "MongoDB connected"}
    
	# Test 3: Redis
	def test_redis():
		from app.services.redis_service import RedisService
		redis = RedisService()
		redis.set_key("test_system", "ok", expire_seconds=5)
		result = redis.get_key("test_system")
		redis.delete_key("test_system")
		if result == "ok":
			return {"status": "success", "message": "Redis connected"}
		else:
			return {"status": "error", "message": "Redis test failed"}
    
	# Test 4: Storage
	def test_storage():
		from app.services.cloud_storage import CloudStorageService
		storage = CloudStorageService.create()
		return {"status": "success", "message": f"Storage: {type(storage).__name__}"}
    
	# Test 5: LLM
	def test_llm():
		from app.config.settings import settings
		from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
		processor = EnterpriseDocumentProcessor()
		return {"status": "success", "message": f"LLM: {settings.LLM_PROVIDER}"}
    
	# Test 6: Celery
	def test_celery():
		from app.tasks.celery_tasks import app as celery_app
		return {"status": "success", "message": "Celery configured"}
    
	# Test 7: API
	def test_api():
		from app.api.main import app
		return {"status": "success", "message": "FastAPI app ready"}
    
	# Run all tests
	test_component("Imports", test_imports)
	test_component("MongoDB", test_mongodb)
	test_component("Redis", test_redis)
	test_component("Storage", test_storage)
	test_component("LLM", test_llm)
	test_component("Celery", test_celery)
	test_component("API", test_api)
    
	# Summary
	write_log("\n" + "="*60)
	write_log("TEST SUMMARY")
	write_log("="*60)
    
	total = len(results["tests"])
	passed = sum(1 for r in results["tests"].values() if r.get("status") == "success")
	failed = sum(1 for r in results["tests"].values() if r.get("status") == "error")
    
	write_log(f"Total Tests: {total}")
	write_log(f"\u2705 Passed: {passed}")
	write_log(f"\u274c Failed: {failed}")
    
	# Save results
	with open(results_file, "w", encoding="utf-8") as f:
		json.dump(results, f, indent=2, default=str)
    
	write_log(f"\nResults saved to: {results_file}")
	write_log(f"Full log: {log_file}")
	write_log("="*60)
    
	return 0 if failed == 0 else 1

if __name__ == "__main__":
	try:
		sys.exit(main())
	except KeyboardInterrupt:
		write_log("Interrupted by user", "WARNING")
		sys.exit(1)
	except Exception as e:
		write_log(f"Fatal error: {e}", "ERROR")
		write_log(traceback.format_exc(), "ERROR")
		sys.exit(1)