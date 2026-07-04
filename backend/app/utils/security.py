import bcrypt
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from app.config import Config

def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt(admin_id: int, username: str) -> str:
    """Generates a JSON Web Token valid for a set duration."""
    payload = {
        'admin_id': admin_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }
    # Encode the token using our secret key
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    """
    Decorator to protect Flask routes. Expects a header of the form:
        Authorization: Bearer <token>
    Returns 401 if the token is missing, malformed, expired, or invalid.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({"error": "Authentication token is missing."}), 401

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            # Make the decoded payload available to the route if it's needed
            request.admin = payload
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Session expired. Please log in again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid authentication token."}), 401

        return f(*args, **kwargs)
    return decorated