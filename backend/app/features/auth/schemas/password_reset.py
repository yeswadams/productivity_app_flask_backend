from app.extensions.database import db
from app.features.auth.models import User
from app.features.auth.models.reset_token import PasswordResetToken
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, validate

class PasswordResetTokenSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PasswordResetToken
        load_instance = True
        include_fk = True
        ordered = True

    # Auto-mapped field from model
    id = auto_field(dump_only=True)
    token = auto_field(dump_only=True)
    expires_at = auto_field(dump_only=True)
    created_at = auto_field(dump_only=True)


# 2. Input / Request Payload Schemas
class ForgotPasswordSchema(SQLAlchemyAutoSchema):
    """Schema for validating POST /forgot-password request body."""
    class Meta:
        model = User
        include_relationships = False

    # Standard field for username validation
    username = fields.Str(required=True)


class ResetPasswordSchema(SQLAlchemyAutoSchema):
    """Schema for validating POST /reset-password request body."""
    class Meta:
        model = PasswordResetToken
        include_relationships = False

    token = fields.Str(required=True)
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters long.")
    )


# Schema Instances
password_reset_token_schema = PasswordResetTokenSchema()
forgot_password_schema = ForgotPasswordSchema()
reset_password_schema = ResetPasswordSchema()