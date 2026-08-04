from app.extensions.database import db
from app.features.auth.models import User
from app.features.auth.models.reset_token import PasswordResetToken
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

class ForgotPasswordSchema(SQLAlchemyAutoSchema):
    """Schema for POST /auth/forgot-password"""
    class Meta:
        model = User
        include_relationships = False

    username = fields.Str(required=True)

class ResetPasswordSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PasswordResetToken
        load_instance = True
        include_fk = True
        ordered = True

    id = db.Column(dump_only=True)
    token = db.Column(dump_only=True)
    expires_at = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)