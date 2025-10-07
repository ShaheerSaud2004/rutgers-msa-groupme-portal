#!/usr/bin/env python3
"""
Setup script for GroupMe Portal
This script helps you configure the application and get started.
"""

import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("Creating directories...")
    directories = [
        "static/uploads",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file...")
        env_content = """# GroupMe API Configuration
GROUPME_ACCESS_TOKEN=your_access_token_here

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///groupme_portal.db

# Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=static/uploads
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file")
        print("⚠️  Please update the GROUPME_ACCESS_TOKEN in .env with your actual token")
    else:
        print("✅ .env file already exists")

def check_groupme_setup():
    """Check if GroupMe API token is configured"""
    print("\n🔍 Checking GroupMe API configuration...")
    
    # Try to import and check config
    try:
        from config import Config
        if Config.GROUPME_ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
            print("⚠️  GroupMe API token not configured!")
            print("   Please:")
            print("   1. Go to https://dev.groupme.com/")
            print("   2. Create an application and get your access token")
            print("   3. Update GROUPME_ACCESS_TOKEN in .env file")
            return False
        else:
            print("✅ GroupMe API token is configured")
            return True
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up GroupMe Portal...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation")
        return False
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check GroupMe setup
    groupme_configured = check_groupme_setup()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if not groupme_configured:
        print("\n⚠️  IMPORTANT: You still need to configure your GroupMe API token!")
        print("   1. Get your token from https://dev.groupme.com/")
        print("   2. Update the .env file with your token")
        print("   3. Then run: python app.py")
    else:
        print("\n✅ Ready to start! Run: python app.py")
    
    print("\n📖 For detailed instructions, see README.md")
    return True

if __name__ == "__main__":
    main()
