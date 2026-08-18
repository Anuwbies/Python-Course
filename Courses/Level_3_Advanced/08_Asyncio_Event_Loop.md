# Lesson 8: Asynchronous Programming with asyncio

`asyncio` is Python's modern asynchronous framework for single-threaded concurrent code using coroutines, non-blocking sockets, and an event loop.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the Event Loop and non-blocking I/O.
2. Define Coroutines with `async def` and pause them with `await`.
3. Run thousands of concurrent tasks with `asyncio.gather()` and `asyncio.TaskGroup`.
4. Throttle requests using `asyncio.Semaphore`.

---

## 1. Coroutines and `async` / `await`

```python
import asyncio
import time

async def fetch_api_data(endpoint: str) -> dict:
    print(f"📡 Requesting {endpoint}...")
    # asyncio.sleep yields control back to event loop without blocking the thread!
    await asyncio.sleep(1.0)
    print(f"✅ Received response from {endpoint}")
    return {"endpoint": endpoint, "status": 200}

async def main():
    start = time.perf_counter()

    # Launching 3 concurrent async coroutines
    results = await asyncio.gather(
        fetch_api_data("/users"),
        fetch_api_data("/orders"),
        fetch_api_data("/products"),
    )

    print(f"All 3 APIs fetched in {time.perf_counter() - start:.2f}s!")
    # Output: ~1.00s total!

if __name__ == '__main__':
    asyncio.run(main())
```

---

## 2. Rate Limiting with `asyncio.Semaphore`

Prevent overwhelming a remote server when making 1,000 async requests:

```python
async def bounded_fetch(sem: asyncio.Semaphore, url_id: int):
    async with sem: # Max 5 concurrent requests at any one time
        await asyncio.sleep(0.5)
        print(f"Finished {url_id}")

async def main():
    semaphore = asyncio.Semaphore(5)
    tasks = [bounded_fetch(semaphore, i) for i in range(50)]
    await asyncio.gather(*tasks)
```

---

## 📝 Quick Exercise

**Prompt**:
Create an async web status checker that takes 20 URLs, queries their status concurrently with a max concurrency limit of 4 using `asyncio.Semaphore`, and returns a summary dict of responsive endpoints.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import asyncio

async def check_url(sem: asyncio.Semaphore, url: str) -> dict:
    async with sem:
        # Simulate network latency
        await asyncio.sleep(0.2)
        return {"url": url, "status": 200, "alive": True}

async def main():
    sem = asyncio.Semaphore(4)
    urls = [f"https://api.example.com/v1/item/{i}" for i in range(20)]
    
    tasks = [check_url(sem, url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    print(f"Checked {len(results)} URLs concurrently with max 4 in-flight at once!")

if __name__ == '__main__':
    asyncio.run(main())
```
</details>
