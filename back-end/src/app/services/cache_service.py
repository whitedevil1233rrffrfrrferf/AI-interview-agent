import json
from infrastructure.redis import redis_client

def get_cache(key:str):
    data=redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def set_cache(key:str, value, ttl:int=3600):
    redis_client.set(key,json.dumps(value), ex=ttl)

