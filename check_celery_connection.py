"""
Diagnostic script to check Celery connection and task registration
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
env_file = os.getenv("ENV_FILE_PATH", "config/.env")
if os.path.exists(env_file):
    load_dotenv(env_file, override=True)
    print(f"[OK] Loaded environment from: {env_file}")
else:
    print(f"⚠️  Environment file not found: {env_file}")

# Now import Celery
try:
    from app.tasks.celery_tasks import celery_app, process_document_task
    from app.config.settings import settings
    import redis
    
    print("\n" + "="*60)
    print("CELERY DIAGNOSTICS")
    print("="*60)
    
    # Check Redis connection
    print("\n1. Redis Connection Check:")
    try:
        celery_redis_url = celery_app.conf.broker_url
        print(f"   Broker URL: {celery_redis_url[:50]}...")
        
        # Parse Redis URL
        if celery_redis_url.startswith("redis://"):
            # Extract connection details
            url_parts = celery_redis_url.replace("redis://", "").split("@")
            if len(url_parts) == 2:
                auth, host_port = url_parts
                host, port = host_port.split(":")
                password = auth.split(":")[-1] if ":" in auth else None
            else:
                host_port = url_parts[0]
                host, port = host_port.split(":")
                password = None
            
            # Test connection
            r = redis.Redis(
                host=host,
                port=int(port),
                password=password,
                decode_responses=False,
                socket_connect_timeout=5
            )
            r.ping()
            print("   [OK] Redis connection successful")
            
            # Check if Celery keys exist
            keys = r.keys("celery*")
            print(f"   Celery keys in Redis: {len(keys)}")
            if keys:
                print(f"   Sample keys: {keys[:5]}")
        else:
            print(f"   [WARN] Using non-Redis broker: {celery_redis_url}")
    except Exception as e:
        print(f"   [ERROR] Redis connection failed: {e}")
    
    # Check Celery app configuration
    print("\n2. Celery App Configuration:")
    print(f"   App name: {celery_app.main}")
    print(f"   Broker: {celery_app.conf.broker_url}")
    print(f"   Backend: {celery_app.conf.result_backend}")
    print(f"   Task serializer: {celery_app.conf.task_serializer}")
    print(f"   Result serializer: {celery_app.conf.result_serializer}")
    print(f"   Worker pool: {celery_app.conf.worker_pool}")
    
    # Check registered tasks
    print("\n3. Registered Tasks:")
    registered_tasks = list(celery_app.tasks.keys())
    print(f"   Total tasks: {len(registered_tasks)}")
    for task_name in registered_tasks:
        if not task_name.startswith("celery."):
            print(f"   [OK] {task_name}")
    
    # Check if our task is registered
    print("\n4. Task Registration Check:")
    task_names = [
        "process_document_task",
        "app.tasks.celery_tasks.process_document_task",
        "enterprise_document_processor.process_document_task"
    ]
    for task_name in task_names:
        if task_name in registered_tasks:
            print(f"   [OK] Task found: {task_name}")
        else:
            print(f"   [ERROR] Task NOT found: {task_name}")
    
    # Check task import
    print("\n5. Task Import Check:")
    try:
        from app.tasks.celery_tasks import process_document_task, query_document_task
        print(f"   [OK] process_document_task imported: {process_document_task}")
        print(f"   [OK] query_document_task imported: {query_document_task}")
        print(f"   Task name: {process_document_task.name}")
        print(f"   Task registered: {process_document_task.name in registered_tasks}")
    except Exception as e:
        print(f"   [ERROR] Task import failed: {e}")
    
    # Test task queuing (dry run)
    print("\n6. Task Queuing Test:")
    try:
        # Don't actually queue, just check if we can create the task
        print("   Testing task creation (not actually queuing)...")
        task_info = {
            "name": process_document_task.name,
            "args": ["test_document_id"],
            "kwargs": {}
        }
        print(f"   [OK] Task can be created: {task_info}")
    except Exception as e:
        print(f"   [ERROR] Task creation failed: {e}")
    
    # Check worker connection (if worker is running)
    print("\n7. Worker Connection Check:")
    try:
        inspect = celery_app.control.inspect()
        active_workers = inspect.active()
        if active_workers:
            print(f"   [OK] Active workers: {len(active_workers)}")
            for worker_name, tasks in active_workers.items():
                print(f"      Worker: {worker_name}")
                print(f"      Active tasks: {len(tasks)}")
        else:
            print("   [WARN] No active workers found")
            print("   💡 Start worker with: celery -A app.tasks.celery_tasks worker --loglevel=info --pool=solo")
    except Exception as e:
        print(f"   [WARN] Could not inspect workers (worker may not be running): {e}")
    
    # Check scheduled tasks
    print("\n8. Scheduled Tasks Check:")
    try:
        inspect = celery_app.control.inspect()
        scheduled = inspect.scheduled()
        if scheduled:
            print(f"   [WARN] Scheduled tasks found: {scheduled}")
        else:
            print("   [OK] No scheduled tasks (normal if no tasks queued)")
    except Exception as e:
        print(f"   [WARN] Could not check scheduled tasks: {e}")
    
    # Check reserved tasks
    print("\n9. Reserved Tasks Check:")
    try:
        inspect = celery_app.control.inspect()
        reserved = inspect.reserved()
        if reserved:
            print(f"   [WARN] Reserved tasks found: {reserved}")
        else:
            print("   [OK] No reserved tasks")
    except Exception as e:
        print(f"   [WARN] Could not check reserved tasks: {e}")
    
    print("\n" + "="*60)
    print("DIAGNOSTICS COMPLETE")
    print("="*60)
    
except Exception as e:
    print(f"\n[ERROR] Error during diagnostics: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

