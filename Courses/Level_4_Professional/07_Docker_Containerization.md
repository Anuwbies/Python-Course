# Lesson 7: Containerization & Docker for Python Applications

Containerization packages an application, Python interpreter, system libraries, and dependencies into an immutable image that runs identically anywhere.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Write production-ready, multi-stage `Dockerfile`s for Python.
2. Minimize container image sizes and remove root security vulnerabilities.
3. Orchestrate multi-container setups (FastAPI + PostgreSQL + Redis) with `docker-compose.yml`.
4. Manage persistent database volumes and environment variables.

---

## 1. Production-Grade Multi-Stage Dockerfile

```dockerfile
# Stage 1: Build dependencies in a virtual environment
FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

COPY requirements.txt .
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: Minimal runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy only the compiled virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create non-root user for security
RUN useradd -m -u 1000 appuser
USER appuser

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 2. Multi-Service Orchestration (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

---

## 📝 Quick Exercise

**Prompt**:
Create a `docker-compose.yml` file that includes a FastAPI service, PostgreSQL database, and a Celery worker service sharing the same codebase.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```yaml
version: '3.8'

services:
  api:
    build: .
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  worker:
    build: .
    command: celery -A tasks.celery_app worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```
</details>
