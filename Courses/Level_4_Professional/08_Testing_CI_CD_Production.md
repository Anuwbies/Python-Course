# Lesson 8: Production Testing, CI/CD Pipelines & Deployment

Writing backend code is only half the engineering equation. Production software requires automated Continuous Integration & Continuous Deployment (CI/CD) pipelines that format code, run static type checkers, execute asynchronous integration tests with database isolation, and build verified artifacts on every `git push`. In this milestone lesson of Level 4, you will master **Async Integration Testing with `pytest-asyncio` & `httpx`**, modern linting with **Ruff**, and automated **GitHub Actions CI/CD Workflows**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Write asynchronous integration tests for FastAPI backends using **`pytest-asyncio`** and **`httpx.AsyncClient`**.
2. Isolate test database state using transactional rollback fixtures.
3. Enforce code quality, style, and linting rules using **Ruff**.
4. Perform automated static type analysis across continuous integration using **`mypy`**.
5. Author complete **GitHub Actions CI/CD Workflows** (`.github/workflows/ci.yml`) that automate linting, testing, and container deployment.

---

## 1. Async Integration Testing with `httpx.AsyncClient`

FastAPI endpoints can be tested asynchronously without binding to a physical TCP socket port by mounting the application directly to an `httpx.AsyncClient`:

```python
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from main import app # Your FastAPI application

@pytest_asyncio.fixture
async def async_client():
    """Provides an isolated async HTTP test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_create_user_endpoint(async_client: AsyncClient):
    payload = {"username": "erostova", "email": "elena@enterprise.com", "role": "ADMIN", "age": 28}
    response = await async_client.post("/api/v1/users", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "erostova"
    assert "user_id" in data
```

---

---

## 4. Sub-Second Test Database Isolation: Transactional Rollback Fixtures

Creating and dropping database tables for every test is prohibitively slow. Instead, modern production test suites start a database transaction before each test, run the test, and execute a **Rollback** on teardown so no state is ever permanently committed:

```python
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.fixture
async def db_session(async_engine):
    """Wraps each test in an isolated rollback transaction."""
    async with async_engine.connect() as conn:
        trans = await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False)
        yield session
        await session.close()
        await trans.rollback() # Instant cleanup: 0 disk I/O!
```

---

## 5. Matrix Builds in GitHub Actions (`strategy.matrix`)

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    steps:
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
```

---

## 6. Blue-Green vs Canary Deployment Strategies

- **Blue-Green Deployment**: Two identical environments (Blue = Live, Green = Idle). Deploy new version to Green, run smoke tests, then switch router traffic from Blue to Green instantly.
- **Canary Deployment**: Route 5% of live traffic to the new version. Monitor error rates in Prometheus/Datadog for 15 minutes; automatically promote to 100% or roll back.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master pytest-asyncio, HTTPX testing, transactional rollback fixtures, CI/CD matrices, and zero-downtime deployments:

---

### 🟢 Tier 1: Unit & Async Test Basics (Exercises 1–3)

#### 🔹 Exercise 1: Basic Async Test with `pytest.mark.asyncio`
* **Goal**: Write an async test function verifying a coroutine return value.

#### 🔹 Exercise 2: HTTPX Mock Client Setup
* **Goal**: Mount a FastAPI app to `httpx.AsyncClient(transport=ASGITransport(app=app))` and test `GET /health`.

#### 🔹 Exercise 3: Pytest Parametrized Tests (`@pytest.mark.parametrize`)
* **Goal**: Test tax calculations across 5 different income bracket inputs.

---

### 🟡 Tier 2: Fixtures, Mocking & Status Codes (Exercises 4–6)

#### 🔹 Exercise 4: Autouse Fixture for Environment Variables
* **Goal**: Set `monkeypatch.setenv("ENV", "TESTING")` across all tests automatically.

#### 🔹 Exercise 5: Mocking External HTTP API Calls (`respx` / `unittest.mock`)
* **Goal**: Mock an outbound Stripe payment endpoint returning 200 OK without hitting external networks.

#### 🔹 Exercise 6: Testing 422 Unprocessable Entity Validation
* **Goal**: Send an invalid JSON body (e.g. `age: -5`) and assert `response.status_code == 422`.

---

### 🟠 Tier 3: Database Isolation & CI/CD Pipelines (Exercises 7–9)

#### 🔹 Exercise 7: Transactional Rollback Test Fixture
* **Goal**: Write a fixture that rolls back SQL inserts after each test to maintain clean tables.

#### 🔹 Exercise 8: GitHub Actions Workflow with Service Containers
* **Goal**: Author `.github/workflows/ci.yml` running Postgres and Redis service containers.

#### 🔹 Exercise 9: Code Coverage Gate (`pytest-cov`)
* **Goal**: Configure CI to fail if test code coverage drops below 90% (`--cov-fail-under=90`).

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: E-Commerce Checkout API Async Integration Test Suite
* **Goal**: Build an end-to-end asynchronous test suite verifying status codes, schema validation, and order state persistence.

---

---

## 3. GitHub Actions CI/CD Workflow (`.github/workflows/ci.yml`)

```yaml
name: Enterprise CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: testuser
          POSTGRES_PASSWORD: testpassword
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff mypy pytest pytest-asyncio httpx -r requirements.txt

      - name: Lint and Format Check (Ruff)
        run: ruff check .

      - name: Static Type Checking (mypy)
        run: mypy app/ --strict

      - name: Run Automated Async Integration Tests (Pytest)
        env:
          DATABASE_URL: postgresql+asyncpg://testuser:testpassword@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379/0
        run: pytest -v --cov=app --cov-report=term-missing
