# Lesson 8: Asynchronous Concurrency: `asyncio` & The Event Loop

When building scalable modern network applications (such as FastAPI backends, chat servers, or high-throughput API crawlers), spawning thousands of OS threads wastes massive amounts of system memory on thread stack allocations and context-switching overhead. **Asynchronous I/O (`asyncio`)** provides single-threaded, cooperative multitasking capable of handling tens of thousands of concurrent connections on a single machine. In this milestone lesson of Level 3, you will master `async`/`await`, the **Event Loop**, `asyncio.gather()`, and concurrency throttling via `asyncio.Semaphore`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the **Event Loop** execution model and cooperative multitasking.
2. Define Coroutines using `async def` and yield control non-blockingly using `await`.
3. Schedule concurrent coroutines using `asyncio.create_task()` and `asyncio.gather()`.
4. Throttle network traffic and prevent API rate-limit bans using `asyncio.Semaphore`.
5. Implement Asynchronous Context Managers (`async with`) and Asynchronous Iterators (`async for`).
6. Identify and prevent the fatal **Event Loop Blocking Trap** (`time.sleep` vs `asyncio.sleep`).

---

## 1. The Event Loop Architecture

Unlike multithreading (where the operating system preemptively pauses threads), `asyncio` runs on a single thread. Coroutines voluntarily yield control back to the **Event Loop** whenever they wait for network, disk, or timer I/O:

```
┌────────────────────────────────────────────────────────┐
│                   THE EVENT LOOP                       │
│  [ Task 1: Wait Socket ] ──> [ Task 2: Resume & Run ]  │
│  [ Task 3: Timer Expire] <── [ Task 4: Wait DB Socket] │
└────────────────────────────────────────────────────────┘
```

```python
import asyncio

# A coroutine function (declared with async def)
async def fetch_user_data(user_id: int) -> dict:
    print(f"Fetching user #{user_id}...")
    # Non-blocking pause: releases control to the event loop
    await asyncio.sleep(0.5) 
    print(f"✅ Received user #{user_id}")
    return {"id": user_id, "username": f"user_{user_id}"}

async def main():
    # Run multiple coroutines concurrently in parallel
    results = await asyncio.gather(
        fetch_user_data(101),
        fetch_user_data(102),
        fetch_user_data(103)
    )
    print(f"All users fetched: {results}")

# Entry point that initializes and manages the event loop
asyncio.run(main())
```

---

## 2. Throttling Concurrency with `asyncio.Semaphore`

Firing 10,000 asynchronous network requests simultaneously will crash servers or trigger rate-limit bans. An `asyncio.Semaphore` guarantees that at most $N$ coroutines execute concurrently:

```python
import asyncio

async def bounded_api_call(semaphore: asyncio.Semaphore, endpoint_id: int):
    # Only N tasks can enter this async context block at any given instant
    async with semaphore:
        print(f"🔒 [Active] Querying Endpoint #{endpoint_id}...")
        await asyncio.sleep(0.2)
        print(f"🔓 [Complete] Endpoint #{endpoint_id}")

async def run_throttled_batch():
    sem = asyncio.Semaphore(3) # Maximum 3 concurrent active requests
    tasks = [bounded_api_call(sem, i) for i in range(1, 10)]
    await asyncio.gather(*tasks)

asyncio.run(run_throttled_batch())
```

---

## 3. Asynchronous Context Managers (`async with`)

Classes can implement `__aenter__` and `__aexit__` to handle non-blocking asynchronous resource setup and teardown:

```python
class AsyncDatabaseClient:
    async def __aenter__(self):
        print("Connecting to async database pool...")
        await asyncio.sleep(0.1) # Non-blocking connection handshake
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Closing async database connection pool...")
        await asyncio.sleep(0.05)

async def test_db():
    async with AsyncDatabaseClient() as db:
        print("  -> Executing async SQL queries...")

asyncio.run(test_db())
```

---

## 💻 Code Example & Reference

The following real-life program models an **Asynchronous High-Throughput Web Crawler & Document Ingestion Engine**, demonstrating coroutines, `asyncio.Semaphore` rate limiting, task gathering, and non-blocking streaming:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Throughput Async Web Crawler & Search Indexer
# =====================================================================

import asyncio
import time

