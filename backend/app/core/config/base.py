import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
    Base config shared accross all environments
    """
    SECRET_KEY = os.getenv(
        'SECRET_KEY', 'dev-secret-key-change-in-prod'
    )
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key')
    # SQLAlchemy Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
