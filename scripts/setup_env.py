#!/usr/bin/env python3
"""
Environment setup script for Document Summarizer Agent
This script helps set up the environment and verify the configuration
"""

import os
import sys
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from config.env template"""
    config_env_path = Path("config.env")
    env_path = Path(".env")
    
    if not config_env_path.exists():
        print("\u274c config.env file not found!")
        return False
    
    if env_path.exists():
        print("\u26a0\ufe0f  .env file already exists. Skipping creation.")
        return True
    
    try:
        shutil.copy2(config_env_path, env_path)
        print("\u2705 Created .env file from config.env template")
        print("\ud83d\udcdd Please edit .env file with your actual API keys and configuration")
        return True
    except Exception as e:
        print(f"\u274c Failed to create .env file: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("\u274c Python 3.8 or higher is required")
        return False
    print(f"\u2705 Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import boto3
        import langchain
        print("\u2705 Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"\u274c Missing dependency: {e}")
        print("\ud83d\udce6 Please run: pip install -r requirements.txt")
        return False

def verify_structure():
    """Verify the project structure"""
    required_dirs = [
        "api", "config", "core", "models", "services", "tasks", "test"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"\u274c Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("\u2705 Project structure is correct")
    return True

def main():
    """Main setup function"""
    print("\ud83d\ude80 Setting up Document Summarizer Agent environment...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Verify project structure
    if not verify_structure():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n\ud83d\udce6 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("\u2705 Environment setup completed successfully!")
    print("\n\ud83d\udccb Next steps:")
    print("1. Edit .env file with your actual API keys")
    print("2. Set up your database (PostgreSQL)")
    print("3. Configure AWS services (S3, SQS, DynamoDB)")
    print("4. Run the application: python run.py")
    print("\n\ud83d\udd27 For testing, run: python -m pytest test/")

if __name__ == "__main__":
    main()
