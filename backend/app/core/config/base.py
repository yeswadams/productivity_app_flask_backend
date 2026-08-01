import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config():
    """
    Base config shared accross all environments
    """
    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    #DB config
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}"
    )

    # SQLAlchemy Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask setting for preventing sorting JSON in alphabetic order
    JSON_SORT_KEYS = False