"""
Configuration module for the Smart Horses Backend.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Server settings
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS settings
    cors_origins_str = os.getenv('CORS_ORIGINS', '*')
    if cors_origins_str == '*':
        CORS_ORIGINS = '*'
    else:
        CORS_ORIGINS = [origin.strip() for origin in cors_origins_str.split(',')]
    
    # API settings
    MAX_BOARD_SIZE = 20
    MIN_BOARD_SIZE = 4
    DEFAULT_BOARD_SIZE = 8
    
    # Algorithm settings (you'll implement these later)
    MAX_EXECUTION_TIME = 60  # seconds
    

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment."""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
