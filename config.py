import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
    
    # Inference Engine Configuration
    ACTION_PRIORITIES = {
        'block_ip': 10,
        'block_country': 9,
        'rate_limit': 8,
        'alert_admin': 7,
        'quarantine_traffic': 6,
        'enable_captcha': 5,
        'log_incident': 4,
        'monitor': 3,
        'investigate': 2,
        'notify_team': 1
    }