import datetime
import jwt
from flask import request, jsonify
from .config import SECRET

def encode_token(payload_data, expires_in_hours=24):
    payload = payload_data.copy()
    payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expires_in_hours)
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None

def current_user():
    authorization = request.headers.get("Authorization", "")
    if not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    return decode_token(token)

def admin_user():
    user = current_user()
    if not user:
        return None
    if user.get("user") == "admin" or user.get("role") == "admin":
        return "admin"
    return None

def require_admin():
    if admin_user() != "admin":
        return jsonify({"error": "Admin authentication required."}), 401
    return None

