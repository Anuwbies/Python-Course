# Lesson 4: Production Database Migrations with Alembic

In real-world software engineering, database schemas constantly change as new features are built—adding columns, creating foreign key relationships, altering constraints, and modifying indices. Manually modifying live production database tables using raw SQL leads to schema drift, data loss, and deployment failures. **Alembic** is the official database migration tool for SQLAlchemy, providing version-controlled, reversible, and automated schema evolution.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the core principles of Database Version Control and Schema Migrations.
2. Initialize and configure an **Alembic** environment (`alembic.ini`, `env.py`).
3. Configure `env.py` to support modern **Async SQLAlchemy Engines**.
4. Generate schema migrations automatically using `alembic revision --autogenerate`.
5. Execute forward and backward schema transitions (`alembic upgrade head`, `alembic downgrade -1`).
6. Apply **Zero-Downtime Migration Patterns** (expand-and-contract strategy for non-breaking deployments).

---

## 1. Alembic Architecture & File Structure

Initializing Alembic generates the following migration repository structure:

```
my_project/
├── alembic.ini                   # Configuration file (DB URL, logging)
├── migrations/
│   ├── env.py                    # Python script executed during migration commands
│   ├── script.py.mako            # Template for new migration files
│   └── versions/                 # Versioned migration scripts
│       ├── 20260819_01_init_users.py
│       └── 20260819_02_add_mfa_columns.py
```

---

## 2. Configuring `env.py` for Async SQLAlchemy

By default, Alembic uses a synchronous database driver. To support async engines (`asyncpg`, `aiosqlite`), configure `migrations/env.py` using `async_engine_from_config`:

```python
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context
from my_app.models import Base # Import your SQLAlchemy DeclarativeBase metadata

# Target metadata allows Alembic to detect differences between code and live DB:
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True # Detect column type changes
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    asyncio.run(run_async_migrations())
```

---

---

## 4. Zero-Downtime Migration Pattern (Expand & Contract)

In production high-availability systems with active web servers, running destructive migrations (e.g. renaming a column from `old_col` to `new_col`) immediately causes downtime because existing running app versions crash trying to query `old_col`.

### The 3-Phase Expand & Contract Strategy:
1. **Phase 1 (Expand)**: Add `new_col` as nullable. Deploy new app version writing to *both* `old_col` and `new_col`, but reading from `old_col`.
2. **Phase 2 (Backfill & Switch)**: Run background data backfill script copying old data into `new_col`. Deploy app version reading from `new_col`.
3. **Phase 3 (Contract)**: Drop `old_col` and enforce `NOT NULL` on `new_col`.

---

## 5. Resolving Multi-Head Migration Conflicts

When two engineers create migrations on separate Git branches simultaneously, merging causes **Multiple Heads**:

```bash
# Check for split migration branches:
$ alembic heads
# Output:
# 3a1b8c2d (head) - Feature A
# 7f9e1d4c (head) - Feature B

# Merge branches into a single unified revision:
$ alembic merge -m "Merge branch A and B revisions" 3a1b8c2d 7f9e1d4c
```

---

## 6. SQLite Batch Migration Mode (`render_as_batch=True`)

SQLite does not natively support altering columns or dropping foreign keys via standard `ALTER TABLE`. Alembic's **Batch Mode** recreates the table, copies existing rows, and replaces the old table seamlessly:

