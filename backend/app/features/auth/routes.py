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
            email=data['email'],
            password=data['password']
        )
        return jsonify({
            "message": "User registered successfully",
            "user": user_schema.dump(user)
        }), 201
    except ValueError as err:
        return jsonify({"message": str(err)}), 400