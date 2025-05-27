import os
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import request, jsonify

INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

def token_required(f):
    """Decorator to check if the request has a valid JWT token.

    Args:
        f (object): function to be decorated

    Returns:
        function object: function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"error": "Unauthorized", "message": str(e)}), 401
        return f(*args, **kwargs)
    return decorated

def internal_only(f):
    """
    Decorator to restrict access to internal users only.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        secret = request.headers.get("INTERNAL-SECRET", "")
        if secret != INTERNAL_SECRET:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated