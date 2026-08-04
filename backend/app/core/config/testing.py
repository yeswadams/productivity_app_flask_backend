from .base import Config

class TestingConfig(Config):
    """
    Configuration used during automated testing
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
