from flask_jwt_extended import JWTManager
from flask import jsonify
from app.features.auth.models.token_blocklist import TokenBlocklist


jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None


@jwt.unauthorized_loader
def missing_token(message):
    return jsonify({"errors": [message]}), 401


@jwt.invalid_token_loader
def invalid_token(message):
    return jsonify({"errors": [message]}), 422


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({"errors": ["Token has expired"]}), 401


@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    return jsonify({"errors": ["Token has been revoked"]}), 401
