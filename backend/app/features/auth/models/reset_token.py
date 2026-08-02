from app.extensions.database import db
from datetime import datetime

class PasswordResetToken(db.model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Columnn(db.String(100), nullbale=False)
    expiration = db.Column(db.Datetime, nullable=False)

    user = db.relationship('User', backref='reset_tokens')