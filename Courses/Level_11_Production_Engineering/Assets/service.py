import os
import psycopg
import redis
from fastapi import FastAPI, HTTPException

app = FastAPI()
@app.get("/ready")
def ready():
    try:
        with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=2) as connection:
            row = connection.execute("SELECT 1").fetchone()
        with redis.Redis.from_url(os.environ["REDIS_URL"], socket_connect_timeout=2, socket_timeout=2) as cache:
            healthy = row == (1,) and cache.ping()
    except (psycopg.Error, redis.exceptions.RedisError):
        raise HTTPException(503, "Dependencies unavailable")
    if not healthy:
        raise HTTPException(503, "Dependencies unavailable")
    return {"status":"ready"}
