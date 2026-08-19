# Lesson 7: Parallel Computing: Multiprocessing & IPC

While Multithreading accelerates I/O-bound tasks, it cannot parallelize CPU-heavy calculations across multiple processor cores due to the CPython GIL. To unlock true multi-core parallel computing for heavy mathematical modeling, image rendering, machine learning inference, or cryptographic hashing, you must use **Multiprocessing**. In this lesson, you will master the `multiprocessing` module, `ProcessPoolExecutor`, and Inter-Process Communication (IPC).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand how separate Python OS processes bypass the Global Interpreter Lock (GIL).
2. Distinguish the performance trade-offs: Memory isolation vs. process spawn overhead.
3. Distribute CPU-intensive batch jobs across multi-core systems using `concurrent.futures.ProcessPoolExecutor`.
4. Communicate data safely between processes using **Inter-Process Communication (IPC)** via `multiprocessing.Queue`.
5. Understand object serialization (**Pickling**) and the mandatory `if __name__ == '__main__':` safeguard on Windows/macOS.

---

## 1. Process Architecture vs. Thread Architecture

```
Thread Model (Single OS Process)        Process Model (True Multi-Core Parallelism)
┌───────────────────────────────┐       ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│     Shared Process Memory     │       │ Process #1    │ │ Process #2    │ │ Process #3    │
│  [ Thread 1 ] [ Thread 2 ]    │       │ Memory Space  │ │ Memory Space  │ │ Memory Space  │
│        🔒 Single GIL          │       │ 🔒 GIL #1     │ │ 🔒 GIL #2     │ │ 🔒 GIL #3     │
│        1 CPU Core             │       │ Core #1       │ │ Core #2       │ │ Core #3       │
└───────────────────────────────┘       └───────────────┘ └───────────────┘ └───────────────┘
```

---

## 2. High-Performance Multi-Core Pools: `ProcessPoolExecutor`

The `concurrent.futures.ProcessPoolExecutor` manages a pool of worker processes, splitting tasks across all available hardware CPU cores:

```python
from concurrent.futures import ProcessPoolExecutor
import os
import math

def compute_heavy_factorials(n: int) -> int:
    """CPU-bound task running in independent worker process."""
    return sum(math.factorial(i % 20) for i in range(n))

if __name__ == "__main__":
    workloads = [500_000, 500_000, 500_000, 500_000]
    
    # Automatically spawns worker processes equal to os.cpu_count()
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(compute_heavy_factorials, workloads))
        print(f"Computed {len(results)} intensive workloads across multiple CPU cores.")
```

---

## 3. Inter-Process Communication (IPC) via `multiprocessing.Queue`

Because processes run in isolated memory spaces, they cannot share plain Python lists or variables. Data must be serialized (**pickled**) and transmitted through IPC channels like `multiprocessing.Queue`:

```python
import multiprocessing

def worker_producer(task_queue: multiprocessing.Queue, worker_id: int):
    for item_id in range(1, 4):
        payload = f"WorkItem-{item_id} from Process-{worker_id}"
        task_queue.put(payload) # Thread/Process-safe IPC enqueue

if __name__ == "__main__":
    shared_queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=worker_producer, args=(shared_queue, 1))
    p2 = multiprocessing.Process(target=worker_producer, args=(shared_queue, 2))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    while not shared_queue.empty():
        print(f"Consumed: {shared_queue.get()}")
```

---

## 💻 Code Example & Reference

The following real-life program models an **Institutional Financial Portfolio Monte Carlo Risk Simulation Engine**, distributing 100,000 statistical market scenario simulations across parallel CPU worker processes:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Performance Monte Carlo Financial Risk Engine
# =====================================================================

import math
import random
import time
import os
from concurrent.futures import ProcessPoolExecutor