```

---

## 💻 Code Example & Reference

The following real-life program models an **End-to-End Asynchronous API Integration Test & CI/CD Verification Runner**, executing automated test cases against a mock FastAPI application with request verification and assertion audits:

```python
# =====================================================================
# REAL-WORLD SYSTEM: E2E Async API Integration Test Suite & CI Runner
# =====================================================================

import asyncio
from datetime import datetime

# 1. Mock FastAPI Application & In-Memory Database
class MockFastAPIApp:
    def __init__(self):
        self.db: dict[str, dict] = {}
        self.seq = 100

    async def handle_request(self, method: str, path: str, json_body: dict = None, headers: dict = None) -> tuple[int, dict]:
        # Emulate routing & middleware
        if path == "/api/v1/health":
            return 200, {"status": "HEALTHY", "timestamp": datetime.utcnow().isoformat()}

        if method == "POST" and path == "/api/v1/merchants":
            auth = (headers or {}).get("Authorization", "")
            if auth != "Bearer secret_ci_admin_key":
                return 401, {"error": "Unauthorized"}
            
            if not json_body or "name" not in json_body or "email" not in json_body:
                return 422, {"error": "Validation Error: 'name' and 'email' required"}

            self.seq += 1
            merchant_id = f"MERCH-{self.seq}"
            record = {"id": merchant_id, "name": json_body["name"], "email": json_body["email"], "status": "ACTIVE"}
            self.db[merchant_id] = record
            return 201, record

        if method == "GET" and path.startswith("/api/v1/merchants/"):
            m_id = path.split("/")[-1]
            if m_id not in self.db:
                return 404, {"error": "Merchant not found"}
            return 200, self.db[m_id]

        return 404, {"error": "Route not found"}


# 2. Automated Async Integration Test Suite (Lesson 8)
class TestMerchantIntegrationSuite:
    def __init__(self, app: MockFastAPIApp):
        self.app = app

    async def test_healthcheck_endpoint(self):
        status_code, body = await self.app.handle_request("GET", "/api/v1/health")
        assert status_code == 200, f"Expected 200, got {status_code}"
        assert body["status"] == "HEALTHY"
        return "test_healthcheck_endpoint: PASSED"

    async def test_create_merchant_unauthorized(self):
        status_code, body = await self.app.handle_request("POST", "/api/v1/merchants", json_body={"name": "Test"})
        assert status_code == 401, f"Expected 401 Unauthorized, got {status_code}"
        return "test_create_merchant_unauthorized: PASSED"

    async def test_create_and_fetch_merchant_lifecycle(self):
        auth_headers = {"Authorization": "Bearer secret_ci_admin_key"}
        payload = {"name": "Apex Global Holdings", "email": "billing@apexholdings.com"}
        
        # Create
        status_code, created = await self.app.handle_request("POST", "/api/v1/merchants", json_body=payload, headers=auth_headers)
        assert status_code == 201, f"Expected 201 Created, got {status_code}"
        assert created["name"] == "Apex Global Holdings"
        merchant_id = created["id"]

        # Fetch
        fetch_code, fetched = await self.app.handle_request("GET", f"/api/v1/merchants/{merchant_id}")
        assert fetch_code == 200
        assert fetched["email"] == "billing@apexholdings.com"
        return "test_create_and_fetch_merchant_lifecycle: PASSED"


# 3. CI/CD Pipeline Orchestrator Execution
async def run_ci_cd_pipeline():
    print("=" * 75)
    print(f"{'GITHUB ACTIONS CI/CD PIPELINE SIMULATION':^75}")
    print("=" * 75)
    print("🚀 [JOB: lint-and-test] Starting automated quality gates...")
    print("  ✓ Step 1: Ruff Lint Check -> Passed (0 errors, 0 warnings)")
    print("  ✓ Step 2: Mypy Strict Type Analysis -> Passed (Success: no issues found)")
    print("  ✓ Step 3: Initializing Test Database & Async HTTP Client Fixtures...")
    print("-" * 75)

    app = MockFastAPIApp()
    suite = TestMerchantIntegrationSuite(app)

    tests = [
        suite.test_healthcheck_endpoint(),
        suite.test_create_merchant_unauthorized(),
        suite.test_create_and_fetch_merchant_lifecycle(),
    ]

    results = await asyncio.gather(*tests)
    for r in results:
        print(f"  🧪 {r}")

    print("-" * 75)
    print("ALL QUALITY GATES PASSED (100% Code Coverage) ✅")
    print("📦 Docker Image 'apex/api:v2.4' Built and Pushed to Registry Successfully!")
    print("=" * 75)

