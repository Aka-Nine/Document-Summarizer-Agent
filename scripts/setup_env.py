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
    config_env_path = Path("config/config.env")
    env_path = Path("config/.env")
    
    if not config_env_path.exists():
        print("❌ config.env file not found!")
        return False
    
    if env_path.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return True
    
    try:
        shutil.copy2(config_env_path, env_path)
        print("✅ Created .env file from config.env template")
        print("📝 Please edit .env file with your actual API keys and configuration")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import boto3
        import langchain
        print("✅ Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please run: pip install -r requirements.txt")
        return False

def verify_structure():
    """Verify the project structure"""
    required_dirs = [
        "app", "config", "docs", "tests", "scripts"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Missing directories: {', '.join(missing_dirs)}")
        return False
    
    print("✅ Project structure is correct")
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up Document Summarizer Agent environment...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Verify project structure
    if not verify_structure():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 To install dependencies, run:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Environment setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your actual API keys")
    print("2. Set up your database (PostgreSQL)")
    print("3. Configure AWS services (S3, SQS, DynamoDB)")
    print("4. Run the application: python run.py")
    print("\n🔧 For testing, run: python -m pytest test/")

if __name__ == "__main__":
    main()
