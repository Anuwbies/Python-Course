# 🔵 Level 4: Professional Capstone Projects

Welcome to the **Level 4 Professional Testing Capstones**! These projects test production-grade backend engineering, microservices, async database persistence with SQLAlchemy/PostgreSQL, database migrations with Alembic, distributed task queues with Celery/Redis, containerization with Docker, and CI/CD pipelines.

---

## 📚 Available Projects

| Project | Domain | Key Concepts Tested | Difficulty | Specification |
| :--- | :--- | :--- | :---: | :--- |
| **01: Multi-Tenant SaaS Project Management API** | Enterprise SaaS / Cloud | Multi-Tenancy Data Isolation, FastAPI, SQLAlchemy 2.0 Async, Pydantic v2, RBAC, Redis Rate Limiting | 🔵 Professional | [Project 01 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_4_Professional/Project_01_Multi_Tenant_SaaS_Task_API.md) |
| **02: Real-Time Chat & Notification Microservice** | Real-Time Systems / Messaging | FastAPI WebSockets, Redis Pub/Sub Message Broker, Celery Email Workers, PostgreSQL Persistence | 🔵 Professional | [Project 02 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_4_Professional/Project_02_Real_Time_Chat_WebSocket_Service.md) |
| **03: Distributed Media Storage & Processing API** | Cloud Infrastructure / Storage | S3 / MinIO Storage, Async Chunked Uploads, Celery Image Transcoding, Docker Compose, CI/CD | 🔵 Professional | [Project 03 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_4_Professional/Project_03_Distributed_File_Storage_Metadata_Engine.md) |

---

## 🎯 Learning Evaluation Rubric
When implementing any Level 4 project, ensure your solution satisfies:
- **Clean Architecture & Layering**: Separation of Routers, Service Layer, Repositories, Schemas (Pydantic), and Database Models.
- **Security & Authorization**: Strict password hashing (`argon2`/`bcrypt`), JWT validation with scopes/roles, and SQL injection prevention via ORM parameterization.
- **Production Readiness**: Automated Alembic migrations, health check endpoints (`/healthz`), centralized logging, and environment variable configuration (`pydantic-settings`).
- **Containerization & CI**: Multi-stage `Dockerfile`, `docker-compose.yml`, and GitHub Actions workflow testing.