class AsyncSearchEngineCrawler:
    """Asynchronously crawls URLs concurrently with strict rate limiting."""

    def __init__(self, max_concurrent_connections: int = 3):
        self.semaphore = asyncio.Semaphore(max_concurrent_connections)
        self.indexed_documents: list[dict] = []
        self.failed_urls: list[str] = []

    async def crawl_url(self, target: dict) -> dict | None:
        url = target["url"]
        simulated_latency = target["latency_sec"]
        should_fail = target["fail"]

        # Acquire concurrency token from semaphore (Lesson 8)
        async with self.semaphore:
            print(f"🌐 [CRAWL START] Fetching {url:<35} (Active Concurrency Bound: 3)")
            
            # Non-blocking network I/O simulation
            await asyncio.sleep(simulated_latency)

            if should_fail:
                print(f"❌ [CRAWL ERROR] HTTP 500 Server Error: {url}")
                self.failed_urls.append(url)
                return None

            doc_payload = {
                "url": url,
                "title": target["title"],
                "content_bytes": target["size_kb"] * 1024,
                "latency_sec": simulated_latency,
            }
            self.indexed_documents.append(doc_payload)
            print(f"✅ [CRAWL DONE]  Indexed: {target['title']} ({target['size_kb']} KB)")
            return doc_payload

    async def crawl_all_targets(self, targets: list[dict]) -> None:
        print("=" * 75)
        print(f"{'ASYNC HIGH-THROUGHPUT WEB CRAWLER & SEARCH INDEXER':^75}")
        print("=" * 75)
        
        start_time = time.perf_counter()
        
        # Create coroutine tasks and gather them concurrently (Lesson 8)
        tasks = [self.crawl_url(target) for target in targets]
        await asyncio.gather(*tasks)
        
        total_time = time.perf_counter() - start_time
        
        # Summarize crawl metrics
        total_kb = sum(doc["content_bytes"] for doc in self.indexed_documents) / 1024.0
        print("-" * 75)
        print(f"{'CRAWLER HARVEST METRICS':^75}")
        print("-" * 75)
        print(f"{'Total Target URLs:':<35} {len(targets)}")
        print(f"{'Successfully Indexed Documents:':<35} {len(self.indexed_documents)}")
        print(f"{'Failed URL Requests:':<35} {len(self.failed_urls)}")
        print(f"{'Total Harvested Payload Data:':<35} {total_kb:,.1f} KB")
        print(f"{'Total Async Execution Time:':<35} {total_time:.2f} seconds ⚡")
        print("=" * 75)


# URL Crawl Target Batch
crawl_manifest = [
    {"url": "https://docs.python.org/3/", "title": "Python 3 Official Docs", "latency_sec": 0.4, "size_kb": 240, "fail": False},
    {"url": "https://fastapi.tiangolo.com/", "title": "FastAPI Web Framework", "latency_sec": 0.3, "size_kb": 180, "fail": False},
    {"url": "https://unreachable-broken-host.net/", "title": "Broken Mirror", "latency_sec": 0.2, "size_kb": 0, "fail": True},
    {"url": "https://pydantic.dev/", "title": "Pydantic Data Models", "latency_sec": 0.5, "size_kb": 310, "fail": False},
    {"url": "https://pytest.org/", "title": "Pytest Automation Framework", "latency_sec": 0.35, "size_kb": 150, "fail": False},
    {"url": "https://redis.io/docs/", "title": "Redis In-Memory Engine", "latency_sec": 0.45, "size_kb": 420, "fail": False},
]

