import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    AI_MODEL_ID = os.getenv('AI_MODEL_ID', 'models/gemini-flash-latest')
    
    # File Upload
    UPLOAD_FOLDER = os.path.abspath(os.getenv('UPLOAD_FOLDER', 'uploads'))
    VAULT_FOLDER = os.path.abspath(os.getenv('VAULT_FOLDER', 'vault_storage'))
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 50000000))  # 50MB default
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'jpg', 'png', 'jpeg'}
    
    # Paths
    POPPLER_PATH = os.getenv('POPPLER_PATH', r'C:\Program Files\poppler\Library\bin')
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')
    
    # Security
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_FILE_SIZE', 50000000))  # 50MB
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes
    SESSION_COOKIE_SECURE = True  # HTTPS only in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Select config based on environment
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
if FLASK_ENV == 'production':
    config = ProductionConfig()
elif FLASK_ENV == 'testing':
    config = TestingConfig()
else:
    config = DevelopmentConfig()
