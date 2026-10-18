"""
Centurion University of Technology and Management (CUTM)
Backend Authentication & Authorization Module - JWT & Cryptography
"""

import datetime
import jwt
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from .config import SECRET, ADMIN_USERNAME, ADMIN_PASSWORD
except ImportError:
    from config import SECRET, ADMIN_USERNAME, ADMIN_PASSWORD


def hash_password(password: str) -> str:
    """Generates a salted cryptographic password hash using PBKDF2/scrypt."""
    return generate_password_hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """Safely verifies a candidate password against the stored cryptographic hash."""
    return check_password_hash(stored_hash, password)


def encode_token(username: str, role: str = "student", user_id: int = None, name: str = "", email: str = "", hours: int = 24) -> str:
    """Generates a digitally signed JSON Web Token (JWT) with 24-hour expiration."""
    payload = {
        "user": username,
        "role": role,
        "name": name,
        "email": email,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=hours)
    }
    if user_id is not None:
        payload["user_id"] = user_id
    return jwt.encode(payload, SECRET, algorithm="HS256")


def decode_token(token: str):
    """Decodes and validates a JSON Web Token."""
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def current_user():
    """Extracts and verifies the user payload from the incoming Authorization header."""
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return None
    token = authorization[7:].strip()
    return decode_token(token)


def admin_user():
    """Returns 'admin' if the caller possesses an authentic administrator token."""
    payload = current_user()
    if not payload:
        return None
    if payload.get("user") == "admin" or payload.get("role") == "admin":
        return "admin"
    return None


def require_admin():
    """Decorator/Guard returning HTTP 401 Unauthorized if caller is not an administrator."""
    if admin_user() != "admin":
        return jsonify({"error": "Admin authentication required."}), 401
    return None

