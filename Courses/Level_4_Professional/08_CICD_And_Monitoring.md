# Lesson 8: CI/CD, Code Quality & Production Deployment

Shipping professional software requires automated pipelines that verify code formatting, linting, type safety, test suites, and zero-downtime deployment.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Enforce automated code formatting and linting with **Ruff** and **Black**.
2. Run static type checking in CI with **Mypy**.
3. Build automated continuous integration pipelines with **GitHub Actions**.
4. Configure production ASGI servers using **Gunicorn with Uvicorn Workers**.

---

## 1. Automated CI Pipeline with GitHub Actions

```yaml
# .github/workflows/ci.yml
name: Continuous Integration

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff mypy pytest pytest-cov -r requirements.txt

      - name: Lint with Ruff
        run: ruff check .

      - name: Type check with Mypy
        run: mypy .

      - name: Run Test Suite with Pytest
        run: pytest --cov=. --cov-report=xml
```

---

## 2. Production Process Management (Gunicorn + Uvicorn)

Run multi-worker processes behind a reverse proxy (like Nginx / Cloudflare):

```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile -
```

---

## 📝 Quick Exercise

**Prompt**:
Configure `pyproject.toml` settings for `ruff` and `pytest` with a minimum test coverage threshold of 85%.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
ignore = []

[tool.pytest.ini_options]
minversion = "7.0"
addopts = "-ra -q --cov=. --cov-fail-under=85"
testpaths = ["tests"]
```
</details>
