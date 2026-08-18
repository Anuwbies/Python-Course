# Lesson 4: Database Migrations with Alembic

As applications evolve, database schemas change. Alembic is the official database migration tool for SQLAlchemy, enabling version control for database schemas.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Initialize an Alembic migration environment (`alembic init -t async alembic`).
2. Generate automatic migration scripts by comparing SQLAlchemy models to database state (`--autogenerate`).
3. Apply (`alembic upgrade head`) and rollback (`alembic downgrade -1`) schema versions.
4. Execute migrations safely in automated CI/CD deployment pipelines.

---

## 1. Migration Workflow

```bash
# 1. Initialize migration environment
alembic init -t async migrations

# 2. Automatically generate migration from model changes
alembic revision --autogenerate -m "add_phone_number_to_users"

# 3. Apply migration to the database
alembic upgrade head

# 4. Roll back last migration
alembic downgrade -1
```

---

## 2. Anatomy of an Alembic Migration File

```python
"""add_phone_number_to_users"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone_number')
```

---

## 📝 Quick Exercise

**Prompt**:
Write an Alembic migration script that creates an `audit_logs` table with columns `id`, `event_name`, and `timestamp`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
"""create_audit_logs_table"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('event_name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table('audit_logs')
```
</details>
