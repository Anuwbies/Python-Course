# Lesson 6: Background Workers & Distributed Task Queues (Celery & Redis)

Long-running jobs (video processing, email sending, PDF invoice generation) should never block an HTTP request. In this lesson, you will master background task queues using **Celery** and **Redis**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the Producer-Broker-Consumer architecture.
2. Use Redis as a high-speed message broker.
3. Define and trigger asynchronous tasks using **Celery**.
4. Schedule recurring periodic background tasks with **Celery Beat** (cron jobs).

---

## 1. Celery Architecture & Worker Definition

```python
# tasks.py
from celery import Celery
import time

# Configure Celery with Redis broker
celery_app = Celery(
    "worker_service",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

@celery_app.task
def send_welcome_email(user_email: str) -> str:
    print(f"📨 Processing email to {user_email} in background worker...")
    time.sleep(3) # Simulating email API delay
    return f"Email sent successfully to {user_email}"
```

```python
# main.py (FastAPI Route)
from fastapi import FastAPI
from tasks import send_welcome_email

app = FastAPI()

@app.post("/register")
async def register(email: str):
    # Enqueue background task asynchronously without blocking HTTP response!
    task = send_welcome_email.delay(email)
    return {"message": "Account created!", "task_id": task.id}
```

---

## 📝 Quick Exercise

**Prompt**:
Write a Celery task `generate_monthly_report_pdf(user_id)` that simulates generating a heavy PDF report and stores the result in Redis.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from celery import Celery
import time

celery_app = Celery("reports", broker="redis://localhost:6379/0", backend="redis://localhost:6379/1")

@celery_app.task(bind=True, max_retries=3)
def generate_monthly_report_pdf(self, user_id: int):
    try:
        print(f"📄 Compiling financial PDF for user {user_id}...")
        time.sleep(4) # Simulate report generation
        pdf_path = f"/storage/reports/report_user_{user_id}_2026.pdf"
        return {"user_id": user_id, "pdf_path": pdf_path, "status": "COMPLETED"}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)
```
</details>
