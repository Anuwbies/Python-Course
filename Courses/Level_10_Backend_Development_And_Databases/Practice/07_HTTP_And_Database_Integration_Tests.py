# Independent task: http & database integration tests
#
# Implement a small create_app(path) with an SQLAlchemy SQLite orders table and POST/GET routes.
# Validate nonblank item and positive strict integer quantity. Prepare the isolated test schema
# inside the factory for this exercise only. Use request-scoped sessions and committed writes.
#
# Write pytest tests using tmp_path and TestClient for create/read across a fresh app instance
# at the same path, quantity-zero rejection (422), and missing ID (404). Expected behavior: all
# three tests pass against real file-backed storage. The migration capstone uses revisions
# instead of this test initializer.

