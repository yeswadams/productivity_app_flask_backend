from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token
)

from app.features.auth.schemas.user_schema import (
    user_schema,
    user_register_schema,
    user_login_schema
)
from app.features.auth.services import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', method=['POST'])
def register():
    """POST /api/v1/auth/register"""

    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400

    try:
        data = user_register_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"erros": err.messages}), 422

    try:
        user = AuthService.register_user(
            username=data['username'],
            password=data['password']
        )
        return jsonify({
            "message": "User registered successfully",
            "user": user_schema.dump(user)
        }), 201
    except ValueError as err:
        return jsonify({"message": str(err)}), 400

    

@auth_bp.route('/login', methods=['POST'])
def login():
    """POST /api/v1/auth/login"""

    json_data = request.get_json()
    if not json_data:
        return jsonify({
            "message": "No input data provided"
        }), 400

    try:
        data = user_login_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    try: 
        auth_data = AuthService.authenticate_user(
            username=data['username'],
            password=data['password']
        )
        return jsonify({
            "message": "Login successful",
            "access_token": auth_data['access_token'],
            "refresh_token": auth_data['refresh_token'],
            "user": user_schema.dump(auth_data['user'])
        }), 200
    except ValueError as err:
        return jsonify({"message": str(err)}), 401



@auth_bp.route('refresh', method=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    """POST /api/v1/auth/refresh (Requires a refresh token)"""
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify({"access_token": new_access_token}), 200