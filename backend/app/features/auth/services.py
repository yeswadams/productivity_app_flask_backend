from app.extensions.database import db
from app.extensions.bcrypt import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from app.features.auth.models import User

class AuthService:
    @staticmethod
    def register_user(username: str, email: str, password: str) -> User:
        """Hashes password and creates a new user in the db"""

        if User.query.filter_by(username=username).first():
            raise ValueError("Username is already taken")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            username=username,
            _password_hash=hashed_password
        )

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        """Verifies credentials and returns acces & refresh JWT tokens."""

        user = User.query.filter_by(username=username).first() 

        if not user or not bcrypt.check_password_hash(user._password_hash, password):
            raise ValueError("Invalid email or password")

        # Generate JWT
        identity = str(user.id)
        access_token = create_access_token(identity=identity)
        refresh_token=create_refresh_token(identity=identity)

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Fetches a user profile by ID"""
        user = User.query.get(user_id)
        if not user:
            raise ValueError("User not found")
        return user