if __name__ == "__main__":
    asyncio.run(run_ci_cd_pipeline())
```

### 🔍 Code Explanation:
- **Async Test Execution**: Emulates `pytest-asyncio` running non-blocking HTTP requests across API route lifecycles.
- **Security & Lifecycle Testing**: Validates authorization guards, payload schema compliance, and end-to-end create-then-fetch operations.
- **CI/CD Quality Gates**: Simulates the full lint $\to$ type check $\to$ test $\to$ container build pipeline required in modern engineering organizations.

---

## 📝 Quick Exercise: API Integration Test Suite with Mock Database Fixtures

### 🏢 Real-Life Scenario
You are developing the integration test suite for an e-commerce checkout API. You must write an async test suite that verifies:
1. Fetching a non-existent order returns HTTP 404.
2. Placing an order with missing items returns HTTP 422.
3. Placing a valid order returns HTTP 201 with an assigned order ID.

### 📋 Requirements
1. **Define Mock Order API Router**:
   - `GET /orders/{order_id}`: Returns 200 if found in `orders_db`, else 404.
   - `POST /orders`: Expects `{"customer_id": str, "items": list}`. If `items` is empty, returns 422; otherwise returns 201 with `{"order_id": "ORD-99", "status": "CONFIRMED"}`.
2. **Write Async Test Functions**:
   - `test_get_nonexistent_order()`
   - `test_create_order_empty_items_validation()`
   - `test_create_order_success()`
3. Run all tests and print the CI test execution summary.

> [!IMPORTANT]
> **Cumulative Level 4 Milestone Constraint**: Combine Level 4 async API testing and status codes with Level 3 asyncio, Level 2 assert testing patterns, and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        ORDER API INTEGRATION TEST SUITE          
==================================================
  ✓ test_get_nonexistent_order:             PASSED (404 Not Found Verified)
  ✓ test_create_order_empty_items_validation:PASSED (422 Unprocessable Verified)
  ✓ test_create_order_success:               PASSED (201 Created Verified)
--------------------------------------------------
ALL 3 INTEGRATION TESTS PASSED (100% GREEN) ✅
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Order API Test & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Order API Integration Test Suite
# =====================================================================
import asyncio

class MockOrderAPI:
    def __init__(self):
        self.orders = {}
        self.counter = 98

    async def handle_request(self, method: str, path: str, payload: dict = None) -> tuple[int, dict]:
        if method == "GET" and path.startswith("/orders/"):
            o_id = path.split("/")[-1]
            if o_id not in self.orders:
                return 404, {"error": "Order not found"}
            return 200, self.orders[o_id]

        if method == "POST" and path == "/orders":
            if not payload or not payload.get("items"):
                return 422, {"error": "Items cannot be empty"}
            self.counter += 1
            order_id = f"ORD-{self.counter}"
            record = {"order_id": order_id, "status": "CONFIRMED", "customer_id": payload["customer_id"]}
            self.orders[order_id] = record
            return 201, record

        return 404, {"error": "Not found"}


async def run_order_test_suite():
    api = MockOrderAPI()

    c1, _ = await api.handle_request("GET", "/orders/ORD-NONEXISTENT")
    assert c1 == 404

    c2, _ = await api.handle_request("POST", "/orders", {"customer_id": "CUST-01", "items": []})
    assert c2 == 422

    c3, b3 = await api.handle_request("POST", "/orders", {"customer_id": "CUST-01", "items": ["Item A"]})
    assert c3 == 201
    assert b3["order_id"] == "ORD-99"

    print("==================================================")
    print("        ORDER API INTEGRATION TEST SUITE          ")
    print("==================================================")
    print("  ✓ test_get_nonexistent_order:             PASSED (404 Not Found Verified)")
    print("  ✓ test_create_order_empty_items_validation:PASSED (422 Unprocessable Verified)")
    print("  ✓ test_create_order_success:               PASSED (201 Created Verified)")
    print("--------------------------------------------------")
    print("ALL 3 INTEGRATION TESTS PASSED (100% GREEN) ✅")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(run_order_test_suite())

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: pytest.mark.asyncio
# @pytest.mark.asyncio async def test_sample(): res = await fetch_data(); assert res == 100

# Ex 2: HTTPX client
# async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac: ...

# Ex 3: Parametrize
# @pytest.mark.parametrize("inc,expected", [(10, 1), (50, 5), (100, 10)])

# Ex 4: Monkeypatch env
# @pytest.fixture(autouse=True) def set_env(monkeypatch): monkeypatch.setenv("ENV", "TEST")

# Ex 5: Mock outbound API
# with mock.patch("httpx.AsyncClient.post", return_value=Response(200)): ...

# Ex 6: Status 422 assertion
# res = await client.post("/items", json={"invalid": True}); assert res.status_code == 422

# Ex 7: Transaction Rollback Fixture
# @pytest.fixture async def db(engine): conn = await engine.connect(); t = await conn.begin(); yield; await t.rollback()

# Ex 8: Matrix CI Workflow
# strategy: matrix: python-version: ["3.11", "3.12"]

# Ex 9: Coverage threshold
# pytest --cov=app --cov-fail-under=90
```
</details>
