# Independent task: server.py
#
# Load DATABASE_URL, REDIS_URL, TOKEN_SECRET from the environment before serving. Reject a
# missing/short key without logging it. Create the SQLAlchemy engine with pool_pre_ping, Redis
# with bounded connect/read timeouts, configure nonsecret logging, and expose
# app=create_app(engine,cache,key) for Uvicorn. Expected behavior: missing configuration
# prevents
# startup; actual /ready probes reflect dependencies.

