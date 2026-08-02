from datetime import datetime
from app.extensions.database import db
from app.extensions.bcrypt import bcrypt


class User(db.model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), nullable=False, unque=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    expense = db.relationship('Expense', uselist=False, back_populates='user')