# Lesson 6: Schema Migrations & Data Preservation

**Prerequisites:** Levels 1–9 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Schema_Migrations_And_Data_Preservation.py`.

Evolve an existing database through named changes and preserve the data already stored. A migration is an operational change with compatibility and rollback implications, not simply a regenerated model definition.

## 1. Separate revisions from current models

An ORM model describes the desired present schema. A revision records how to move from one known schema to another. Alembic tracks a revision graph and applies upgrade/downgrade operations through its environment and version table.

Autogeneration compares metadata with a database to propose changes. It cannot decide every business intention, such as whether a removed and added column are actually a rename. Review generated operations and any data transformation before applying them.

## 2. Add a compatible field

Adding a nonnullable field to existing rows requires a value for those rows or a staged backfill. A server default can make a simple added note field compatible with existing data. The database default and an application's Python default are distinct mechanisms.

Programmatic MigrationContext and Operations can demonstrate real DDL operations without a full CLI project. The capstone includes the actual revision environment and history so upgrades can be run as a normal operational step.

## 3. Account for database capabilities

SQLite supports a different set of alteration operations than PostgreSQL. Alembic's batch_alter_table can rebuild a table when direct alteration is unsuitable. DDL transaction guarantees and locking behavior vary by database; do not claim every schema change can be safely undone just because a downgrade function exists.

A downgrade that drops a field also drops its data. Rollback of application code and rollback of database data are not interchangeable. Backups, compatibility windows, and forward recovery can be more appropriate than a destructive reverse migration.

## 4. Observe actual data after the change

Inspect the real schema and a preserved row after an upgrade. A message saying migration complete is weak evidence if no connection executed the DDL. Then rehearse the supported downgrade and inspect the resulting schema again.

For a production rollout, test a copy of representative data, plan the migration's lock and runtime costs, and coordinate old/new application compatibility. This local exercise keeps the change deliberately small so the mechanism and consequences are inspectable.

## Execute and inspect a real alteration

`MigrationContext.configure(connection)` attaches Alembic operations to a SQLAlchemy connection. Operations exposes add_column; a batch context supplies drop_column when SQLite needs a rebuild. Column describes the actual DDL field, rather than an ORM attribute.

```python
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import Column, String, create_engine, inspect, text

engine = create_engine("sqlite+pysqlite:///:memory:")
try:
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE messages (id INTEGER PRIMARY KEY)"))
        connection.execute(text("INSERT INTO messages VALUES (1)"))
        operations = Operations(MigrationContext.configure(connection))
        operations.add_column("messages", Column("label", String(20),
                              nullable=False, server_default=""))
        columns = inspect(connection).get_columns("messages")
        print([column["name"] for column in columns])
        with operations.batch_alter_table("messages") as batch:
            batch.drop_column("label")
finally:
    engine.dispose()
```

engine.begin owns a connection and transaction together. text wraps literal SQL for SQLAlchemy execution; its named values can still be bound separately. inspect reads the database's actual metadata. A new inspection call after DDL avoids relying on a stale cached Inspector. Dropping label loses its values even though the id row remains.

## Build an actual revision environment

The capstone supplies alembic.ini and script.py.mako configuration scaffolding. Learn the editable boundaries here before completing its Python files. A revision module sets `revision = "a001"`, `down_revision = None` for its root, and defines upgrade/downgrade. Later revisions point down_revision to the prior ID. `branch_labels = None` and `depends_on = None` express that this linear exercise has no extra branch labels or cross-branch dependencies. Import `op` from alembic inside a revision. `op.create_table("messages", Column("id", Integer, primary_key=True))` creates a table; `op.drop_table("messages")` reverses that step. Import Column and Integer from sqlalchemy. `import sqlalchemy as sa` is the same import under a shorter alias, so sa.Column and sa.Integer name those same objects.

For named checks, `batch.create_check_constraint("ck_label", "length(label) <= 20")` adds one and `batch.drop_constraint("ck_label", type_="check")` removes it. Put removal before dropping the constrained field. Use this inside op.batch_alter_table for revision-based batch changes.

The environment file connects the revision runner to the chosen database:

```python
# The structure of an Alembic env.py; Base is your mapped project base.
from alembic import context
from sqlalchemy import engine_from_config, pool
from project import Base

config = context.config
target_metadata = Base.metadata

def run_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"),
                      target_metadata=target_metadata, literal_binds=True,
                      dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_online():
    engine = engine_from_config(config.get_section(config.config_ini_section),
                                prefix="sqlalchemy.", poolclass=pool.NullPool)
    try:
        with engine.connect() as connection:
            context.configure(connection=connection, target_metadata=target_metadata,
                              render_as_batch=True)
            with context.begin_transaction():
                context.run_migrations()
    finally:
        engine.dispose()

if context.is_offline_mode():
    run_offline()
else:
    run_online()
```

context.config is the active Alembic Config. get_main_option reads one setting; set_main_option writes it; get_section(config.config_ini_section) returns its settings mapping. engine_from_config extracts sqlalchemy-prefixed options. NullPool avoids retaining reusable pooled connections for this short-lived command. Online mode executes against a connection; offline mode emits SQL using the URL's dialect, without proving that a live upgrade ran. target_metadata enables schema comparison; render_as_batch supports SQLite batch output.

For a controlled programmatic run, import `Config` from alembic.config and `command` from alembic. Construct `config = Config(str(ini_path))`, set sqlalchemy.url to your isolated URL, then use `command.upgrade(config, "head")` or `command.downgrade(config, "a001")`. Applied IDs live in alembic_version; query its version_num through the real connection. An absent table or incorrect revision means the application is not ready for the expected schema.

To locate bundled configuration, use the source-relative Path helpers from Level 4. `sys.path.insert(0, str(project_directory))` explicitly adds the known project directory to the beginning of import lookup in env.py; do not populate it from arbitrary untrusted input. `os.environ` is a mapping of process environment text; `os.environ.get("DATABASE_URL", fallback)` permits an explicit deployment URL with a local fallback. Only apply that fallback when config.get_main_option("sqlalchemy.url") is empty, so a caller's isolated test URL wins. Required settings and secrets receive stricter treatment in Level 11.

References: [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [Batch migrations](https://alembic.sqlalchemy.org/en/latest/batch.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the value of an added nonnullable note on an existing row.
2. **Explain:** Explain why model create_all does not constitute a revision history.
3. **Modify:** Inspect a real preserved row after adding the column.
4. **Debug:** Identify the data loss caused by dropping a populated column on downgrade.

<details>
<summary>Hints</summary>

Inspect the database through the actual connection after each operation.

</details>

## Independent task: schema migrations & data preservation

In `Practice/06_Schema_Migrations_And_Data_Preservation.py`, complete this task:

Create a real in-memory orders table containing id 1 and quantity 2. Use Alembic MigrationContext/Operations to add a nonnullable string note column with an empty server default. Print whether note exists and the preserved quantity. Use batch_alter_table to drop note, then print whether it still exists. Dispose the engine.

Expected output:

```text
True
2
False
```
