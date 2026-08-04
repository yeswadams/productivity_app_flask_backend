import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
    Base config shared accross all environments
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'development-only-secret-key-change-me')
    JWT_SECRET_KEY = os.environ.get(
        'JWT_SECRET_KEY', 'development-only-jwt-secret-key-change-me'
    )
    # SQLAlchemy Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
