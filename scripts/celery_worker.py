import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.tasks.celery_tasks import celery_app
    celery_app.worker_main()
