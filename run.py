import os
import sys

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
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
