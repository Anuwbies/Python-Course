# Lesson 7: HTTP & Database Integration Tests

**Prerequisites:** Levels 1–9 and Lessons 1–6 of this level. **Practice file:** `Practice/07_HTTP_And_Database_Integration_Tests.py`.

Exercise the actual route, validation, and storage layers together under isolated conditions. A persistent API needs evidence that data survives a fresh application instance, not merely a second dictionary lookup.

## 1. Decide the test boundary

An in-process HTTP client can exercise request parsing, dependencies, route behavior, database statements, and response serialization. It does not exercise a real listening socket, reverse proxy, or remote database server unless those are explicitly included.

A unit test can replace storage to isolate a domain rule. An integration test should use the real selected storage implementation. Do not replace the repository with a fixed answer and then claim database persistence was tested.

## 2. Give each test a database

Use tmp_path for a unique SQLite file and an application factory receiving that path. A fresh app with the same path should read an earlier committed order. A fresh path should begin empty. These two cases distinguish persistence from unintended global state.

A test-only create_all initializer can prepare an isolated schema for a bounded test. Migration behavior needs its own test against revision operations; the capstone uses actual Alembic upgrades rather than assuming table creation covers revision history.

## 3. Scope sessions to requests

FastAPI Depends can call a generator dependency that yields a Session inside a with block. The dependency holds the session for the request and closes it afterward. Explicitly commit successful writes before returning data that must survive the request.

With SQLite used across TestClient worker threads, configure the engine's thread compatibility appropriately and use separate sessions. Disabling a driver thread check is not permission to share one Session across concurrent requests.

## 4. Assert behavior and state

Check status and meaningful response fields. For a rejected payload, inspect that no order was created. For a missing ID, expect a documented 404. For restart persistence, recreate the app and read the actual stored identifier.

A coverage percentage is optional measured information, not a substitute for these behavioral claims. Include failure cases that would catch a broken commit, missing validation, or shared-state leak rather than adding assertions that merely mirror implementation details.

## Wire a generator dependency and own the engine

The public Depends API calls the dependency per request and arranges exit from its yielded resource lifetime. For an app-local engine, register it explicitly:

```python
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

# engine is a configured SQLAlchemy engine from Lesson 5.
app = FastAPI()
app.state.engine = engine

def session_dependency():
    with Session(engine) as session:
        yield session

@app.get("/database-probe")
def database_probe(session: Session = Depends(session_dependency)):
    from sqlalchemy import text
    return {"value": session.execute(text("SELECT 1")).scalar_one()}
```

app.state is an application-owned namespace, useful for test cleanup: after the client exits, call app.state.engine.dispose(). With a file-backed SQLite URL, `create_engine(url, connect_args={"check_same_thread": False})` permits the driver connections' use across the framework's worker threads; retain one Session per request. `url.startswith("sqlite")` tests the known URL prefix before selecting SQLite-only options. Do not pass them to PostgreSQL drivers.

A POST can build `Order(**payload.model_dump())`, add it, commit, refresh it, then return explicitly selected fields. A GET can use session.get and raise HTTPException(404, ...) for None. A schema probe can query alembic_version, catch SQLAlchemyError from sqlalchemy.exc, and return 503 on query failure or an unexpected revision. This is the limited database readiness required by the capstone; full dependency readiness follows next level.

References: [FastAPI database patterns](https://fastapi.tiangolo.com/tutorial/sql-databases/), [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict what a fresh app should see with the same versus a new database path.
2. **Explain:** Explain why an in-memory fake does not establish database persistence.
3. **Modify:** Add a rejected request and inspect that state remains unchanged.
4. **Debug:** Find a globally shared Session in a request dependency.

<details>
<summary>Hints</summary>

Close/dispose each test application's database resources after its client is finished.

</details>

## Independent task: http & database integration tests

In `Practice/07_HTTP_And_Database_Integration_Tests.py`, complete this task:

Implement a small `create_app(path)` with an SQLAlchemy SQLite orders table and POST/GET routes. Validate nonblank item and positive strict integer quantity. Prepare the isolated test schema inside the factory for this exercise only. Use request-scoped sessions and committed writes.

Write pytest tests using tmp_path and TestClient for create/read across a fresh app instance at the same path, quantity-zero rejection (422), and missing ID (404). Expected behavior: all three tests pass against real file-backed storage. The migration capstone uses revisions instead of this test initializer.
