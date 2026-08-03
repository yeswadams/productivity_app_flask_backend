# The Appication Factory
import os
from flask import Flask

# config
from app.core.config import config_by_name
from app.extensions.bcrypt import bcrypt
from app.extensions.database import db
from app.extensions.jwt import jwt
from app.extensions.migrate import migrate

#models
from app.features.auth.models import User, PasswordResetToken
from app.features.expenses.models import Expense

def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    selected_config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(selected_config)

    print(f"--> Current config_name: {config_name}")
    print(f"--> Selected Config class: {selected_config}")
    print(f"--> Loaded SQLALCHEMY_DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

    # initializes the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    return app

    
    