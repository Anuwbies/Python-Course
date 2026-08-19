# Lesson 6: Concurrency & Multithreading: The GIL, Threads & Locks

Modern software systems spend vast amounts of time waiting for input/output (I/O) operations: fetching remote API responses, querying databases, or reading disks. Running these operations sequentially causes extreme bottlenecks. In this lesson, you will master **Multithreading**, understand the CPython **Global Interpreter Lock (GIL)**, prevent deadly **Race Conditions** using mutual exclusion locks (`threading.Lock`), and manage concurrent worker pools via `ThreadPoolExecutor`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Distinguish between **Concurrency** (handling multiple tasks interleaved) and **Parallelism** (executing multiple tasks simultaneously on separate CPU cores).
2. Understand the **CPython Global Interpreter Lock (GIL)** and why Python threads do not execute CPU-bound bytecode in true hardware parallel.
3. Identify when Multithreading provides massive speedups (**I/O-bound tasks**).
4. Spawn, synchronize, and join worker threads using `threading.Thread` and `concurrent.futures.ThreadPoolExecutor`.
5. Identify and eliminate **Race Conditions** on shared memory using `threading.Lock` and `threading.RLock`.

---

## 1. Concurrency vs. Parallelism & The CPython GIL

- **Concurrency**: Structuring software to handle multiple tasks at overlapping times. (e.g. one chef juggling multiple pots on a stove).
- **Parallelism**: Executing multiple computations at the exact same physical instant on separate hardware CPU cores. (e.g. multiple chefs working in parallel).

### What is the GIL?
The **Global Interpreter Lock (GIL)** is a mutex mechanism used by CPython to prevent multiple native threads from executing Python bytecode simultaneously. The GIL was implemented to ensure CPython's reference-counting memory manager remains thread-safe.

> [!IMPORTANT]
> **The Golden Rule of Python Concurrency**:
> - **I/O-Bound Tasks** (HTTP requests, database calls, disk I/O): **Use Threads (`threading` / `asyncio`)**. When a thread waits for network I/O, it releases the GIL, allowing other threads to run concurrently.
> - **CPU-Bound Tasks** (image compression, cryptography, machine learning, physics simulations): **Use Processes (`multiprocessing`)** to bypass the GIL across multiple CPU cores.

---

## 2. Race Conditions & Mutual Exclusion (`threading.Lock`)

When multiple threads read and modify shared mutable memory simultaneously, non-atomic operations (such as `balance += amount`) result in corrupted lost-update bugs:

```python
import threading
import time

shared_balance = 1000.0
balance_lock = threading.Lock() # Mutex Lock

def safe_deposit(amount: float):
    global shared_balance
    # with lock guarantees mutual exclusion and automatic release
    with balance_lock:
        current = shared_balance
        time.sleep(0.001) # Simulates context switch
        shared_balance = current + amount
```

---

## 3. High-Level Thread Pools: `ThreadPoolExecutor`

Rather than manually creating and joining individual `Thread` objects, `concurrent.futures.ThreadPoolExecutor` provides a worker pool with `map()` and `submit()`:

