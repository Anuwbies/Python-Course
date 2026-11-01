import logging
import os
import redis
from sqlalchemy import create_engine
from project import create_app

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
url = os.environ["DATABASE_URL"]
key = os.environ["TOKEN_SECRET"]
if len(key) < 32:
    raise ValueError("TOKEN_SECRET is too short")
engine = create_engine(url, pool_pre_ping=True, pool_timeout=2, connect_args={"connect_timeout":2,"options":"-c statement_timeout=2000"})
cache = redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True,
                            socket_connect_timeout=2, socket_timeout=2)
app = create_app(engine, cache, key)
