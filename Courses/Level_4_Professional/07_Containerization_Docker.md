# Lesson 7: Production Containerization: Docker & Multi-Service Orchestration

In enterprise software engineering, the classic excuse *"it works on my machine"* is unacceptable. **Docker** packages an application alongside its exact Python runtime, OS dependencies, system libraries, and configuration into lightweight, reproducible, and immutable **Containers**. In this lesson, you will master production multi-stage `Dockerfile` construction, container security, `.dockerignore` hygiene, and multi-service orchestration using **Docker Compose**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the architectural difference between **Virtual Machines (Hypervisors)** and **Containers (OS Namespaces/cgroups)**.
2. Build minimal, secure **Multi-Stage Dockerfiles** that eliminate compiler bloat from production images.
3. Apply container security best practices (non-root `appuser` execution, read-only filesystems).
4. Author comprehensive `.dockerignore` files to prevent secret leakage and cache invalidation.
5. Orchestrate full-stack multi-container topologies (**FastAPI + PostgreSQL + Redis + Celery**) with `docker-compose.yml`.
6. Configure container Healthchecks, Volume persistence, and isolated Bridge Networks.

---

## 1. Multi-Stage Production `Dockerfile`

Multi-stage builds split image creation into a temporary **Builder Stage** (which installs wheels and compiler tools) and a lean **Runtime Stage** (containing only the bare minimum runtime artifacts):

```dockerfile
# ----------------------------------------------------
# Stage 1: Build & Dependency Compilation
# ----------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ----------------------------------------------------
# Stage 2: Final Secure Production Runtime
# ----------------------------------------------------
FROM python:3.12-slim AS runtime

WORKDIR /app

# Security: Create unprivileged system user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

# Copy installed Python packages from builder stage
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# Copy application source code
COPY --chown=appuser:appgroup ./app /app

# Switch to non-root user
USER appuser

EXPOSE 8000

# Health check to ensure API responsiveness
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

---

## 4. Docker Layer Caching & Build Optimization

Docker builds images as a stack of read-only layers. If a layer hasn't changed, Docker reuses the cached layer:
- ❌ **Anti-Pattern**: `COPY . .` followed by `RUN pip install -r requirements.txt` (any source code change invalidates the pip install cache, causing slow 5-minute rebuilds).
- ✅ **Optimized Order**:
  1. `COPY requirements.txt .`
  2. `RUN pip install -r requirements.txt` (Cached as long as requirements don't change!)
  3. `COPY ./app /app` (Only fast app layer rebuilds on code edits).

---

## 5. Under the Hood: Linux Cgroups & Namespaces

Containers are not lightweight virtual machines; they are standard OS processes isolated by kernel features:
- **Namespaces**: Provide process isolation (`PID` namespace hides other processes; `NET` namespace gives isolated virtual network interfaces; `MNT` isolates the filesystem).
- **Cgroups (Control Groups)**: Enforce hardware resource limits (e.g. `deploy.resources.limits.cpus: "2.0"` and `memory: "1GB"`).

---

## 6. The PID 1 Zombie Reaping Problem & `tini`

When a Python script runs as `PID 1` in a container, it does not inherit default OS init system behavior—it fails to reap orphaned child processes (creating zombie processes) and may ignore `SIGTERM` shutdown signals from Docker/Kubernetes. Use an init helper like **`tini`** or `dumb-init`:

```dockerfile
RUN apt-get update && apt-get install -y tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "main.py"]
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master Dockerfiles, caching, multi-stage builds, compose orchestration, and container security:

---

### 🟢 Tier 1: Basic Dockerfile & Build Context (Exercises 1–3)

#### 🔹 Exercise 1: Single-Stage Python Dockerfile
* **Goal**: Write a `Dockerfile` for a Flask/FastAPI app setting `WORKDIR /app` and `EXPOSE 8000`.

#### 🔹 Exercise 2: Comprehensive `.dockerignore`
* **Goal**: Author `.dockerignore` excluding `.git`, `.venv`, `__pycache__`, and `.env`.

#### 🔹 Exercise 3: Docker Layer Cache Verification
* **Goal**: Structure a `Dockerfile` separating dependency installation from application source copying.

---

### 🟡 Tier 2: Multi-Stage Builds & Security (Exercises 4–6)

#### 🔹 Exercise 4: Multi-Stage C-Extension Build
* **Goal**: Compile C dependencies (`gcc`, `libpq-dev`) in a builder stage and copy clean wheels to runtime.

#### 🔹 Exercise 5: Non-Root System User (`USER appuser`)
* **Goal**: Create an unprivileged user/group (`appuser:1001`) and run the container securely.

#### 🔹 Exercise 6: Container `HEALTHCHECK` Instruction
* **Goal**: Add a `HEALTHCHECK --interval=10s` querying `/health` endpoint.

---

### 🟠 Tier 3: Docker Compose & Orchestration (Exercises 7–9)

#### 🔹 Exercise 7: Multi-Service Compose Setup
* **Goal**: Write `docker-compose.yml` linking a web app and Redis with shared bridge networks.

