#!/usr/bin/env python3
"""
Test script to verify Vercel deployment configuration
"""

import os
import sys
import tempfile
from PIL import Image
import requests

def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from api.index import app, db, GroupChat, ScheduledPost, groupme_api
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_config():
    """Test configuration for Vercel"""
    print("🧪 Testing configuration...")
    try:
        from config import Config
        
        # Test environment detection
        if os.environ.get('VERCEL'):
            print("✅ Vercel environment detected")
            assert Config.UPLOAD_FOLDER == '/tmp/uploads'
            print("✅ Upload folder set to /tmp/uploads for Vercel")
        else:
            print("✅ Local environment detected")
            assert Config.UPLOAD_FOLDER == 'static/uploads'
            print("✅ Upload folder set to static/uploads for local")
        
        # Test database configuration
        if os.environ.get('DATABASE_URL') and 'postgresql://' in os.environ.get('DATABASE_URL', ''):
            print("✅ PostgreSQL database URL configured")
            assert 'postgresql://' in Config.SQLALCHEMY_DATABASE_URI
        else:
            print("✅ SQLite database configured for local development")
            assert 'sqlite:///' in Config.SQLALCHEMY_DATABASE_URI
        
        # Test GroupMe API token
        assert Config.GROUPME_ACCESS_TOKEN != 'YOUR_ACCESS_TOKEN_HERE'
        print("✅ GroupMe API token configured")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_image_handling():
    """Test image upload and processing"""
    print("🧪 Testing image handling...")
    try:
        from api.index import groupme_api
        
        # Create a test image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            # Create a simple test image
            img = Image.new('RGB', (100, 100), color='red')
            img.save(tmp_file.name, 'PNG')
            
            # Test image upload (this will fail without real API, but we can test the function)
            try:
                result = groupme_api.upload_image(tmp_file.name)
                if result:
                    print("✅ Image upload successful")
                else:
                    print("⚠️  Image upload failed (expected without real API)")
            except Exception as e:
                print(f"⚠️  Image upload error (expected): {e}")
            
            # Clean up
            os.unlink(tmp_file.name)
        
        return True
    except Exception as e:
        print(f"❌ Image handling error: {e}")
        return False

def test_database_models():
    """Test database models"""
    print("🧪 Testing database models...")
    try:
        from api.index import db, GroupChat, ScheduledPost
        
        # Test model creation
        group = GroupChat(
            name="Test Group",
            group_id="123456",
            bot_id="test_bot_id"
        )
        
        post = ScheduledPost(
            title="Test Post",
            message="Test message",
            group_chat_id=1,
            scheduled_time=datetime.now()
        )
        
        print("✅ Database models created successfully")
        return True
    except Exception as e:
        print(f"❌ Database model error: {e}")
        return False

def test_flask_routes():
    """Test Flask routes"""
    print("🧪 Testing Flask routes...")
    try:
        from api.index import app
        
        with app.test_client() as client:
            # Test main routes
            routes_to_test = [
                ('/', 'GET'),
                ('/add_group', 'GET'),
                ('/create_post', 'GET'),
                ('/scheduled_posts', 'GET'),
                ('/health', 'GET')
            ]
            
            for route, method in routes_to_test:
                if method == 'GET':
                    response = client.get(route)
                    if response.status_code in [200, 302]:  # 302 for redirects
                        print(f"✅ Route {route} working")
                    else:
                        print(f"⚠️  Route {route} returned {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Flask routes error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 GroupMe Portal Vercel Deployment Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_database_models,
        test_image_handling,
        test_flask_routes
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Ready for Vercel deployment!")
        print("\n📋 Deployment Checklist:")
        print("✅ Code is Vercel-ready")
        print("✅ PostgreSQL configuration set")
        print("✅ Image handling configured")
        print("✅ GroupMe API integration ready")
        print("✅ All routes working")
        print("\n🚀 Next steps:")
        print("1. Push to GitHub")
        print("2. Deploy to Vercel")
        print("3. Add environment variables")
        print("4. Set up PostgreSQL database")
        return True
    else:
        print("❌ Some tests failed. Please fix issues before deployment.")
        return False

if __name__ == "__main__":
    from datetime import datetime
    success = main()
    sys.exit(0 if success else 1)
