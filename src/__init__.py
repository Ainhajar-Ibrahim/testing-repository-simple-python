import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS  # type: ignore
from flask_jwt_extended import JWTManager

from src.routes.auth import auth_bp
from src.routes.user import user_bp
from src.utils.jwt import register_jwt_handlers
from flask_caching import Cache
from src.cache import init_cache 

APP_ROOT = os.path.join(os.path.dirname(__file__), "../")
dotenv_path = os.path.join(APP_ROOT, ".env")
load_dotenv(dotenv_path)


application = Flask(__name__, instance_relative_config=True)
application.config['CACHE_TYPE'] = 'redis'
application.config['CACHE_REDIS_URL'] = 'redis://redis:6379/0'



init_cache(application)


application.register_blueprint(auth_bp)
application.register_blueprint(user_bp)


application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
application.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY", "SECRET_KEY")

jwt_manager = JWTManager(application)
register_jwt_handlers(jwt_manager)

CORS(application, expose_headers="Authorization", supports_credentials=True)
