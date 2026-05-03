import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")

redis_client=redis.Redis(
    host=redis_host,
    port=redis_port,
    db=redis_db
)
