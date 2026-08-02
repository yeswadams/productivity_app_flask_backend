from app.extensions.database import db
from datetime import datetime, timezone

class PasswordResetToken(db.model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Columnn(db.String(100), nullbale=False)
    is_used = db.Column(db.Boolen, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), nullable=False)
    expirats_at = db.Column(db.Datetime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='reset_tokens')

    def is_valid(self):
        """Checks if token has not expired and has not been used yet"""
        return not self.is_used and datetime.now(timezone.utc)

    def __repr__(self):
        return f"<PasswordResetToken user_id+{self.user_id} used={self.is_used}>"