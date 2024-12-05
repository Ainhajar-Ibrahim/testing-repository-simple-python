import redis
from flask_caching import Cache

cache = Cache()
redis_client = redis.Redis(host='redis', port=6379, db=0)

def init_cache(app):
    cache.init_app(app)