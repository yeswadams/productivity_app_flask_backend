from app.extensions.database import db
from app.extensions.bcrypt import bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from app.features.auth.models import User
from app.features.auth.models.token_blocklist import TokenBlocklist

class AuthService:
    @staticmethod
    def register_user(username: str, password: str) -> User:
        """Hashes password and creates a new user in the db"""

        if User.query.filter_by(username=username).first():
            raise ValueError("Username is already taken")

        user = User(username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        """Verifies credentials and returns access & refresh JWT tokens."""

        user = User.query.filter_by(username=username).first() 

        if not user or not bcrypt.check_password_hash(user._password_hash, password):
            raise ValueError("Invalid username or password")

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
    def logout_user(jti: str) -> None:
        """Revokes the current user's JWT token by adding its JTI to the blocklist."""
        blocked_token = TokenBlocklist(jti=jti)
        db.session.add(blocked_token)
        db.session.commit()

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Fetches a user profile by ID"""
        user = db.session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        return user
