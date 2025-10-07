#!/usr/bin/env python3
"""
Run script for GroupMe Portal
This script starts the application with proper configuration.
"""

import os
import sys
from pathlib import Path

def check_setup():
    """Check if the application is properly set up"""
    required_files = [
        "app.py",
        "config.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease run setup.py first: python setup.py")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists and has proper configuration"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating default...")
        create_default_env()
    
    # Check if token is configured
    try:
        from config import Config
        if Config.GROUPME_ACCESS_TOKEN == "YOUR_ACCESS_TOKEN_HERE":
            print("⚠️  GroupMe API token not configured!")
            print("   Please update GROUPME_ACCESS_TOKEN in .env file")
            print("   Get your token from: https://dev.groupme.com/")
            return False
    except Exception as e:
        print(f"❌ Error checking configuration: {e}")
        return False
    
    return True

def create_default_env():
    """Create a default .env file"""
    env_content = """# GroupMe API Configuration
GROUPME_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE

# Flask Configuration
SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///groupme_portal.db

# Upload Configuration
MAX_CONTENT_LENGTH=16777216  # 16MB in bytes
UPLOAD_FOLDER=static/uploads
"""
    with open(".env", "w") as f:
        f.write(env_content)
    print("✅ Created default .env file")

def main():
    """Main run function"""
    print("🚀 Starting GroupMe Portal...")
    print("=" * 40)
    
    # Check setup
    if not check_setup():
        return False
    
    # Check environment
    if not check_env_file():
        print("\n❌ Configuration incomplete. Please fix the issues above.")
        return False
    
    # Start the application
    print("✅ Configuration looks good!")
    print("🌐 Starting web server...")
    print("📱 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
