# Task: write pytest integration tests for the actual project API and migrations.
# Use tmp_path SQLite files, real Alembic upgrades, and TestClient.
# Cover validation, missing IDs, restart persistence, and a 0001 row preserved
# through upgrade to head and downgrade to 0001. Dispose engines after each case.
# Expected behavior: tests observe committed rows and real revision/schema changes.

