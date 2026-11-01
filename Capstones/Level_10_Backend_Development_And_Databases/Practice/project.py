# Independent task: Persistent order API with revision history
#
# Implement OrderInput and OrderOutput with item trimmed/nonblank/max80, strict integer quantity
# 1..100, and note default empty/max120. Define default_url() using DATABASE_URL when present
# and otherwise orders.sqlite beside project.py, and migrate(url) applying the neighboring
# Alembic history to head. Define create_app(url=None), using that default only when url is
# omitted, with POST /orders (201), GET /orders/{identifier} (200 or 404), and GET /health (200
# only for revision 0002; otherwise 503). Use real request-scoped SQLAlchemy sessions and
# committed writes. OrderOutput includes the server-assigned integer id. Expose app=create_app()
# for Uvicorn. Put the engine on app.state.engine so tests can dispose it after their client
# closes. Do not call create_all as a migration substitute.
#
# Complete the neighboring Alembic environment and two revision files according to their task
# comments. Enforce quantity/item/note constraints in the schema. Support actual
# upgrade/downgrade operations; note that dropping note discards that field's data.
#
# Provide a guarded demonstration using an isolated SQLite file: upgrade to head, create Pen/2,
# reject quantity 0, read a missing ID, dispose/recreate the app at the same URL, read the
# persisted item, and query the actual Alembic revision.
#
# Expected output:
#
# Created: 201
# Invalid: 422
# Missing: 404
# Persisted item: Pen
# Revision: 0002

