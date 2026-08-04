from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    get_jwt
)

from app.features.auth.schemas.user_schema import (
    user_schema,
    user_register_schema,
    user_login_schema
)
from app.features.auth.services import AuthService

auth_bp = Blueprint(
    'auth', 
    __name__
)


def validation_error_response(errors):
    """Return validation errors in a shape understood by the supplied client."""
    messages = [message for field_errors in errors.values() for message in field_errors]
    return jsonify({"errors": messages, "fields": errors}), 422


def parse_registration_request():
    json_data = request.get_json(silent=True)
    if not json_data:
        return None, (jsonify({"errors": ["No input data provided"]}), 400)

    try:
        data = user_register_schema.load(json_data)
    except ValidationError as err:
        return None, validation_error_response(err.messages)

    confirmation = data.pop("password_confirmation", None)
    if confirmation is not None and confirmation != data["password"]:
        return None, (jsonify({"errors": ["Password confirmation does not match"]}), 422)
    return data, None


def register_user():
    data, error = parse_registration_request()
    if error:
        return None, error
    try:
        return AuthService.register_user(**data), None
    except ValueError as err:
        return None, (jsonify({"errors": [str(err)]}), 409)


def login_user():
    json_data = request.get_json(silent=True)
    if not json_data:
        return None, (jsonify({"errors": ["No input data provided"]}), 400)
    try:
        data = user_login_schema.load(json_data)
    except ValidationError as err:
        return None, validation_error_response(err.messages)
    try:
        return AuthService.authenticate_user(**data), None
    except ValueError as err:
        return None, (jsonify({"errors": [str(err)]}), 401)

@auth_bp.post('/register')
def register():
    """POST /api/v1/auth/register"""

    user, error = register_user()
    if error:
        return error
    return jsonify({
        "message": "User registered successfully",
        "user": user_schema.dump(user)
    }), 201

@auth_bp.post('/login')
def login():
    """POST /api/v1/auth/login"""

    auth_data, error = login_user()
    if error:
        return error
    return jsonify({
        "message": "Login successful",
        "access_token": auth_data['access_token'],
        "refresh_token": auth_data['refresh_token'],
        "user": user_schema.dump(auth_data['user'])
    }), 200



@auth_bp.post('/refresh')
@jwt_required(refresh=True)
def refresh_token():
    """POST /api/v1/auth/refresh (Requires a refresh token)"""
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200

@auth_bp.post('/logout')
@jwt_required()
def logout():
    """POST /api/v1/auth/logout - Revokes the user's active access token."""
    jti = get_jwt()["jti"]
    AuthService.logout_user(jti)
    return jsonify({"message": "Successfully logged out"}), 200


@auth_bp.get('/me')
@jwt_required()
def get_current_user():
    """GET /api/v1/auth/me - Get current user information"""
    try:
        current_user_id = int(get_jwt_identity())
        user = AuthService.get_user_by_id(current_user_id)
        return jsonify({
            "user": user_schema.dump(user)
        }), 200
    except ValueError as err:
        return jsonify({"message": str(err)}), 404


# Compatibility routes required by the provided React JWT client. The versioned
# API above remains the canonical API for new integrations.
client_auth_bp = Blueprint('client_auth', __name__)


@client_auth_bp.post('/signup')
def signup_client():
    user, error = register_user()
    if error:
        return error
    auth_data = AuthService.authenticate_user(user.username, request.get_json()["password"])
    return jsonify({"token": auth_data["access_token"], "user": user_schema.dump(user)}), 201


@client_auth_bp.post('/login')
def login_client():
    auth_data, error = login_user()
    if error:
        return error
    return jsonify({"token": auth_data["access_token"], "user": user_schema.dump(auth_data["user"])}), 200


@client_auth_bp.get('/me')
@jwt_required()
def me_client():
    user = AuthService.get_user_by_id(int(get_jwt_identity()))
    return jsonify(user_schema.dump(user)), 200
