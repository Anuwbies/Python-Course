# Lesson 6: Distributed Task Queues: Celery, Redis & Asynchronous Workers

In production web applications, long-running operations—such as video rendering, sending thousands of customer notification emails, generating large PDF invoices, or executing machine learning pipelines—must never block synchronous HTTP request-response cycles. Instead, web servers offload these jobs to background worker queues. In this lesson, you will master distributed asynchronous task architectures using **Celery** and **Redis**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master the **Producer-Broker-Consumer Architecture** for distributed computing.
2. Configure **Redis** as both an in-memory message broker and a task result backend.
3. Define and dispatch background tasks using Celery's `@app.task` decorator and `.delay()` method.
4. Track task execution states (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`) and retrieve asynchronous results (`AsyncResult`).
5. Implement automatic retry mechanisms with exponential backoff for flaky external network calls.
6. Schedule recurring periodic background tasks using **Celery Beat**.

---

## 1. Producer-Broker-Consumer Architecture

```
┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
│ Web API Server  │ ──.delay()──>   Redis Broker  │ ──Task Q──> │  Celery Worker  │
│   (Producer)    │           │ (Message Queue) │           │   (Consumer)    │
└─────────────────┘           └─────────────────┘           └─────────────────┘
         ▲                                                           │
         │                                                           ▼
         └───────────── Queries AsyncResult ───────────────── Result Backend
```

---

## 2. Celery Application Setup & Task Definitions

```python
from celery import Celery
import time

# Configure Celery with Redis broker and result backend
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

# Celery Task definition
@celery_app.task(bind=True, max_retries=3, default_retry_delay=5)
def send_marketing_campaign_email(self, user_email: str, subject: str, body: str):
    """Asynchronous background worker task."""
    try:
        print(f"📧 [Worker] Sending email to {user_email}...")
        time.sleep(1.0) # Simulate slow SMTP network transmission
        return {"status": "DELIVERED", "recipient": user_email, "timestamp": time.time()}
    except Exception as exc:
        # Automatic retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)
```

---

## 3. Dispatching & Polling Tasks from Web APIs

```python
# In FastAPI route handler:
@app.post("/campaigns/send")
async def trigger_campaign(email: str):
    # .delay() immediately enqueues the task into Redis and returns in 1 millisecond!
    async_task = send_marketing_campaign_email.delay(email, "Welcome to Apex", "Hello!")
    
    # Return immediate 202 Accepted HTTP response to client:
    return {"status": "QUEUED", "task_id": async_task.id}

@app.get("/tasks/{task_id}")
async def check_task_status(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "state": task_result.state, # PENDING, SUCCESS, FAILURE
        "result": task_result.result if task_result.ready() else None
    }
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Asynchronous Media Ingestion & Distributed Video Transcoding Queue Engine**, simulating a Redis broker, task state management, retries with exponential backoff, and asynchronous polling:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Distributed Media Transcoding & Queue Worker Engine
# =====================================================================

import time
import uuid
from collections import deque
from typing import Callable

class SimulatedRedisBroker:
    """In-memory Redis message broker and key-value state backend."""
    def __init__(self):
        self._queue = deque() # Broker FIFO Queue
        self._backend: dict[str, dict] = {} # Result Backend Store

    def enqueue_task(self, task_payload: dict) -> None:
        self._queue.append(task_payload)
        self._backend[task_payload["task_id"]] = {
            "task_id": task_payload["task_id"],
            "task_name": task_payload["task_name"],
            "state": "PENDING",
            "result": None,
            "error": None
        }

    def pop_task(self) -> dict | None:
        return self._queue.popleft() if self._queue else None

    def update_state(self, task_id: str, state: str, result: any = None, error: str = None) -> None:
        if task_id in self._backend:
            self._backend[task_id]["state"] = state
            self._backend[task_id]["result"] = result
            self._backend[task_id]["error"] = error

    def get_task_result(self, task_id: str) -> dict | None:
        return self._backend.get(task_id)


class CeleryWorkerPool:
    """Worker node consuming and executing tasks from Redis broker."""
    def __init__(self, broker: SimulatedRedisBroker):
        self.broker = broker
        self._task_registry: dict[str, Callable] = {}

    def register_task(self, name: str, fn: Callable) -> None:
        self._task_registry[name] = fn

    def process_all_queued_tasks(self) -> None:
        while True:
            task = self.broker.pop_task()
            if not task:
                break

            task_id = task["task_id"]
            name = task["task_name"]
            args = task["args"]

            self.broker.update_state(task_id, "STARTED")
            print(f"⚙️ [WORKER RUNNING] Task: {name} (ID: {task_id[:8]}...)")

            fn = self._task_registry.get(name)
            try:
                result = fn(*args)
                self.broker.update_state(task_id, "SUCCESS", result=result)
                print(f"✅ [WORKER SUCCESS] Task {task_id[:8]} -> Result: {result}")
            except Exception as ex:
                self.broker.update_state(task_id, "FAILURE", error=str(ex))
                print(f"❌ [WORKER FAILURE] Task {task_id[:8]} -> Error: {ex}")


# Define Distributed Background Tasks
def transcode_video_task(filename: str, target_resolution: str) -> dict:
    # Simulate heavy compute transcoding
    time.sleep(0.05)
    return {
        "output_file": f"{filename.split('.')[0]}_{target_resolution}.mp4",
        "resolution": target_resolution,
        "codec": "H.264",
        "duration_sec": 124.5
    }

def generate_pdf_report_task(client_name: str, quarter: str) -> dict:
    time.sleep(0.02)
    return {"pdf_url": f"https://cdn.enterprise.com/reports/{client_name}_{quarter}.pdf", "pages": 18}


# Execution Simulation
broker = SimulatedRedisBroker()
worker = CeleryWorkerPool(broker)
worker.register_task("transcode_video", transcode_video_task)
worker.register_task("generate_pdf", generate_pdf_report_task)

print("=" * 75)
print(f"{'DISTRIBUTED CELERY & REDIS TASK PIPELINE SIMULATION':^75}")
print("=" * 75)

# Producer: Fast non-blocking web server enqueueing jobs
def dispatch_async(task_name: str, *args) -> str:
    tid = str(uuid.uuid4())
    broker.enqueue_task({"task_id": tid, "task_name": task_name, "args": args})
    return tid

print("--- PHASE 1: Web Server Enqueues Background Jobs ---")
t1 = dispatch_async("transcode_video", "4k_product_demo.mov", "1080p")
t2 = dispatch_async("generate_pdf", "AlphaCorp", "Q3-2026")
t3 = dispatch_async("transcode_video", "interview.mov", "720p")
print("  -> All 3 jobs enqueued into Redis Broker in 0.2ms!")

print("\n--- PHASE 2: Background Celery Worker Consumes Queue ---")
worker.process_all_queued_tasks()

print("\n--- PHASE 3: Client Checks Task Status from Backend ---")
for tid in (t1, t2, t3):
    res = broker.get_task_result(tid)
    print(f"  Task {tid[:8]}... | State: {res['state']:<8} | Result: {res['result']}")

print("=" * 75)
```

### 🔍 Code Explanation:
- **Producer / Broker Decoupling**: The web application dispatches jobs into the Redis broker in sub-millisecond time, immediately returning a `task_id` to the HTTP caller without waiting.
- **Worker Execution Loop**: Celery workers pull jobs off the queue asynchronously, updating state in the Result Backend upon completion (`SUCCESS` or `FAILURE`).
- **Resilience**: Task failures are tracked in the result backend without crashing the parent web server.

---

## 📝 Quick Exercise: High-Volume Customer Billing PDF Invoicing Task Queue

### 🏢 Real-Life Scenario
You are developing the monthly billing dispatcher for an enterprise SaaS provider. At midnight on the 1st of each month, 10,000 invoices must be generated as PDF documents and emailed to customers. You must design the background worker task that generates invoice PDFs and records results in a task registry.

### 📋 Requirements
1. **Define Task `generate_monthly_invoice_task(customer_id: str, billing_month: str, amount_due: float) -> dict`**:
   - Simulates generating a PDF document.
   - If `amount_due < 0`: Raise `ValueError("Invalid negative invoice amount")`.
   - Returns: `{"invoice_ref": f"INV-{customer_id}-{billing_month}", "amount": amount_due, "pdf_path": f"/storage/invoices/{customer_id}_{billing_month}.pdf"}`.
2. Dispatch 3 customer invoice tasks (including 1 invalid negative amount task).
3. Process the queue and output the task completion report.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 Celery/Redis task patterns with Level 2 custom exceptions and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
       MONTHLY INVOICE BILLING QUEUE RUNNER       
==================================================
⚙️ Processing Task: INV-CUST-101-AUG2026 -> SUCCESS: $1,250.00
⚙️ Processing Task: INV-CUST-102-AUG2026 -> FAILURE: Invalid negative invoice amount
⚙️ Processing Task: INV-CUST-103-AUG2026 -> SUCCESS: $4,500.00
--------------------------------------------------
Total Invoices Processed: 3
Successfully Generated:   2
Failed Invoices:          1
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Billing Task Definition (Level 4)
def generate_monthly_invoice_task(customer_id: str, billing_month: str, amount_due: float) -> dict:
    if amount_due < 0:
        raise ValueError("Invalid negative invoice amount")
    return {
        "invoice_ref": f"INV-{customer_id}-{billing_month}",
        "amount": amount_due,
        "pdf_path": f"/storage/invoices/{customer_id}_{billing_month}.pdf"
    }


# 2. Queue Simulation Runner
task_queue = [
    ("CUST-101", "AUG2026", 1250.00),
    ("CUST-102", "AUG2026", -50.00), # Failure case
    ("CUST-103", "AUG2026", 4500.00),
]

print("==================================================")
print("       MONTHLY INVOICE BILLING QUEUE RUNNER       ")
print("==================================================")

success_count = 0
fail_count = 0

for cust, month, amt in task_queue:
    ref = f"INV-{cust}-{month}"
    try:
        res = generate_monthly_invoice_task(cust, month, amt)
        success_count += 1
        print(f"⚙️ Processing Task: {ref} -> SUCCESS: ${res['amount']:,.2f}")
    except ValueError as err:
        fail_count += 1
        print(f"⚙️ Processing Task: {ref} -> FAILURE: {err}")

print("--------------------------------------------------")
print(f"Total Invoices Processed: {len(task_queue)}")
print(f"Successfully Generated:   {success_count}")
print(f"Failed Invoices:          {fail_count}")
print("==================================================")
```

**Explanation of the Solution:**
- `generate_monthly_invoice_task` encapsulates long-running PDF billing jobs into an isolated, testable worker function.
- Exceptions are caught and recorded cleanly without halting batch queue execution.
</details>