```python
with op.batch_alter_table("users", schema=None) as batch_op:
    batch_op.alter_column("email", type_=sa.String(300), nullable=False)
    batch_op.drop_constraint("fk_old_company", type_="foreignkey")
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master Alembic migrations, revisions, autogeneration, zero-downtime evolution, and conflict merging:

---

### 🟢 Tier 1: Alembic Configuration & Basic Revisions (Exercises 1–3)

#### 🔹 Exercise 1: Configure `alembic.ini`
* **Goal**: Point `sqlalchemy.url` to an environment variable `os.environ["DATABASE_URL"]`.

#### 🔹 Exercise 2: Create First Manual Revision
* **Goal**: Write an Alembic migration script creating a `users` table with `op.create_table()`.

#### 🔹 Exercise 3: Inspect Current Revision
* **Goal**: Use `alembic current` and query the `alembic_version` table.

---

### 🟡 Tier 2: Column Additions & Autogeneration (Exercises 4–6)

#### 🔹 Exercise 4: Autogenerate Diff Migration
* **Goal**: Add a `bio` column to a SQLAlchemy model and run `alembic revision --autogenerate`.

#### 🔹 Exercise 5: Reversible Downgrade Script
* **Goal**: Verify that calling `alembic downgrade -1` cleanly removes added columns without data corruption.

#### 🔹 Exercise 6: Adding Unique Index via Migration
* **Goal**: Write `op.create_index("idx_user_email", "users", ["email"], unique=True)`.

---

### 🟠 Tier 3: Zero-Downtime & Multi-Head Merging (Exercises 7–9)

#### 🔹 Exercise 7: SQLite Batch Mode Column Modification
* **Goal**: Use `op.batch_alter_table()` to alter a column type in SQLite.

#### 🔹 Exercise 8: Resolve Multiple Migration Heads
* **Goal**: Simulate two conflicting migration branches and merge them with `alembic merge`.

#### 🔹 Exercise 9: Zero-Downtime Column Rename Simulation
* **Goal**: Implement Phase 1 of Expand-and-Contract by adding a new column and writing a data sync trigger.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Multi-Factor Authentication Schema Migration Runner
* **Goal**: Build a programmatic schema migration engine executing forward upgrades and rollback downgrades on live authentication tables.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Automated Schema Evolution & Migration Simulation Engine**, demonstrating revision history tracking, upgrade/downgrade execution functions, and programmatic table schema transformation:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Programmatic Database Schema Migration Engine
# =====================================================================

import sqlite3
import os
from typing import Callable

DB_FILE = "enterprise_app.db"

class MigrationEngine:
    """Manages version-controlled database schema migrations."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._migrations: list[dict] = []
        self._init_migration_table()

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_migration_table(self) -> None:
        """Initializes the alembic_version tracking table."""
        with self._get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS schema_version_control (
                revision_id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """)

    def register_revision(self, rev_id: str, desc: str, upgrade_fn: Callable, downgrade_fn: Callable) -> None:
        self._migrations.append({
            "revision_id": rev_id,
            "description": desc,
            "upgrade": upgrade_fn,
            "downgrade": downgrade_fn
        })

    def get_current_revision(self) -> str | None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT revision_id FROM schema_version_control ORDER BY applied_at DESC LIMIT 1;")
            row = cursor.fetchone()
            return row[0] if row else None

    def upgrade_to_head(self) -> None:
        current = self.get_current_revision()
        applied_revs = set()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT revision_id FROM schema_version_control;")
            applied_revs = {r[0] for r in cursor.fetchall()}

        for m in self._migrations:
            if m["revision_id"] not in applied_revs:
                print(f"⏩ [MIGRATING UP] Revision: {m['revision_id']} - {m['description']}")
                with self._get_connection() as conn:
                    m["upgrade"](conn)
                    conn.execute(
                        "INSERT INTO schema_version_control (revision_id, description) VALUES (?, ?)",
                        (m["revision_id"], m["description"])
                    )
                print(f"  ✓ Successfully applied revision {m['revision_id']}")

    def downgrade_last(self) -> None:
        current = self.get_current_revision()
        if not current:
            print("⚠️ No applied migrations to downgrade.")
            return

        matching = next((m for m in self._migrations if m["revision_id"] == current), None)
        if matching:
            print(f"⏪ [ROLLING BACK] Revision: {matching['revision_id']} - {matching['description']}")
            with self._get_connection() as conn:
                matching["downgrade"](conn)
                conn.execute("DELETE FROM schema_version_control WHERE revision_id = ?", (current,))
            print(f"  ✓ Successfully rolled back revision {current}")


# Define Schema Revisions
def rev_01_up(conn: sqlite3.Connection):
    conn.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        full_name TEXT NOT NULL
    );
    """)

def rev_01_down(conn: sqlite3.Connection):
    conn.execute("DROP TABLE IF EXISTS users;")

def rev_02_up(conn: sqlite3.Connection):
    conn.execute("ALTER TABLE users ADD COLUMN is_mfa_enabled INTEGER DEFAULT 0 NOT NULL;")
    conn.execute("ALTER TABLE users ADD COLUMN phone_number TEXT DEFAULT NULL;")

def rev_02_down(conn: sqlite3.Connection):
    # SQLite 3.35+ supports DROP COLUMN
    conn.execute("ALTER TABLE users DROP COLUMN is_mfa_enabled;")
    conn.execute("ALTER TABLE users DROP COLUMN phone_number;")


# Execution Simulation
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

engine = MigrationEngine(DB_FILE)
engine.register_revision("0001_init", "Initialize core users table", rev_01_up, rev_01_down)
engine.register_revision("0002_add_mfa", "Add MFA and phone verification columns", rev_02_up, rev_02_down)

print("=" * 75)
print(f"{'DATABASE SCHEMA MIGRATION PIPELINE SIMULATION':^75}")
print("=" * 75)

# Apply all migrations
print("\n--- PHASE 1: Upgrade Database Schema to Head ---")
engine.upgrade_to_head()
print(f"Current Schema Version: {engine.get_current_revision()}")

# Test schema with insert
with sqlite3.connect(DB_FILE) as conn:
    conn.execute("INSERT INTO users (email, full_name, is_mfa_enabled, phone_number) VALUES (?, ?, ?, ?)",
                 ("elena@corp.io", "Elena Rostova", 1, "+1-555-0199"))
    row = conn.execute("SELECT * FROM users").fetchone()
    print(f"Verified Inserted User Record: {row}")

# Rollback one migration
print("\n--- PHASE 2: Downgrade Last Migration ---")
engine.downgrade_last()
print(f"Current Schema Version: {engine.get_current_revision()}")

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)
print("=" * 75)
```

