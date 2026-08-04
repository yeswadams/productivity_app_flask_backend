from datetime import datetime, timezone
from app.extensions.database import db
from app.extensions.bcrypt import bcrypt


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reset_tokens = db.relationship('PasswordResetToken', back_populates='user', lazy='dynamic', cascade='all, delete-orphan')

    # Check constraints
    __table_args__ = (
        db.CheckConstraint('length(username) > 3', name='ck_users_username_min_length'),
    )

    def set_password(self, plain_text_password):
        # Responsible for hashing the password
        self._password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, plain_text_password):
        # Verifies an incoming plain-text password against the stored hashed one
        return bcrypt.check_password_hash(self._password_hash, plain_text_password)

    def __repr__(self):
        return f"<User {self.username}>"