# CPU-Bound Task (Executed in parallel across separate worker processes)
def simulate_portfolio_monte_carlo(batch_params: tuple[int, float, float, float, int]) -> dict:
    """Simulates geometric Brownian motion stock market trajectories."""
    sim_count, initial_nav, annual_drift, annual_volatility, days = batch_params
    dt = 1.0 / 252.0 # 252 trading days per calendar year
    
    worst_drawdown_nav = initial_nav
    ending_navs = []
    
    # Independent random seed per process
    random.seed(os.getpid() + int(time.time() * 1000) % 100000)
    
    for _ in range(sim_count):
        current_price = initial_nav
        for _ in range(days):
            # Box-Muller normal distribution random shock
            u1, u2 = random.random(), random.random()
            z = math.sqrt(-2.0 * math.log(max(1e-10, u1))) * math.cos(2.0 * math.pi * u2)
            
            daily_return = (annual_drift - 0.5 * annual_volatility**2) * dt + (annual_volatility * math.sqrt(dt) * z)
            current_price *= math.exp(daily_return)
            
        ending_navs.append(current_price)
        if current_price < worst_drawdown_nav:
            worst_drawdown_nav = current_price

    avg_terminal_nav = sum(ending_navs) / len(ending_navs)
    
    return {
        "pid": os.getpid(),
        "simulations_run": sim_count,
        "avg_terminal_nav": avg_terminal_nav,
        "worst_drawdown_nav": worst_drawdown_nav,
    }


# Master Process Execution Orchestrator
if __name__ == "__main__":
    TOTAL_SIMULATIONS = 40_000
    NUM_WORKER_CORES = 4
    SIMS_PER_WORKER = TOTAL_SIMULATIONS // NUM_WORKER_CORES
    
    # (simulations, initial_nav, drift_pct, volatility_pct, trading_days)
    batch_args = [
        (SIMS_PER_WORKER, 1_000_000.0, 0.08, 0.22, 252) for _ in range(NUM_WORKER_CORES)
    ]

    print("=" * 75)
    print(f"{'PARALLEL MULTI-CORE MONTE CARLO VALUE-AT-RISK SIMULATOR':^75}")
    print("=" * 75)
    print(f"Allocating {TOTAL_SIMULATIONS:,} stochastic market simulations across {NUM_WORKER_CORES} CPU processes...")

    start_wall_clock = time.perf_counter()

    with ProcessPoolExecutor(max_workers=NUM_WORKER_CORES) as executor:
        batch_results = list(executor.map(simulate_portfolio_monte_carlo, batch_args))

    total_time = time.perf_counter() - start_wall_clock

    # Aggregate parallel batch results
    overall_avg_nav = sum(b["avg_terminal_nav"] for b in batch_results) / len(batch_results)
    absolute_worst = min(b["worst_drawdown_nav"] for b in batch_results)

    print("-" * 75)
    print(f"{'Worker PID':<15} | {'Simulations':<15} | {'Average Ending NAV':>20} | {'Worst Tail Loss':>16}")
    print("-" * 75)
    for b in batch_results:
        print(f"Process #{b['pid']:<7} | {b['simulations_run']:<15,} | ${b['avg_terminal_nav']:>19,.2f} | ${b['worst_drawdown_nav']:>15,.2f}")
    print("-" * 75)
    print(f"{'CONSOLIDATED 1-YEAR PROJECTED NAV:':<40} ${overall_avg_nav:,.2f}")
    print(f"{'EXTREME TAIL LOSS (Value-at-Risk):':<40} ${absolute_worst:,.2f}")
    print(f"{'PARALLEL COMPUTE EXECUTION TIME:':<40} {total_time:.3f} seconds ⚡")
    print("=" * 75)