#### 🔹 Exercise 8: Service Startup Dependency Ordering
* **Goal**: Use `depends_on` with `condition: service_healthy` to ensure DB is healthy before app starts.

#### 🔹 Exercise 9: Persistent Volume Configuration
* **Goal**: Configure named volumes for PostgreSQL data persistence across container restarts.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Dockerfile Security Compliance Linter
* **Goal**: Build an automated static analyzer auditing Dockerfile syntax for multi-stage usage, non-root users, and healthchecks.

---

---

## 3. Multi-Service Orchestration with `docker-compose.yml`

```yaml
version: '3.8'

services:
  # 1. FastAPI Web Application
  api:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:secret@db:5432/appdb
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - internal_network

  # 2. Celery Asynchronous Worker
  worker:
    build:
      context: .
      dockerfile: Dockerfile
    command: ["celery", "-A", "tasks", "worker", "--loglevel=info"]
    environment:
      - REDIS_URL=redis://cache:6379/0
    depends_on:
      - cache
    networks:
      - internal_network

  # 3. PostgreSQL Database
  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - internal_network

  # 4. Redis Cache & Message Broker
  cache:
    image: redis:7-alpine
    networks:
      - internal_network

volumes:
  postgres_data:

networks:
  internal_network:
    driver: bridge
```

---

## 💻 Code Example & Reference

The following real-life program models an **Automated Container Topology Verification & Healthcheck Orchestrator Engine**, validating multi-container network wiring, environment variable injection, and non-root user permissions:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Multi-Container Architecture Verification Engine
# =====================================================================

import yaml
import json

class ContainerServiceNode:
    def __init__(self, name: str, image: str, port: int, requires_auth: bool = True):
        self.name = name
        self.image = image
        self.port = port
        self.requires_auth = requires_auth
        self.status = "STOPPED"
        self.user = "root"

    def apply_security_profile(self, run_as_user: str) -> None:
        self.user = run_as_user

    def boot(self) -> bool:
        if self.user == "root":
            print(f"⚠️ [SECURITY WARNING] Service '{self.name}' is booting as ROOT user!")
        self.status = "RUNNING"
        print(f"🐳 [CONTAINER STARTED] {self.name:<18} (Image: {self.image:<20} | Port: {self.port} | User: {self.user})")
        return True

    def healthcheck(self) -> tuple[bool, str]:
        if self.status == "RUNNING":
            return True, f"HTTP 200 OK on port {self.port}"
        return False, "Connection refused"


class DockerComposeClusterOrchestrator:
    def __init__(self, cluster_name: str):
        self.cluster_name = cluster_name
        self.services: dict[str, ContainerServiceNode] = {}
        self.shared_network = "bridge_app_net"

    def register_service(self, service: ContainerServiceNode) -> None:
        self.services[service.name] = service

    def boot_full_stack(self) -> None:
        print("=" * 80)
        print(f"{'DOCKER COMPOSE MULTI-SERVICE ORCHESTRATION BOOT':^80}")
        print("=" * 80)
        print(f"Initializing virtual bridge network: '{self.shared_network}'...")
        
        for name, svc in self.services.items():
            svc.boot()

        print("-" * 80)
        print("EXECUTING CONTAINER HEALTHCHECK PROBES:")
        for name, svc in self.services.items():
            ok, msg = svc.healthcheck()
            tag = "✅ HEALTHY" if ok else "❌ UNHEALTHY"
            print(f"  {svc.name:<20} -> {tag:<12} ({msg})")
        print("=" * 80)


# Assemble Multi-Service Topology
orchestrator = DockerComposeClusterOrchestrator("ApexProductionCluster")

api_svc = ContainerServiceNode("fastapi_web_api", "apex/api:v2.4", 8000)
api_svc.apply_security_profile("appuser:1001") # Non-root security

celery_svc = ContainerServiceNode("celery_worker_01", "apex/worker:v2.4", 0)
celery_svc.apply_security_profile("appuser:1001")

postgres_svc = ContainerServiceNode("postgres_db_replica", "postgres:16-alpine", 5432)
postgres_svc.apply_security_profile("postgres:999")

redis_svc = ContainerServiceNode("redis_message_broker", "redis:7-alpine", 6379)
redis_svc.apply_security_profile("redis:1000")

orchestrator.register_service(api_svc)
orchestrator.register_service(celery_svc)
orchestrator.register_service(postgres_svc)
orchestrator.register_service(redis_svc)

