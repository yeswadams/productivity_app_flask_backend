from app.extensions.database import db
from datetime import datetime, timezone, timedelta
import secrets

class PasswordResetToken(db.Model):
    __tablename__ = 'password_reset_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default= lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship('User', back_populates='reset_tokens')

    @staticmethod
    def generate_for_user(user_id: int, expires_in_minutes: int = 15):
        PasswordResetToken.query.filter_by(user_id=user_id).delete()

        token = PasswordResetToken(
            token=secrets.token_urlsafe(32),
            user_id=user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
        )

        db.session.add(token)
        db.session.commit()

        return token

    def is_expired(self) -> bool:
        """Checks if token has not expired and has not been used yet"""
        expires_at = self.expires_at

        if expires_at.tzinfo is None:
            expires_att = expires_at.replace(tzinfo=timezone.utc)

        return datetime.now(timezone.utc) > expires_at

    def __repr__(self):
        return f"<PasswordResetToken user_id={self.user_id} expired={self.expires_at}>"

    