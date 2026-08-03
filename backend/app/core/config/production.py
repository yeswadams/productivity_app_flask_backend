import os
from .base import Config

class ProductionConfig(Config):
    """
    Configuration used in production
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')