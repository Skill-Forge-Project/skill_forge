from functools import wraps
import os
from flask import request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

INTERNAL_SECRET = os.getenv("INTERNAL_SECRET")

def generate_token(identity):
    return create_access_token(identity=identity, expires_delta=timedelta(hours=1))

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

def set_avatar(image_path: str) -> bytes:
    """
    Reads an image from the given path and returns its binary content.
    
    :param image_path: Path to the image file.
    :return: Binary content of the image.
    """
    try:
        with open(image_path, "rb") as image_file:
            return image_file.read()
    except FileNotFoundError:
        raise ValueError(f"File not found: {image_path}")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the file: {e}")