#!/usr/bin/env python3
"""
Start server with error handling and diagnostics
"""
import sys
import os
import traceback

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Starting FastAPI Server")
print("=" * 60)

# Check dependencies
print("\n[1] Checking dependencies...")
try:
    import uvicorn
    print(f"  \u2713 uvicorn {uvicorn.__version__}")
except ImportError as e:
    print(f"  \u2717 uvicorn not found: {e}")
    sys.exit(1)

try:
    import fastapi
    print(f"  \u2713 fastapi {fastapi.__version__}")
except ImportError as e:
    print(f"  \u2717 fastapi not found: {e}")
    sys.exit(1)

# Test imports
print("\n[2] Testing imports...")
try:
    from app.config.settings import settings
    print("  \u2713 Settings imported")
except Exception as e:
    print(f"  \u2717 Settings import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

try:
    from app.api.main import app
    print("  \u2713 FastAPI app imported")
except Exception as e:
    print(f"  \u2717 App import failed: {e}")
    traceback.print_exc()
    sys.exit(1)

# Start server
print("\n[3] Starting server...")
print("  Server will be available at: http://localhost:8000")
print("  API Docs: http://localhost:8000/docs")
print("  Press Ctrl+C to stop")
print("=" * 60)
print()

if __name__ == "__main__":
    try:
        import platform
        # On Windows, disable reload to avoid multiprocessing issues
        use_reload = platform.system() != "Windows"
        
        uvicorn.run(
            "app.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=use_reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n\n\u2717 Server failed to start: {e}")
        traceback.print_exc()
        sys.exit(1)