orchestrator.boot_full_stack()
```

### 🔍 Code Explanation:
- **Multi-Stage Security**: Demonstrates enforcing non-root user execution (`appuser:1001`) to protect host operating systems from container escape vulnerabilities.
- **Docker Compose Topology**: Models a 4-tier microservice architecture (`API`, `Worker`, `PostgreSQL`, `Redis`) communicating across a shared bridge network.
- **Automated Healthchecks**: Validates that all dependent services are responding on their assigned container ports before accepting inbound traffic.

---

## 📝 Quick Exercise: Dockerfile Security & Multi-Stage Configuration Parser

### 🏢 Real-Life Scenario
You are developing a static security analysis linter for CI/CD deployment pipelines (such as Hadolint). The linter inspects `Dockerfile` configurations to ensure they satisfy enterprise compliance:
1. Uses multi-stage builds (`AS builder` and `AS runtime` or similar).
2. Explicitly specifies an unprivileged non-root user (`USER <non-root>`).
3. Defines a container `HEALTHCHECK` instruction.

### 📋 Requirements
1. **Define `audit_dockerfile_security(dockerfile_text: str) -> dict`**:
   - Checks:
     - `has_multistage`: `True` if `FROM` keyword appears more than once.
     - `has_non_root_user`: `True` if `USER` keyword appears with a non-root name.
     - `has_healthcheck`: `True` if `HEALTHCHECK` keyword is present.
   - Computes `compliance_score` (out of 100%).
   - Returns dictionary of audit results.
2. Run audit against sample production and insecure Dockerfile strings.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 Docker concepts with Level 1 string analysis, conditionals, and formatted reporting.

### 🎯 Expected Output
```text
==================================================
       DOCKERFILE SECURITY COMPLIANCE AUDIT       
==================================================
Target: Production Multi-Stage Dockerfile
  - Multi-Stage Build: ✅ PASS
  - Non-Root User:     ✅ PASS
  - Healthcheck Rule:  ✅ PASS
  - Compliance Score:  100.0% [PASSED FOR CI/CD DEPLOY]
--------------------------------------------------
Target: Insecure Legacy Single-Stage Dockerfile
  - Multi-Stage Build: ❌ FAIL (Missing Multi-Stage)
  - Non-Root User:     ❌ FAIL (Runs as Root)
  - Healthcheck Rule:  ❌ FAIL (No Healthcheck)
  - Compliance Score:  0.0% [BLOCKED BY SECURITY GUARD]
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Docker Linter & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Dockerfile Security Compliance Linter
# =====================================================================
def audit_dockerfile_security(dockerfile_content: str) -> dict:
    lines = [line.strip() for line in dockerfile_content.splitlines() if line.strip() and not line.startswith("#")]
    
    from_count = sum(1 for line in lines if line.startswith("FROM "))
    has_multistage = from_count > 1
    
    has_non_root = any(line.startswith("USER ") and "root" not in line.lower() for line in lines)
    has_healthcheck = any(line.startswith("HEALTHCHECK ") for line in lines)

    checks_passed = sum([has_multistage, has_non_root, has_healthcheck])
    score = (checks_passed / 3.0) * 100.0

    return {
        "multistage": has_multistage,
        "non_root": has_non_root,
        "healthcheck": has_healthcheck,
        "score": score,
        "approved": score == 100.0
    }


prod_dockerfile = """
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-slim AS runtime
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
USER appuser
HEALTHCHECK CMD python health.py || exit 1
CMD ["uvicorn", "main:app"]
"""

insecure_dockerfile = """
FROM python:3.12
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
"""

print("==================================================")
print("       DOCKERFILE SECURITY COMPLIANCE AUDIT       ")
print("==================================================")

for label, content in [("Production Multi-Stage Dockerfile", prod_dockerfile), ("Insecure Legacy Single-Stage Dockerfile", insecure_dockerfile)]:
    res = audit_dockerfile_security(content)
    verdict = "[PASSED FOR CI/CD DEPLOY]" if res["approved"] else "[BLOCKED BY SECURITY GUARD]"
    print(f"Target: {label}")
    print(f"  - Multi-Stage Build: {'✅ PASS' if res['multistage'] else '❌ FAIL (Missing Multi-Stage)'}")
    print(f"  - Non-Root User:     {'✅ PASS' if res['non_root'] else '❌ FAIL (Runs as Root)'}")
    print(f"  - Healthcheck Rule:  {'✅ PASS' if res['healthcheck'] else '❌ FAIL (No Healthcheck)'}")
    print(f"  - Compliance Score:  {res['score']:.1f}% {verdict}")
    print("--------------------------------------------------")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Basic Dockerfile
# FROM python:3.12-slim; WORKDIR /app; COPY . .; CMD ["python", "main.py"]

# Ex 2: .dockerignore
# .git\n.venv\n__pycache__\n.env

# Ex 3: Cache Separation
# COPY req.txt .; RUN pip install -r req.txt; COPY src/ /app/

# Ex 4: Multi-Stage C-Ext
# FROM python:3.12 AS builder; RUN pip install psycopg2 ... FROM python:3.12-slim AS runtime

# Ex 5: Non-Root User
# RUN useradd -u 8888 appuser; USER appuser

# Ex 6: Healthcheck
# HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1

# Ex 7: Docker Compose Services
# services: web: { build: . }, redis: { image: redis:alpine }

# Ex 8: depends_on condition
# depends_on: db: { condition: service_healthy }

# Ex 9: Volumes
# volumes: pg_data: {}
```
</details>
