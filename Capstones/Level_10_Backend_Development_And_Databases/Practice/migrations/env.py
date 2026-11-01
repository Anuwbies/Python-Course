# Task: configure an actual Alembic environment for project.Base.metadata.
# Use the configured sqlalchemy.url when supplied; otherwise use DATABASE_URL
# or an orders.sqlite file beside project.py. Support offline and online modes,
# run migrations inside context.begin_transaction, and dispose the engine.
# Expected behavior: alembic upgrade head executes both supplied revisions.

