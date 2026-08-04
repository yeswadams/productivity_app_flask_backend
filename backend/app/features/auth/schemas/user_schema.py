from app.features.auth.models import User
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import Schema, fields, validate
from app.extensions.database import db

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        load_instance = True 
        include_fk = True
        sqla_session = None
        ordered = True
        exclude = ["_password_hash"] # excludes password hash from serilization objects
    
    id = fields.Integer(dump_only=True)
    username = fields.String(
        required=True, 
        validate=[
            validate.Length(min=3, max=50, error='Username must be between 3 and 50 characters'),
            validate.Regexp(
                r'^[a-zA-z0-9_]+$',
                error="Username can only contain letters, numbers and underscores"
            )
        ]
    )
    created_at = fields.DateTime(dump_only=True)

class UserRegisterSchema(Schema):
    """Schema for POST /auth/register payloads"""
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=3, max=50),
            validate.Regexp(
                r'^[a-zA-z0-9_]+$',
                error="Username can only contain letters, numbers and underscores"
            )
        ]
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, error="Password must be at least 8 characters")
    )

class UserLoginSchema(Schema):
    """Schema for POST /auth/login payloads"""
    username = fields.Str(required=True)
    password = fields.Str(required=True)

# Singleton instances for clean imports across bp and services
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
    
