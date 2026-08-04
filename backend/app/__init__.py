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

#blueprints
from app.features.auth.routes import auth_bp, client_auth_bp
from app.features.expenses.routes import expenses_bp
from app.core.health.routes import health_bp

def register_bp(app):
    app.register_blueprint(
        auth_bp,
        url_prefix='/api/v1/auth'
    )
    app.register_blueprint(
        expenses_bp,
        url_prefix='/api/v1/expenses'
    )
    app.register_blueprint(client_auth_bp)
    app.register_blueprint(health_bp, url_prefix='/api/v1')


def create_app(config_name=None):
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    selected_config = config_by_name.get(config_name, config_by_name['default'])
    app.config.from_object(selected_config)

    app.json.sort_keys=False

    # initializes the extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    register_bp(app)

    return app
