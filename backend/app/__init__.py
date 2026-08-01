# The Appication Factory
from flask import Flask

# config
from app.core.config import DevelopmentConfig
from app.extensions import bcrypt
from app.extensions import db
from app.extensions import jwt
from app.extensions import migrate

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initializes the extensions
    db.init_app(app, db)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    return app

    
    