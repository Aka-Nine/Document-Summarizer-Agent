import os
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    # Try multiple possible .env file locations
    env_paths = [
        Path(__file__).parent / "config" / ".env",
        Path(__file__).parent / ".env",
        os.getenv("ENV_FILE_PATH")
    ]
    for env_path in env_paths:
        if env_path and Path(env_path).exists():
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from: {env_path}")
            break
    # Also set ENV_FILE_PATH for pydantic settings
    if not os.getenv("ENV_FILE_PATH"):
        env_file = Path(__file__).parent / "config" / ".env"
        if env_file.exists():
            os.environ["ENV_FILE_PATH"] = str(env_file)
except ImportError:
    print("Warning: python-dotenv not installed, using environment variables only")
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api.main:app", host="0.0.0.0", port=8000, reload=True)
