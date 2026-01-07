import os
import sys
from pathlib import Path

# Add app to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file BEFORE importing anything
try:
    from dotenv import load_dotenv
    # Try multiple possible .env file locations
    env_paths = [
        project_root / "config" / ".env",
        project_root / ".env",
        os.getenv("ENV_FILE_PATH")
    ]
    for env_path in env_paths:
        if env_path and Path(env_path).exists():
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from: {env_path}")
            break
    # Also set ENV_FILE_PATH for pydantic settings
    if not os.getenv("ENV_FILE_PATH"):
        env_file = project_root / "config" / ".env"
        if env_file.exists():
            os.environ["ENV_FILE_PATH"] = str(env_file)
except ImportError:
    print("Warning: python-dotenv not installed, using environment variables only")
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

if __name__ == "__main__":
    # Instead of using worker_main(), we'll use the standard celery command
    # But first ensure environment is loaded, then call celery CLI
    import subprocess
    
    # Build celery command
    celery_cmd = ['celery', '-A', 'app.tasks.celery_tasks', 'worker', '--loglevel=info']
    
    # Add any additional arguments
    if len(sys.argv) > 1:
        celery_cmd.extend(sys.argv[1:])
    
    # Execute celery command
    # This ensures proper argument handling
    sys.exit(subprocess.call(celery_cmd))
