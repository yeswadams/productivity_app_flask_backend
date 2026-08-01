from .base import Config

class ProductionConfig(Config):
    """
    Configuration used in production
    """
    DEBUG = False
    TESTING = False