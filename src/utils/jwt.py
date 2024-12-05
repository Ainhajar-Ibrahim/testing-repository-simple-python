import json
from typing import Dict

from flask import jsonify
from flask_jwt_extended import JWTManager
from src.firestore import get_collection

from src.static import DATA_FILE_PATH


def register_jwt_handlers(jwt: JWTManager):
    @jwt.user_lookup_loader  
    def user_lookup_loader(
        _jwt_header: Dict[str, str], jwt_data: Dict[str, Dict[str, str]]
    ):
        try:
            username = jwt_data["sub"]

            users_ref = get_collection("users")
            user_query = users_ref.where("username", "==", username).limit(1).stream()

            user_data = None
            for user in user_query:
                user_data = user.to_dict()

            if user_data:
                return user_data  
            else:
                raise Exception("User not found in database.")
        except Exception as e:
            print(f"Error looking up user: {e}")
            return None

    @jwt.expired_token_loader
    def expired_token_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Token has expired.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.invalid_token_loader
    def invalid_token_loader(reason):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": f"Token is invalid: {reason}.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Fresh token is needed.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.revoked_token_loader
    def revoked_token_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Token is revoked.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.unauthorized_loader
    def unauthorized_loader(reason):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": f"Unauthorized: {reason}.",
                "solution": "Check your parameters.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.token_verification_failed_loader
    def token_verification_failed_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "UnauthorizedError",
                "name": "Unauthorized Error",
                "message": "Token verification failed.",
                "solution": "Please refresh your token.",
            },
            "code": 401,
            "status_code": 401,
        }
        return jsonify(json)

    @jwt.user_lookup_error_loader
    def user_lookup_error_loader(di, di2):  # pragma: no cover
        json = {
            "success": False,
            "error": {
                "type": "BadRequestError",
                "name": "BadRequest Error",
                "message": "User in identity not found in database.",
                "solution": "Try again.",
            },
            "code": 404,
            "status_code": 404,
        }
        return jsonify(json)