```python
from concurrent.futures import ThreadPoolExecutor
import time

def fetch_api_endpoint(endpoint_id: int) -> str:
    time.sleep(0.1) # Simulate network latency
    return f"Response from API #{endpoint_id}"

# Execute 5 concurrent worker threads:
with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(fetch_api_endpoint, range(1, 6))
    for res in results:
        print(res)
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise High-Throughput Concurrent Microservice Health Monitor & Metrics Aggregator**, demonstrating thread pools, safe locking on shared telemetry summaries, and execution time acceleration:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Throughput Microservice Fleet Health Auditor
# =====================================================================

import threading
import time
from concurrent.futures import ThreadPoolExecutor

class FleetHealthMonitor:
    def __init__(self):
        self._lock = threading.Lock() # Protects shared metrics dict
        self._telemetry = {
            "total_probed": 0,
            "healthy_count": 0,
            "unhealthy_count": 0,
            "total_latency_ms": 0.0,
            "failures": []
        }

    def probe_microservice_node(self, node_info: dict) -> dict:
        """Simulates concurrent network HTTP probe to microservice endpoint."""
        hostname = node_info["host"]
        simulated_latency = node_info["latency_ms"] / 1000.0
        should_fail = node_info["is_down"]

        # Simulate I/O network roundtrip (releases GIL during sleep)
        time.sleep(simulated_latency)

        status = "CRITICAL_DOWN" if should_fail else "HEALTHY_200_OK"
        probe_result = {
            "host": hostname,
            "status": status,
            "latency_ms": node_info["latency_ms"]
        }

        # Thread-safe critical section (Lessons 6 & 7)
        with self._lock:
            self._telemetry["total_probed"] += 1
            self._telemetry["total_latency_ms"] += node_info["latency_ms"]
            if should_fail:
                self._telemetry["unhealthy_count"] += 1
                self._telemetry["failures"].append(hostname)
            else:
                self._telemetry["healthy_count"] += 1

        return probe_result

    def print_audit_report(self, total_wall_clock_sec: float) -> None:
        avg_latency = self._telemetry["total_latency_ms"] / max(1, self._telemetry["total_probed"])
        print("\n" + "=" * 70)
        print(f"{'CONCURRENT MICROSERVICE AUDIT REPORT':^70}")
        print("=" * 70)
        print(f"{'Total Nodes Probed:':<35} {self._telemetry['total_probed']} microservices")
        print(f"{'Healthy Instances (200 OK):':<35} {self._telemetry['healthy_count']}")
        print(f"{'Unhealthy / Outage Nodes:':<35} {self._telemetry['unhealthy_count']}")
        print(f"{'Average Node Latency:':<35} {avg_latency:.2f} ms")
        print(f"{'Total Concurrent Wall-Clock Time:':<35} {total_wall_clock_sec * 1000:.2f} ms")
        print("-" * 70)
        if self._telemetry["failures"]:
            print("FAILED SERVICE ENDPOINTS:")
            for f in self._telemetry["failures"]:
                print(f"  🚨 Node Down: {f}")
        print("=" * 70)


# Fleet Targets
node_cluster = [
    {"host": "auth-api-01.internal", "latency_ms": 120, "is_down": False},
    {"host": "billing-api-01.internal", "latency_ms": 250, "is_down": False},
    {"host": "search-indexer-02.internal", "latency_ms": 180, "is_down": True},
    {"host": "recommendations-01.internal", "latency_ms": 140, "is_down": False},
    {"host": "notifications-svc.internal", "latency_ms": 90, "is_down": False},
]

monitor = FleetHealthMonitor()

start_time = time.perf_counter()

# Dispatch concurrent probes using ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as executor:
    probe_futures = executor.map(monitor.probe_microservice_node, node_cluster)
    for res in probe_futures:
        tag = "✅" if res["status"] == "HEALTHY_200_OK" else "❌"
        print(f"  {tag} Probed: {res['host']:<32} -> {res['status']:<16} ({res['latency_ms']} ms)")

total_elapsed = time.perf_counter() - start_time
monitor.print_audit_report(total_elapsed)
```

### 🔍 Code Explanation:
- **`ThreadPoolExecutor(max_workers=5)`**: Fires 5 probe requests concurrently. Sequential execution would take $120+250+180+140+90 = 780\text{ms}$; concurrent execution finishes in roughly the duration of the slowest single call ($\approx 250\text{ms}$).
- **`threading.Lock`**: Guards `self._telemetry` during concurrent updates, ensuring race conditions do not drop failure counts or corrupt average latency metrics.
- **I/O GIL Release**: Python automatically releases the GIL during `time.sleep()`, socket operations, and file reads.

---

## 📝 Quick Exercise: Concurrent Bank Wire Transfer Processor with Thread Locks

### 🏢 Real-Life Scenario
You are developing the concurrent wire settlement engine for an interbank clearing house. Multiple transaction worker threads execute transfers simultaneously across shared customer accounts. You must use a `threading.Lock` on each account to prevent race conditions (lost updates) and record the final balances accurately.