```

### 🔍 Code Explanation:
- **`if __name__ == '__main__':`**: Mandatory on Windows/macOS to prevent recursive process spawning during interpreter initialization.
- **`ProcessPoolExecutor(max_workers=4)`**: Distributes statistical mathematical calculations across 4 separate CPU cores, bypassing the GIL completely.
- **Independent Seeds**: Each worker process seeds its RNG with `os.getpid()` to ensure statistical randomness across parallel processes.

---

## 📝 Quick Exercise: Parallel Cryptographic Proof-of-Work Mining Engine

### 🏢 Real-Life Scenario
You are developing a high-throughput blockchain verification and proof-of-work block miner. Finding a valid cryptographic nonce requires hashing millions of candidate strings until one matches a target prefix difficulty (e.g. finding a hash starting with `"0000"`). You will implement a parallel miner using `ProcessPoolExecutor` that partitions the nonce search space across multi-core worker processes.

### 📋 Requirements
1. **Define `mine_block_partition(args: tuple[str, int, int, str]) -> tuple[int, str, int] | None`**:
   - Accepts `(block_header: str, start_nonce: int, end_nonce: int, difficulty_prefix: str)`.
   - Iterates through the range `start_nonce` to `end_nonce`.
   - Computes mock SHA-256 hash using `hashlib.sha256(f"{block_header}:{nonce}".encode()).hexdigest()`.
   - If hash starts with `difficulty_prefix` (e.g. `"0000"`), returns `(nonce, hash_str, os.getpid())`.
   - Returns `None` if no matching nonce was discovered in this partition.
2. Partition a search space of 100,000 nonces across 4 worker processes.
3. Run the parallel search and output the discovered winning block nonce.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 multiprocessing and `ProcessPoolExecutor` with Level 2 tuples, type annotations, and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        PARALLEL MULTI-CORE PROOF-OF-WORK MINER   
==================================================
Block Header:       BLOCK-ROOT-HASH-890214
Difficulty Target:  Starts with '0000'
Search Range:       0 to 100,000 nonces (4 CPU Processes)
--------------------------------------------------
⛏️ MINING RESULT DISCOVERED:
  ✓ Winning Nonce:    38491
  ✓ Verified Hash:    0000fa249018e4...
  ✓ Mined by Process: PID #...
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import hashlib
import os
from concurrent.futures import ProcessPoolExecutor

# 1. Parallel Nonce Mining Worker (Level 3)
def mine_block_partition(args: tuple[str, int, int, str]) -> tuple[int, str, int] | None:
    block_header, start_nonce, end_nonce, difficulty = args
    
    for nonce in range(start_nonce, end_nonce):
        candidate = f"{block_header}:{nonce}".encode("utf-8")
        h = hashlib.sha256(candidate).hexdigest()
        if h.startswith(difficulty):
            return nonce, h, os.getpid()
            
    return None


# 2. Main Process Orchestrator
if __name__ == "__main__":
    HEADER = "BLOCK-ROOT-HASH-890214"
    DIFFICULTY = "0000"
    TOTAL_SPACE = 100_000
    WORKERS = 4
    CHUNK = TOTAL_SPACE // WORKERS

    partitions = [
        (HEADER, i * CHUNK, (i + 1) * CHUNK, DIFFICULTY) for i in range(WORKERS)
    ]

    print("==================================================")
    print("        PARALLEL MULTI-CORE PROOF-OF-WORK MINER   ")
    print("==================================================")
    print(f"Block Header:       {HEADER}")
    print(f"Difficulty Target:  Starts with '{DIFFICULTY}'")
    print(f"Search Range:       0 to {TOTAL_SPACE:,} nonces ({WORKERS} CPU Processes)")
    print("--------------------------------------------------")

    winning_solution = None

    with ProcessPoolExecutor(max_workers=WORKERS) as executor:
        results = executor.map(mine_block_partition, partitions)
        for res in results:
            if res is not None:
                winning_solution = res
                break

    if winning_solution:
        nonce, hash_val, pid = winning_solution
        print("⛏️ MINING RESULT DISCOVERED:")
        print(f"  ✓ Winning Nonce:    {nonce}")
        print(f"  ✓ Verified Hash:    {hash_val}")
        print(f"  ✓ Mined by Process: PID #{pid}")
    else:
        print("❌ Target difficulty not found in allocated nonce space.")

    print("==================================================")
```

**Explanation of the Solution:**
- Distributing search partitions across `ProcessPoolExecutor` allows 4 CPU cores to hash candidate nonces in true hardware parallel, accelerating cryptographic discovery by $\approx 4\times$.
</details>
