from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import create_access_token
from src.firestore import get_collection
from flask import Blueprint, jsonify
import random
from src.cache import cache, redis_client


auth_bp = Blueprint("auth_bp", __name__)

def generate_unique_id():
    while True:
        user_id = random.randint(1, 999999)
        users_ref = get_collection("users")
        user_query = users_ref.where("id", "==", user_id).limit(1).stream()

        if not any(user_query):
            return user_id
        
# Check if user data is cached
def get_cached_user(username):
    cached_user = redis_client.get(username)
    if cached_user:
        return json.loads(cached_user)
    return None

# Cache the user data
def cache_user(username, user_data):
    redis_client.setex(username, 3600, json.dumps(user_data))

@auth_bp.post("/authenticate")
def authenticate():
    try:
        username = request.form["username"]

        # Try fetching user from cache first
        cached_user = get_cached_user(username)
        
        if cached_user:
            user = cached_user
            print("User fetched from cache.")
        else:
            # If not found in cache, query Firestore
            users_ref = get_collection("users") 
            user_doc = users_ref.where("username", "==", username).stream()

            user = None
            for doc in user_doc:
                user = doc.to_dict()

            # If user exists in Firestore, cache the result
            if user:
                print("User fetched from Firestore.")
                cache_user(username, user)
            else:
                # If user doesn't exist, create new user
                user_id = generate_unique_id()
                users_ref.add({
                    "username": username,
                    "id": user_id
                })
                user = {"username": username, "id": user_id}
                print("New user created in Firestore.")

                # Cache the new user data
                cache_user(username, user)

        # Generate JWT token
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500