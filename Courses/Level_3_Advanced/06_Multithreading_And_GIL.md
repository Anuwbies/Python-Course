# Lesson 6: Multithreading, ThreadPools & The GIL

Concurrency allows applications to handle multiple tasks concurrently. In Python, understanding how threads interact with the **Global Interpreter Lock (GIL)** is crucial for building performant network and I/O applications.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the difference between Concurrency and Parallelism.
2. Understand what the **Global Interpreter Lock (GIL)** is and why it exists.
3. Manage threads using `threading.Thread` and `concurrent.futures.ThreadPoolExecutor`.
4. Prevent Race Conditions using Thread Locks (`threading.Lock`).

---

## 1. What is the GIL & When is Multithreading Useful?

The **GIL (Global Interpreter Lock)** is a mutex in CPython that ensures only one native OS thread executes Python bytecode at any given moment.

- **CPU-Bound Tasks** (Heavy math, video rendering): Python multithreading will **not** provide speedups due to the GIL (use `multiprocessing` instead).
- **I/O-Bound Tasks** (Fetching 50 URLs, querying databases, writing files): Python threads **release the GIL** while waiting for network/disk I/O, allowing massive concurrent speedups!

---

## 2. Using `ThreadPoolExecutor` for Concurrent I/O

```python
import concurrent.futures
import time

def fetch_url_data(site_id: int) -> str:
    # Simulating 1-second network latency
    time.sleep(1)
    return f"Data from site {site_id}"

start_time = time.perf_counter()

# Concurrent execution with 5 worker threads:
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(fetch_url_data, i) for i in range(1, 6)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

print(f"Fetched 5 sites concurrently in {time.perf_counter() - start_time:.2f}s!")
# Output: ~1.01s (instead of 5.0s sequential!)
```

---

## 3. Thread Synchronization & Locks

When multiple threads mutate shared data simultaneously, a **Race Condition** corrupts the data. Use `threading.Lock` to enforce mutual exclusion:

```python
import threading

balance = 0
lock = threading.Lock()

def safe_deposit():
    global balance
    for _ in range(100_000):
        with lock: # Only one thread can modify balance at a time!
            balance += 1
```

---

## 📝 Quick Exercise

**Prompt**:
Write a multi-threaded port scanner using `ThreadPoolExecutor` that checks which ports (e.g. 80, 443, 8080) are open on `localhost`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import socket
import concurrent.futures

def scan_port(host: str, port: int) -> int | None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        result = s.connect_ex((host, port))
        if result == 0:
            return port
    return None

target_host = "127.0.0.1"
ports_to_check = [21, 22, 80, 443, 3000, 5000, 8000, 8080]

print(f"Scanning {target_host}...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(scan_port, target_host, p): p for p in ports_to_check}
    for future in concurrent.futures.as_completed(futures):
        port = futures[future]
        if future.result() is not None:
            print(f"🟢 Port {port} is OPEN!")
```
</details>
