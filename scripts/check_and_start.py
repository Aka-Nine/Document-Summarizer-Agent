#!/usr/bin/env python3
"""Check configuration and start server"""
import sys
import os
import traceback

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("\u2713 Environment variables loaded")
except Exception as e:
    print(f"\u26a0 Warning: Could not load .env: {e}")

# Check required environment variables
print("\nChecking required environment variables...")
required_vars = ["SECRET_KEY", "MONGODB_URL"]
missing = []

for var in required_vars:
    value = os.getenv(var)
    if value:
        print(f"  \u2713 {var}: SET")
    else:
        print(f"  \u2717 {var}: MISSING")
        missing.append(var)

if missing:
    print(f"\n\u26a0 Missing required variables: {', '.join(missing)}")
    print("Please check your .env file")
    print("\nYou can create .env from env.example:")
    print("  copy env.example .env")
    print("  # Then edit .env with your values")
else:
    print("\n\u2713 All required variables are set")

# Try to import and start
print("\n" + "="*60)
print("Attempting to start server...")
print("="*60)

try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    import uvicorn
    from app.api.main import app
    
    print("\n\u2713 All imports successful")
    print("\nStarting server on http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Press Ctrl+C to stop\n")
    
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
    print("\n\nServer stopped")
except Exception as e:
    print(f"\n\u2717 Error starting server: {e}")
    traceback.print_exc()
    sys.exit(1)