### 📋 Requirements
1. **Define Class `ThreadSafeAccount`**:
   - Attributes: `account_id: str`, `balance: float`.
   - Has a dedicated internal lock: `self._lock = threading.Lock()`.
   - Method `deposit(amount: float) -> None`: Uses `with self._lock:` to add amount safely.
   - Method `withdraw(amount: float) -> bool`: Uses `with self._lock:` to check `balance >= amount` and deduct amount.
2. **Define `execute_transfer(src: ThreadSafeAccount, dst: ThreadSafeAccount, amount: float)`**:
   - Acquires locks cleanly and transfers funds between accounts.
3. Spawn 10 concurrent threads that perform simultaneous transfers and deposits, ensuring that final balances match exact theoretical accounting totals without discrepancy.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 multithreading and locks with Level 2 OOP/encapsulation and Level 1 arithmetic and formatting.

### 🎯 Expected Output
```text
==================================================
      THREAD-SAFE BANK TRANSACTION PROCESSOR      
==================================================
Initial Master Account Balances:
  - Account A: $10,000.00
  - Account B: $10,000.00
--------------------------------------------------
Dispatching 10 concurrent high-speed wire transfers...
  ✓ Transferred $200.00 from Account A -> Account B
  ✓ Transferred $200.00 from Account A -> Account B
  ...
--------------------------------------------------
FINAL RECONCILED BALANCES (Race-Condition Free):
  - Account A: $8,000.00
  - Account B: $12,000.00
  - Combined System Liquidity: $20,000.00 (100% Balanced ✅)
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import threading
from concurrent.futures import ThreadPoolExecutor

# 1. Thread-Safe Account Class (Level 2 & 3)
class ThreadSafeAccount:
    def __init__(self, account_id: str, balance: float):
        self.account_id = account_id
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self, amount: float) -> None:
        with self.lock:
            self.balance += amount

    def withdraw(self, amount: float) -> bool:
        with self.lock:
            if self.balance >= amount:
                self.balance -= amount
                return True
            return False


# 2. Transfer Function
def transfer_funds(src: ThreadSafeAccount, dst: ThreadSafeAccount, amount: float) -> bool:
    # Acquire locks in deterministic order to prevent deadlock
    first_lock, second_lock = (src.lock, dst.lock) if src.account_id < dst.account_id else (dst.lock, src.lock)
    
    with first_lock:
        with second_lock:
            if src.balance >= amount:
                src.balance -= amount
                dst.balance += amount
                return True
            return False


# 3. Execution Simulation
acc_a = ThreadSafeAccount("ACC-A", 10_000.00)
acc_b = ThreadSafeAccount("ACC-B", 10_000.00)

print("==================================================")
print("      THREAD-SAFE BANK TRANSACTION PROCESSOR      ")
print("==================================================")
print("Initial Master Account Balances:")
print(f"  - Account A: ${acc_a.balance:,.2f}")
print(f"  - Account B: ${acc_b.balance:,.2f}")
print("--------------------------------------------------")
print("Dispatching 10 concurrent high-speed wire transfers...")

with ThreadPoolExecutor(max_workers=5) as executor:
    # 10 concurrent transfers of $200 from A to B
    futures = [executor.submit(transfer_funds, acc_a, acc_b, 200.00) for _ in range(10)]
    for f in futures:
        f.result()

total_system_liquidity = acc_a.balance + acc_b.balance

print("--------------------------------------------------")
print("FINAL RECONCILED BALANCES (Race-Condition Free):")
print(f"  - Account A: ${acc_a.balance:,.2f}")
print(f"  - Account B: ${acc_b.balance:,.2f}")
print(f"  - Combined System Liquidity: ${total_system_liquidity:,.2f} (100% Balanced ✅)")
print("==================================================")
```

**Explanation of the Solution:**
- `ThreadSafeAccount` utilizes `threading.Lock()` to serialize read-modify-write state changes.
- Ordered lock acquisition prevents deadlock when multiple threads transfer between accounts concurrently.
</details>
