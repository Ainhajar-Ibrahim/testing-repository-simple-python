from google.cloud import firestore
import os

# Set the environment variable for the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./config/testing-repository-e403c-firebase-adminsdk-av0jt-0b1ce1961a.json"

# Initialize Firestore client
db = firestore.Client()

def get_collection(collection_name):
    return db.collection(collection_name)