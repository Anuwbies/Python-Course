from pathlib import Path
import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from project import Base

config = context.config
if not config.get_main_option("sqlalchemy.url"):
    default = "sqlite+pysqlite:///" + (Path(__file__).resolve().parents[1] / "orders.sqlite").as_posix()
    config.set_main_option("sqlalchemy.url", os.environ.get("DATABASE_URL", default))
target_metadata = Base.metadata

def run_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"), target_metadata=target_metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_online():
    engine = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    try:
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata, render_as_batch=True)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()

if context.is_offline_mode():
    run_offline()
else:
    run_online()