# Run Async Event Loop
crawler = AsyncSearchEngineCrawler(max_concurrent_connections=3)
asyncio.run(crawler.crawl_all_targets(crawl_manifest))
```

### 🔍 Code Explanation:
- **`asyncio.gather(*tasks)`**: Concurrently schedules all 6 crawl targets onto the single-threaded event loop.
- **`asyncio.Semaphore(3)`**: Enforces that no more than 3 network streams download simultaneously, safeguarding client memory and honoring server rate limits.
- **Non-Blocking Execution**: While one task waits on `await asyncio.sleep()`, the event loop immediately switches context to execute and advance the other tasks.

---

## 📝 Quick Exercise: Async Microservice Health Prober & Latency Aggregator

### 🏢 Real-Life Scenario
You are developing the active health-check probe for a Kubernetes microservice ingress controller. The ingress prober must ping 5 distinct service endpoints asynchronously with an `asyncio.Semaphore(2)` limiting concurrent socket connections, collect latency statistics, and report service availability without blocking.

### 📋 Requirements
1. **Define Coroutine `probe_service_async(sem: asyncio.Semaphore, name: str, latency: float, healthy: bool) -> dict`**:
   - Uses `async with sem:` to throttle execution to 2 concurrent tasks.
   - Awaits `asyncio.sleep(latency)`.
   - Returns `{"name": name, "latency_ms": latency * 1000.0, "status": "200_OK" if healthy else "503_UNAVAILABLE"}`.
2. **Define Coroutine `run_health_audit(services: list[tuple])`**:
   - Initializes `sem = asyncio.Semaphore(2)`.
   - Uses `asyncio.gather()` to execute all probes concurrently.
   - Formats and displays the health status table and average response latency.
3. Execute the async runner via `asyncio.run()`.

> [!IMPORTANT]
> **Cumulative Level 3 Milestone Constraint**: Combine Level 3 `asyncio`, coroutines, and semaphores with Level 2 dictionaries/tuples and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        ASYNC FLEET HEALTH CHECK AUDITOR          
==================================================
  ✓ Service: Auth-Service          | Latency:  150.00 ms | Status: 200_OK
  ✓ Service: Payments-Gateway      | Latency:  300.00 ms | Status: 200_OK
  ✗ Service: Search-Indexer        | Latency:  100.00 ms | Status: 503_UNAVAILABLE
  ✓ Service: User-Profile-DB       | Latency:  250.00 ms | Status: 200_OK
  ✓ Service: Notification-Queue    | Latency:  120.00 ms | Status: 200_OK
--------------------------------------------------
Total Services Probed: 5
Fleet Availability:    80.0% (4/5 Online)
Average Response Time: 184.00 ms
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import asyncio

# 1. Async Probe Coroutine (Level 3)
async def probe_service_async(sem: asyncio.Semaphore, name: str, latency: float, healthy: bool) -> dict:
    async with sem:
        await asyncio.sleep(latency) # Non-blocking I/O
        return {
            "name": name,
            "latency_ms": latency * 1000.0,
            "status": "200_OK" if healthy else "503_UNAVAILABLE",
            "healthy": healthy
        }


# 2. Main Audit Coroutine Orchestrator (Level 3)
async def run_health_audit(services: list[tuple]) -> None:
    sem = asyncio.Semaphore(2) # Throttle to 2 concurrent sockets
    
    tasks = [
        probe_service_async(sem, name, latency, is_healthy)
        for name, latency, is_healthy in services
    ]
    
    results = await asyncio.gather(*tasks)

    print("==================================================")
    print("        ASYNC FLEET HEALTH CHECK AUDITOR          ")
    print("==================================================")
    
    healthy_count = 0
    total_latency = 0.0

    for r in results:
        tag = "✓" if r["healthy"] else "✗"
        if r["healthy"]:
            healthy_count += 1
        total_latency += r["latency_ms"]
        print(f"  {tag} Service: {r['name']:<22} | Latency: {r['latency_ms']:>7.2f} ms | Status: {r['status']}")

    avg_latency = total_latency / len(results)
    availability_pct = (healthy_count / len(results)) * 100.0

    print("--------------------------------------------------")
    print(f"Total Services Probed: {len(results)}")
    print(f"Fleet Availability:    {availability_pct:.1f}% ({healthy_count}/{len(results)} Online)")
    print(f"Average Response Time: {avg_latency:.2f} ms")
    print("==================================================")


# 3. Execution Entry Point
if __name__ == "__main__":
    service_fleet = [
        ("Auth-Service", 0.15, True),
        ("Payments-Gateway", 0.30, True),
        ("Search-Indexer", 0.10, False),
        ("User-Profile-DB", 0.25, True),
        ("Notification-Queue", 0.12, True),
    ]

    asyncio.run(run_health_audit(service_fleet))
```

**Explanation of the Solution:**
- `probe_service_async` executes single-threaded non-blocking I/O using `await asyncio.sleep()`.
- `asyncio.Semaphore(2)` limits concurrent network connections.
- `asyncio.gather()` orchestrates concurrent results and aggregates metrics cleanly.
</details>
