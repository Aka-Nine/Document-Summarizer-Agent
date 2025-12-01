#!/usr/bin/env python3
"""
Setup environment and run server with clear error messages
"""
import sys
import os
from pathlib import Path

print("=" * 70)
print("FastAPI Server Setup & Start")
print("=" * 70)

# Check for .env file
env_file = Path(".env")
env_example = Path("env.example") or Path("config.env")

if not env_file.exists():
    print("\n\u26a0 .env file not found!")
    if env_example.exists():
        print(f"Found {env_example.name} - you can copy it:")
        print(f"  copy {env_example.name} .env")
        print("  Then edit .env with your actual values")
    print("\nRequired variables:")
    print("  - SECRET_KEY (JWT secret - generate with: openssl rand -hex 32)")
    print("  - MONGODB_URL (MongoDB connection string)")
    print("  - ALLOWED_ORIGINS (JSON array, e.g., [\"*\"] or [\"http://localhost:8080\"])" )
    print("  - ALLOWED_HOSTS (JSON array, e.g., [\"*\"] or [\"localhost\"])" )
    print("\nWould you like to create a minimal .env file? (y/n): ", end="")
    
    # For automated setup, create minimal .env
    create_minimal = True
    if create_minimal:
        print("y (auto)")
        # Create minimal .env
        minimal_env = """# Minimal .env file - UPDATE THESE VALUES!
SECRET_KEY=change-this-to-a-random-secret-key-min-32-chars
MONGODB_URL=mongodb://localhost:27017/docsumm
ALLOWED_ORIGINS=["*"]
ALLOWED_HOSTS=["*"]
CLOUD_PROVIDER=filesystem
FILESYSTEM_STORAGE_PATH=storage
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
REDIS_URL=redis://localhost:6379/0
"""
        with open(".env", "w") as f:
            f.write(minimal_env)
        print("\u2713 Created minimal .env file")
        print("\u26a0 IMPORTANT: Edit .env and add your actual values!")
        print("   Especially: SECRET_KEY, MONGODB_URL, GROQ_API_KEY")
else:
    print("\n\u2713 .env file found")

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("\u2713 Environment variables loaded")
except Exception as e:
    print(f"\u26a0 Warning: {e}")

# Check required variables
print("\nChecking required environment variables...")
required = {
    "SECRET_KEY": os.getenv("SECRET_KEY"),
    "MONGODB_URL": os.getenv("MONGODB_URL"),
    "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS"),
    "ALLOWED_HOSTS": os.getenv("ALLOWED_HOSTS"),
}

missing = [k for k, v in required.items() if not v]

if missing:
    print(f"\n\u274c Missing required variables: {', '.join(missing)}")
    print("\nPlease set these in your .env file and try again.")
    sys.exit(1)
else:
    print("\n\u2713 All required variables are set")

# Try to start server
print("\n" + "=" * 70)
print("Starting FastAPI Server")
print("=" * 70)
print("\nServer will be available at:")
print("  - API: http://localhost:8000")
print("  - Docs: http://localhost:8000/docs")
print("  - Frontend: http://localhost:8000/frontend")
print("\nPress Ctrl+C to stop the server")
print("=" * 70)
print()

if __name__ == "__main__":
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import uvicorn
        import platform
        
        # On Windows, disable reload to avoid multiprocessing issues
        # Use watchfiles for better Windows support if available
        use_reload = platform.system() != "Windows"
        
        if use_reload:
            print("  (Auto-reload enabled)")
        else:
            print("  (Auto-reload disabled on Windows - restart manually to see changes)")
        
        uvicorn.run(
            "app.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=use_reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n\u2713 Server stopped")
    except Exception as e:
        print(f"\n\n\u274c Error starting server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
