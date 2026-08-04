from flask import Blueprint
from flask import Blueprint, jsonify


health_bp = Blueprint('health', __name__)


@health_bp.get('/health')
def health_check():
    """Liveness endpoint for local development and deployment checks."""
    return jsonify({"status": "ok"}), 200
