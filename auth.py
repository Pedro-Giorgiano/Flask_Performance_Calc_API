import bcrypt
from flask import request, jsonify
from functools import wraps
import jwt
import datetime
from models import session, User
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = session.query(User).filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # check the stored hash against the entered password
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"error": "Invalid credentials"}), 401

    # Gen jwt tonken
    token = jwt.encode({
        "username": username,
        "role": user.role,
        "user_id": user.id,
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            return jsonify({'error': 'Missing or malformed token'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = data
            print(f"request user {data}")
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)
    return decorated
