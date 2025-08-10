import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Require real environment values; no insecure defaults
    SUPABASE_URL = os.environ.get('SUPABASE_URL')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
    
    # Flask settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))

    # Flask-Caching defaults (avoid null warning)
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # Database settings
    DB_RETRY_ATTEMPTS = int(os.environ.get('DB_RETRY_ATTEMPTS', 3))
    DB_RETRY_DELAY = int(os.environ.get('DB_RETRY_DELAY', 2))
    DB_MAX_RETRY_DELAY = int(os.environ.get('DB_MAX_RETRY_DELAY', 300))
    
    # Regional mapping
    REGION_MAPPING = {
        "Ανατολικής Μακεδονίας και Θράκης": "FR1",
        "Κεντρικής Μακεδονίας": "FR2",
        "Δυτικής Μακεδονίας": "FR3",
        "Ηπείρου": "FR4",
        "Θεσσαλίας": "FR5",
        "Ιονίων Νήσων": "FR6",
        "Δυτικής Ελλάδας": "FR7",
        "Στερεάς Ελλάδας": "FR8",
        "Αττικής": "FR9",
        "Πελοποννήσου": "FR10",
        "Βορείου Αιγαίου": "FR11",
        "Νοτίου Αιγαίου": "FR12",
        "Κρήτης": "FR13"
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 