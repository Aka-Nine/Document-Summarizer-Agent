#!/usr/bin/env python3
"""Quick system check with logging"""
import sys
import os
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Create logs directory
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / f"system_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(msg):
    """Log to both console and file"""
    print(msg, flush=True)
    try:
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except:
        pass

log("=" * 70)
log("SYSTEM CHECK - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
log("=" * 70)

# Test imports
log("\n[1] Testing imports...")
try:
    from app.config.settings import settings
    log("  \u2713 Settings imported")
except Exception as e:
    log(f"  \u2717 Settings import failed: {e}")
    sys.exit(1)

try:
    from app.api.main import app
    log("  \u2713 API app imported")
except Exception as e:
    log(f"  \u2717 API import failed: {e}")
    sys.exit(1)

# Test MongoDB
log("\n[2] Testing MongoDB...")
try:
    from app.models.mongodb_database import get_database, create_indexes
    db = get_database()
    db.command("ping")
    create_indexes()
    log("  \u2713 MongoDB connected")
except Exception as e:
    log(f"  \u2717 MongoDB failed: {e}")

# Test Redis
log("\n[3] Testing Redis...")
try:
    from app.services.redis_service import RedisService
    redis = RedisService()
    redis.set_key("test", "ok", expire_seconds=5)
    result = redis.get_key("test")
    redis.delete_key("test")
    if result == "ok":
        log("  \u2713 Redis connected")
    else:
        log("  \u2717 Redis test failed")
except Exception as e:
    log(f"  \u2717 Redis failed: {e}")

# Test Storage
log("\n[4] Testing Storage...")
try:
    from app.services.cloud_storage import CloudStorageService
    storage = CloudStorageService.create()
    log(f"  \u2713 Storage configured: {type(storage).__name__}")
except Exception as e:
    log(f"  \u2717 Storage failed: {e}")

# Test LLM
log("\n[5] Testing LLM...")
try:
    from app.core.enterprise_document_processor import EnterpriseDocumentProcessor
    processor = EnterpriseDocumentProcessor()
    log(f"  \u2713 LLM configured: {settings.LLM_PROVIDER}")
except Exception as e:
    log(f"  \u2717 LLM failed: {e}")

# Test Celery
log("\n[6] Testing Celery...")
try:
    from app.tasks.celery_tasks import app as celery_app
    log("  \u2713 Celery configured")
except Exception as e:
    log(f"  \u2717 Celery failed: {e}")

log("\n" + "=" * 70)
log(f"Check complete. Log saved to: {log_file}")
log("=" * 70)
