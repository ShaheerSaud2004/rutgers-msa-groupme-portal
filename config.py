import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///groupme_portal.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # GroupMe API settings
    GROUPME_ACCESS_TOKEN = os.environ.get('GROUPME_ACCESS_TOKEN') or 'HRsKfLdVUMHZo9wqnCtlBOCo1W8KZfX80rQ9zFLP'
    GROUPME_BASE_URL = 'https://api.groupme.com/v3'
