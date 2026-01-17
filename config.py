import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Generate secure random key if not provided (for development only)
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
    
    # Warn if using auto-generated key
    if not os.environ.get('SECRET_KEY'):
        print("⚠️  WARNING: Using auto-generated SECRET_KEY. Set SECRET_KEY environment variable in production!")
    
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL')
        or 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'cybersecurity.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour session timeout