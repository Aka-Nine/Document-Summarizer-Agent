import os
import sys

# Ensure app package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    from app.tasks.celery_tasks import celery_app
    celery_app.worker_main()
