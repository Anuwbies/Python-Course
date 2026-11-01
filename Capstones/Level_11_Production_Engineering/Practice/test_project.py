# Independent task: test_project.py
#
# Write pytest cases against the actual API factory, SQLAlchemy store, and migrations using
# tmp_path SQLite files and an explicitly labeled isolated cache adapter. Cover 401/403 role
# rules, order creation, duplicate idempotency keys, effect rollback, successful retry,
# completed
# replay, and three-attempt exhaustion. Expected behavior: tests establish local contracts;
# PostgreSQL worker locking and Redis TTL/network behavior still require the real Compose stack.

