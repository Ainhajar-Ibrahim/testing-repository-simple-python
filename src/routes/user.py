from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.firestore import get_collection
from src.cache import redis_client, cache

user_bp = Blueprint("user_bp", __name__)

@user_bp.route('/id', methods=['GET'])
@jwt_required()
def get_user_id():
    print("Getting user ID...")

    try:
        # Get the username from the JWT identity
        username = get_jwt_identity()

        # Check if user ID is cached in Redis
        cached_user_id = redis_client.get(f"user:{username}:id")
        if cached_user_id:
            # User ID found in Redis cache
            print("User ID found in cache")
            return jsonify({"id": cached_user_id.decode('utf-8')}), 200

        # If not cached, fetch from Firestore
        print("User ID not found in cache, querying Firestore...")
        users_ref = get_collection("users")
        user_query = users_ref.where("username", "==", username).limit(1).stream()

        user_data = None
        for user in user_query:
            user_data = user.to_dict()

        if user_data:
            user_id = user_data.get("id")

            redis_client.setex(f"user:{username}:id", 3600, user_id)

            return jsonify({"id": user_id}), 200
        else:
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        print(f"Error retrieving user ID: {e}")
        return jsonify({"message": "Error retrieving user ID"}), 500