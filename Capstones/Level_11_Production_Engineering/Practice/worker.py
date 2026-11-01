# Independent task: worker.py
#
# Implement a guarded worker launcher with its own DATABASE_URL engine. Repeatedly call
# storage.process_one, wait 0.2 seconds after work or 0.5 when idle, and rate-limit transient
# dependency reconnect attempts with a one-second wait. Use an Event and SIGINT/SIGTERM handlers
# for graceful stopping; dispose the engine in finally. Do not require TOKEN_SECRET or
# REDIS_URL.
# Expected behavior: pending jobs are processed without giving the worker API signing
# credentials.

