import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
    Base config shared accross all environments
    """
    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )
    # SQLAlchemy Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask setting for preventing Flask from sorting JSON in alphabetic order
    JSON_SORT_KEYS = False