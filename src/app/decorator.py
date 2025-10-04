from functools import wraps
from flask import request, jsonify

from dotenv import load_dotenv
load_dotenv()
import os

from .message import IS_ERROR, STATUS
from .token import token_obj
from .database import db


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            resp = IS_ERROR["ERR_AUTH_TOKEN_MISSING"]
            status = STATUS["BAD_REQUEST"]
            return jsonify(resp), status
        token = token.split(" ")[1] if " " in token else token
        resp, status = token_obj.isTokenValid(token)
        if status != STATUS["OK"]:
            return jsonify(resp), status
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user_id = request.headers.get('UserID')
        if not user_id:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
            return jsonify(resp), status
        is_admin = db.get_user_admin_privilage_by_id(user_id)
        if is_admin is None:
            resp = IS_ERROR['ERR_USER_NOT_FOUND']
            status = STATUS["NOT_FOUND"]
            return jsonify(resp), status
        if not is_admin.get('is_admin', False):
            resp = IS_ERROR["ERR_USER_UNAUTHORIZED"]
            status = STATUS["BAD_REQUEST"]
            return jsonify(resp), status
        return f(*args, **kwargs)
    return decorator

def sudo_admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user_id = request.headers.get('UserID')
        if not user_id:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
            return jsonify(resp), status
        user = db.get_user_by_id(user_id)
        if not user or user['email'] != os.getenv("SUDO_ADMIN_EMAIL"):
            resp = IS_ERROR["ERR_USER_UNAUTHORIZED"]
            status = STATUS["BAD_REQUEST"]
            return jsonify(resp), status
        return f(*args, **kwargs)
    return decorator