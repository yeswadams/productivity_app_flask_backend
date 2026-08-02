from datetime import datetime
from app.extensions.database import db
from app.extensions.bcrypt import bcrypt


class User(db.model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), nullable=False, unique=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reset_token = db.relationship('PasswordResetToken', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, plain_text_password):
        # Responsible for hashing the password
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, plain_text_password):
        # Verifies an incoming plain-text password against the stored hashed one
        return bcrypt.check_password_hash(self.password_hash, plain_text_password)

    def __repr__(self):
        return f"<User {self.name}>"
