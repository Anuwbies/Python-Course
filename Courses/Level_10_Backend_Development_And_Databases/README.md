# Level 10: Backend Development & Databases

**Stage:** Professional. **Prerequisites:** Levels 1–9.

Build a validated HTTP API with actual relational persistence, explicit transaction boundaries, reviewed migrations, and integration evidence across application restarts.

## Reading order

| Lesson | Guide | Saved task |
| --- | --- | --- |
| 1 | [HTTP, Routes & FastAPI](01_HTTP_Routes_And_FastAPI.md) | [Practice](Practice/01_HTTP_Routes_And_FastAPI.py) |
| 2 | [Request Validation & Response Contracts](02_Request_Validation_And_Response_Contracts.md) | [Practice](Practice/02_Request_Validation_And_Response_Contracts.py) |
| 3 | [Relational Data & Parameterized SQL](03_Relational_Data_And_Parameterized_SQL.md) | [Practice](Practice/03_Relational_Data_And_Parameterized_SQL.py) |
| 4 | [Transactions & Consistent Changes](04_Transactions_And_Consistent_Changes.md) | [Practice](Practice/04_Transactions_And_Consistent_Changes.py) |
| 5 | [SQLAlchemy Models & Sessions](05_SQLAlchemy_Models_And_Sessions.md) | [Practice](Practice/05_SQLAlchemy_Models_And_Sessions.py) |
| 6 | [Schema Migrations & Data Preservation](06_Schema_Migrations_And_Data_Preservation.md) | [Practice](Practice/06_Schema_Migrations_And_Data_Preservation.py) |
| 7 | [HTTP & Database Integration Tests](07_HTTP_And_Database_Integration_Tests.md) | [Practice](Practice/07_HTTP_And_Database_Integration_Tests.py) |

Continue with the [Persistent order API with revision history capstone](../../Capstones/Level_10_Backend_Development_And_Databases/README.md).

## Working through this level

Read the detailed explanation, trace the examples, and complete the practice ladder before the independent task. Each file in `Practice/` contains the full task, accepted inputs, and expected behavior as comments. Write your own implementation below those comments. Reference implementations are in `Solutions/`; compare them after an attempt.

Ask the assistant to review your saved submission when ready. Progress is recorded manually after review, including revisions and topics to revisit. Independent-task sections contain only the assignment and its expected behavior.

## Environment and run commands

Use a Python 3.13 project environment and install this level's requirements.txt. SQLAlchemy examples target the 2.0 API and Pydantic examples target v2. TestClient demonstrations run actual routes in process. The capstone includes Uvicorn and Alembic commands for a local service; tests use isolated SQLite files.

## Advancement

Build a validated HTTP API with actual relational persistence, explicit transaction boundaries, reviewed migrations, and integration evidence across application restarts.

Demonstrate the capstone with its documented normal, boundary, and failure cases and explain one small requirement change. Record evidence in [the Level 10 progress record](../../Progress/Level_10_Backend_Development_And_Databases.md). Running a reference does not complete your own submission.

## Scope and next steps

This level's local API is unauthenticated and uses SQLite for reproducible learning. Access control, deployment configuration, durable jobs, caching, and operational recovery are Level 11 responsibilities.