### 🔍 Code Explanation:
- **`schema_version_control`**: Mirrors Alembic's `alembic_version` table, persisting which migration hashes have already been executed against the database.
- **Idempotent Upgrades**: `upgrade_to_head` checks applied revisions and only runs unapplied migrations sequentially.
- **Reversible Downgrades**: `downgrade_last` invokes the inverse `down()` function and removes the tracking record, allowing safe local and staging rollbacks.

---

## 📝 Quick Exercise: Multi-Factor Authentication Schema Migration Script

### 🏢 Real-Life Scenario
You are the lead database engineer preparing an Alembic migration script for an upcoming security release. The security team requires adding two columns to the `accounts` table: `totp_secret` (a 32-character string for authenticator apps) and `failed_login_attempts` (an integer defaulting to 0). You must construct the Python migration functions (`upgrade()` and `downgrade()`) and verify execution.

### 📋 Requirements
1. **Define `upgrade(conn)` Function**:
   - Executes `ALTER TABLE accounts ADD COLUMN totp_secret TEXT DEFAULT NULL;`
   - Executes `ALTER TABLE accounts ADD COLUMN failed_login_attempts INTEGER DEFAULT 0 NOT NULL;`
2. **Define `downgrade(conn)` Function**:
   - Drops `totp_secret` and `failed_login_attempts` columns.
3. Test applying the upgrade on a test database, inserting a record, and rolling back cleanly.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 database migration concepts with Level 1 SQLite3, functions, and string formatting.

### 🎯 Expected Output
```text
==================================================
        ALEMBIC SECURITY MIGRATION RUNNER         
==================================================
⏩ Running migration: 20260819_add_security_mfa (upgrade)
  ✓ Columns 'totp_secret' and 'failed_login_attempts' added.
  ✓ Inserted verified account: (1, 'elena@corp.com', 'SECRET_KEY_XYZ_99', 0)
⏪ Running migration: 20260819_add_security_mfa (downgrade)
  ✓ Rolled back MFA columns successfully.
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (MFA Migration & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Multi-Factor Authentication Schema Migration Runner
# =====================================================================
import sqlite3
import os

DB_TEST = "test_mfa_migration.db"
if os.path.exists(DB_TEST):
    os.remove(DB_TEST)

conn = sqlite3.connect(DB_TEST)
conn.execute("CREATE TABLE accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL);")
conn.commit()

def upgrade_add_mfa(connection: sqlite3.Connection):
    connection.execute("ALTER TABLE accounts ADD COLUMN totp_secret TEXT DEFAULT NULL;")
    connection.execute("ALTER TABLE accounts ADD COLUMN failed_login_attempts INTEGER DEFAULT 0 NOT NULL;")
    connection.commit()

def downgrade_add_mfa(connection: sqlite3.Connection):
    connection.execute("ALTER TABLE accounts DROP COLUMN totp_secret;")
    connection.execute("ALTER TABLE accounts DROP COLUMN failed_login_attempts;")
    connection.commit()

print("==================================================")
print("        ALEMBIC SECURITY MIGRATION RUNNER         ")
print("==================================================")
print("⏩ Running migration: 20260819_add_security_mfa (upgrade)")
upgrade_add_mfa(conn)
print("  ✓ Columns 'totp_secret' and 'failed_login_attempts' added.")

conn.execute("INSERT INTO accounts (email, totp_secret, failed_login_attempts) VALUES (?, ?, ?)",
             ("elena@corp.com", "SECRET_KEY_XYZ_99", 0))
conn.commit()
row = conn.execute("SELECT * FROM accounts WHERE email = 'elena@corp.com'").fetchone()
print(f"  ✓ Inserted verified account: {row}")

print("⏪ Running migration: 20260819_add_security_mfa (downgrade)")
downgrade_add_mfa(conn)
print("  ✓ Rolled back MFA columns successfully.")
print("==================================================")

conn.close()
if os.path.exists(DB_TEST):
    os.remove(DB_TEST)

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: alembic.ini config
# sqlalchemy.url = %(DATABASE_URL)s

# Ex 2: op.create_table
# op.create_table('users', sa.Column('id', sa.Integer, primary_key=True), sa.Column('email', sa.String, nullable=False))

# Ex 3: alembic current
# alembic current --verbose

# Ex 4: autogenerate
# alembic revision --autogenerate -m "add bio column"

# Ex 5: downgrade
# def downgrade(): op.drop_column('users', 'bio')

# Ex 6: create index
# op.create_index('idx_user_email', 'users', ['email'], unique=True)

# Ex 7: batch alter table
# with op.batch_alter_table('users') as batch_op: batch_op.alter_column('email', type_=sa.String(300))

# Ex 8: merge heads
# alembic merge -m "merge revisions" rev_a rev_b

# Ex 9: Expand and Contract pattern
# Phase 1: op.add_column('users', sa.Column('new_col', sa.String, nullable=True))
```
</details>
