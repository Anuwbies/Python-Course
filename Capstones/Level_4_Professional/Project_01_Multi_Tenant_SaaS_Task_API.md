# Capstone Project 4.1: Multi-Tenant SaaS Project Management API

## 📌 Project Overview
Architect and implement a production-ready, cloud-native **Multi-Tenant Project Management REST API** (similar to Jira or Linear) using FastAPI, SQLAlchemy 2.0 Async, PostgreSQL, Redis, Alembic, and Docker. The platform features strict tenant data isolation, Role-Based Access Control (RBAC), subscription plan limits, Redis token-bucket rate limiting, and an automated CI/CD test pipeline.

---

## 🎯 Learning Objectives
- **Multi-Tenant Architecture**: Implementing tenant data isolation at the ORM/database layer via tenant foreign keys and automated query scoping.
- **FastAPI & Async SQLAlchemy 2.0**: Writing scalable async endpoints with dependency injection (`Depends`), async sessions, and select expressions.
- **Data Validation & Serialization**: Using Pydantic v2 schemas for strict request/response data filtering and validation.
- **Authentication & RBAC**: Issuing and verifying JWT bearer tokens with organization-level roles (`Owner`, `Admin`, `Member`, `Viewer`).
- **Database Migrations**: Managing evolving database schemas using Alembic.
- **Redis Rate Limiting**: Protecting tenant API quotas using Redis sliding window counters.

---

## 🏗️ System Architecture

```text
                                [ Client HTTP / JSON ]
                                          |
                                          v
                              [ FastAPI Gateway Router ]
                                          |
            +-----------------------------+-----------------------------+
            |                             |                             |
            v                             v                             v
   [ Auth & Tenant Middleware ]   [ Rate Limiter (Redis) ]      [ RBAC Guard (Depends) ]
            |                             |                             |
            +-----------------------------+-----------------------------+
                                          |
                                          v
                               [ Business Service Layer ]
                                          |
                        +-----------------+-----------------+
                        |                                   |
                        v                                   v
          [ PostgreSQL Database (Async) ]          [ Redis Cache / Quotas ]
          - tenants / organizations                - token buckets
          - users / memberships                    - session tokens
          - projects / tasks / labels
```

---

## 📋 Functional Requirements

### 1. Multi-Tenant Data Isolation
Every data model (`Project`, `Task`, `Comment`, `Label`) belongs to a `tenant_id` (Organization). Users can belong to multiple organizations with distinct roles. All database queries must automatically filter by `tenant_id` to guarantee zero data leakage between organizations.

### 2. Role-Based Access Control (RBAC)
- `Owner`: Full access, manage billing, delete organization, manage user roles.
- `Admin`: Create/Delete projects, invite members, assign tasks.
- `Member`: Create/Edit tasks, assign tasks to self, comment.
- `Viewer`: Read-only access to projects and tasks.

### 3. Core API Endpoints
- `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `POST /api/v1/auth/refresh`
- `POST /api/v1/organizations/` (Create tenant organization)
- `POST /api/v1/organizations/{id}/invite` (Invite user with specific role)
- `GET/POST /api/v1/projects/` (CRUD scoped to tenant)
- `GET/POST/PUT/DELETE /api/v1/tasks/` (Full task workflow with status `TODO`, `IN_PROGRESS`, `DONE`, priority, assignees)
- `GET /api/v1/tasks/analytics` (Aggregation of tasks completed per member)

### 4. Redis Rate Limiter Middleware
Enforce tenant API request limits based on subscription tier:
- Free Tier: 60 requests / minute
- Pro Tier: 1,000 requests / minute
Return HTTP `429 Too Many Requests` with `Retry-After` header when exceeded.

### 5. Docker & CI/CD Pipeline
- Multi-stage `Dockerfile` with slim Python runtime and non-root user.
- `docker-compose.yml` spinning up FastAPI app, PostgreSQL 16, and Redis 7.
- GitHub Actions workflow testing migration scripts, linting, and running full async test suites against live Postgres test containers.

---

## 📐 Phased Implementation Guide

### Phase 1: SQLAlchemy Async Models & Tenant Base
```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Integer, func
import uuid

class Base(DeclarativeBase):
    pass

class TenantModelMixin:
    tenant_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id", ondelete="CASCADE"), index=True)

class Task(Base, TenantModelMixin):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, default="")
    status: Mapped[str] = mapped_column(String(30), default="TODO", index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

### Phase 2: FastAPI Dependency Injection for Tenant Resolution
Extract tenant context from JWT claims or request headers (`X-Tenant-ID`) and inject the active tenant context into route handlers.

### Phase 3: Pydantic v2 Schemas & CRUD Routers
Implement type-safe request validation and response models.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Cross-Tenant Data Leakage** | Tenant A attempts to fetch `GET /tasks/{tenant_b_task_id}` | Returns `404 Not Found` (never reveals entity exists) |
| **RBAC Violation** | `Viewer` sends `DELETE /projects/{id}` | Returns `403 Forbidden` with descriptive permission error |
| **Rate Limit Exceeded** | Send 65 rapid requests on Free tier | Returns `429 Too Many Requests` on request 61 |
| **Expired JWT Token** | Send expired access token in `Authorization: Bearer <token>` | Returns `401 Unauthorized` prompting token refresh |

---

## 🚀 Bonus Challenges
- **Audit Event Log**: Asynchronously publish all CRUD mutations to an audit table or Kafka topic.
- **Full-Text Search**: Implement PostgreSQL `tsvector` full-text search indexing on task descriptions.
