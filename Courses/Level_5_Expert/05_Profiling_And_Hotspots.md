# Lesson 5: High-Performance Profiling, Hotspot Analysis & Memory Tracing

*"Premature optimization is the root of all evil"* (Donald Knuth). Senior software engineers never guess where bottlenecks are; they measure them using deterministic profilers, statistical sampling tools, and memory allocators. In this lesson, you will master **CPU Profiling (`cProfile`, `pstats`)**, line-by-line memory allocation tracking (**`tracemalloc`**), and statistical sampling techniques to optimize algorithmic hotspots.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Distinguish between **Deterministic Profiling** (tracing every call) and **Statistical Sampling** (`py-spy`).
2. Profile execution hotspots using Python's built-in **`cProfile`** and analyze metrics via **`pstats`**.
3. Understand profiler column metrics: `ncalls`, `tottime`, `percall`, and `cumtime`.
4. Capture memory allocation snapshots and detect memory leaks using **`tracemalloc`**.
5. Eliminate common performance bottlenecks (allocations in tight loops, global lookups, quadratic string concatenation).

---

## 1. CPU Profiling with `cProfile` & `pstats`

`cProfile` hooks into the CPython evaluation loop, counting every function invocation and measuring exact wall-clock/CPU durations:

```python
import cProfile
import pstats
import io

def slow_computation():
    total = 0
    for i in range(1_000_000):
        total += i
    return total

# Run profiler
pr = cProfile.Profile()
pr.enable()
slow_computation()
pr.disable()

# Format statistics
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
ps.print_stats(10) # Print top 10 most expensive calls
print(s.getvalue())
```

### Profiler Metrics Explained:
- **`ncalls`**: Total number of times the function was called.
- **`tottime`**: Total time spent *strictly inside* this function (excluding time in sub-functions).
- **`cumtime`**: Cumulative time spent in this function *plus all child calls* it initiated.
- **`percall`**: Average time per single invocation (`tottime / ncalls`).

---

## 2. Memory Allocation Tracing with `tracemalloc`

The `tracemalloc` module tracks every single memory block allocated by Python interpreters back to the exact source file and line number:

```python
import tracemalloc

tracemalloc.start()

# Code that allocates memory
data_cache = [f"Record_{i}" for i in range(500_000)]

# Capture snapshot
current, peak = tracemalloc.get_traced_memory()
print(f"Current RAM Allocated: {current / (1024 * 1024):.2f} MB")
print(f"Peak RAM Consumed:     {peak / (1024 * 1024):.2f} MB")

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("\n--- Top 3 Memory Allocation Lines ---")
for stat in top_stats[:3]:
    print(stat)

tracemalloc.stop()
```

---

## 3. Production Statistical Sampling (`py-spy`)

In live production Kubernetes clusters, running deterministic profilers like `cProfile` introduces 10%–30% runtime overhead. Tools like **`py-spy`** inspect Python process memory externally at 100Hz with $<1\%$ overhead to generate interactive **Flame Graphs**.

---

## 💻 Code Example & Reference

The following real-life program models an **Algorithmic Trading Quantitative Signal Engine & Memory Hotspot Benchmarker**, demonstrating `cProfile` profiling, `tracemalloc` memory differential comparison, and hotspot optimization:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Quantitative Signal Profiling & Memory Diagnostics
# =====================================================================

import cProfile
import pstats
import io
import tracemalloc
import math

class QuantitativeSignalEngine:
    """Calculates statistical indicators over financial price feeds."""

    def __init__(self, price_series: list[float]):
        self.prices = price_series

    # Unoptimized: Reallocates lists and performs redundant loops
    def compute_moving_averages_unoptimized(self, window: int = 20) -> list[float]:
        n = len(self.prices)
        result = []
        for i in range(n - window + 1):
            window_slice = self.prices[i : i + window] # Inefficient slicing in tight loop
            avg = sum(window_slice) / window
            result.append(avg)
        return result

    # Optimized: Rolling sliding-window sum (O(n) time, minimal allocations)
    def compute_moving_averages_optimized(self, window: int = 20) -> list[float]:
        n = len(self.prices)
        if n < window:
            return []

        # Calculate initial window sum
        current_sum = sum(self.prices[:window])
        result = [current_sum / window]

        # Slide window by adding incoming and subtracting outgoing element
        for i in range(window, n):
            current_sum += self.prices[i] - self.prices[i - window]
            result.append(current_sum / window)

        return result


# Benchmark & Profiling Suite
DATASET_SIZE = 500_000
raw_prices = [100.0 + math.sin(i * 0.01) * 20.0 for i in range(DATASET_SIZE)]
engine = QuantitativeSignalEngine(raw_prices)

print("=" * 80)
print(f"{'QUANTITATIVE SIGNAL PROFILER & MEMORY TRACE SUITE':^80}")
print("=" * 80)

# 1. Profile CPU Hotspots using cProfile (Lesson 5)
pr = cProfile.Profile()
pr.enable()

res_unoptimized = engine.compute_moving_averages_unoptimized(window=50)
res_optimized = engine.compute_moving_averages_optimized(window=50)

pr.disable()

s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
ps.print_stats(6)

print("--- CPU PROFILER EXECUTION BREAKDOWN (cProfile) ---")
print(s.getvalue())

# 2. Profile Memory Footprint using tracemalloc (Lesson 5)
print("-" * 80)
print("--- MEMORY TRACING & PEAK RAM CONSUMPTION (tracemalloc) ---")

tracemalloc.start()
snap_before = tracemalloc.take_snapshot()

# Run memory-intensive workload
signal_matrix = [engine.compute_moving_averages_optimized(window=w) for w in [10, 20, 50]]

current_ram, peak_ram = tracemalloc.get_traced_memory()
snap_after = tracemalloc.take_snapshot()
tracemalloc.stop()

print(f"Current Signal Buffer: {current_ram / (1024 * 1024):.2f} MB")
print(f"Peak Memory Allocated: {peak_ram / (1024 * 1024):.2f} MB")

diff_stats = snap_after.compare_to(snap_before, 'lineno')
print("\nTop Memory Allocation Differences:")
for stat in diff_stats[:2]:
    print(f"  • {stat}")

print("=" * 80)
```

### 🔍 Code Explanation:
- **`cProfile.Profile()`**: Measures exact CPU time spent in list slicing vs rolling math calculations.
- **`pstats.Stats.sort_stats(SortKey.CUMULATIVE)`**: Sorts functions by total time spent to pinpoint bottlenecks immediately.
- **`tracemalloc.get_traced_memory()`**: Measures current and peak RAM allocations in megabytes, proving that sliding window algorithms avoid large intermediate buffer allocations.

---

## 📝 Quick Exercise: Memory Allocation Peak Profiler & Hotspot Detector

### 🏢 Real-Life Scenario
You are developing a continuous performance regression test for a large data processing library. You must write a decorator `@profile_memory_peak` that measures the exact peak RAM allocated during a function's execution and prints an alert if memory exceeds a defined threshold (e.g. 5 MB).

### 📋 Requirements
1. **Define Parameterized Decorator `@profile_memory_peak(max_allowed_mb: float = 5.0)`**:
   - Starts `tracemalloc.start()`.
   - Executes the wrapped function.
   - Retrieves peak RAM via `tracemalloc.get_traced_memory()`.
   - Stops `tracemalloc.stop()`.
   - Converts peak bytes to MB.
   - If `peak_mb > max_allowed_mb`: Prints `f"⚠️ [MEMORY WARNING] {func.__name__} exceeded limit: {peak_mb:.2f} MB / {max_allowed_mb} MB"`.
   - Else: Prints `f"✅ [MEMORY CLEAR] {func.__name__} peak RAM: {peak_mb:.2f} MB"`.
2. Test on a lightweight generator function and a memory-heavy list allocation.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 5 `tracemalloc` profiling with Level 2 parameterized decorators and `functools.wraps`.

### 🎯 Expected Output
```text
==================================================
        PEAK MEMORY REGRESSION AUDITOR TEST       
==================================================
✅ [MEMORY CLEAR] test_lightweight_generator peak RAM: 0.01 MB
⚠️ [MEMORY WARNING] test_heavy_list_allocation exceeded limit: 7.63 MB / 5.0 MB
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import functools
import tracemalloc

# 1. Parameterized Memory Profiling Decorator (Level 5)
def profile_memory_peak(max_allowed_mb: float = 5.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            tracemalloc.reset_peak()
            
            result = func(*args, **kwargs)
            
            _, peak_bytes = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            peak_mb = peak_bytes / (1024.0 * 1024.0)

            if peak_mb > max_allowed_mb:
                print(f"⚠️ [MEMORY WARNING] {func.__name__} exceeded limit: {peak_mb:.2f} MB / {max_allowed_mb} MB")
            else:
                print(f"✅ [MEMORY CLEAR] {func.__name__} peak RAM: {peak_mb:.2f} MB")

            return result
        return wrapper
    return decorator


# 2. Test Functions
@profile_memory_peak(max_allowed_mb=5.0)
def test_lightweight_generator():
    return sum(x for x in range(10_000))

@profile_memory_peak(max_allowed_mb=5.0)
def test_heavy_list_allocation():
    # Allocates ~7.6 MB of integers
    return [x for x in range(200_000)]


# 3. Execution Simulation
print("==================================================")
print("        PEAK MEMORY REGRESSION AUDITOR TEST       ")
print("==================================================")
test_lightweight_generator()
test_heavy_list_allocation()
print("==================================================")
```

**Explanation of the Solution:**
- `@profile_memory_peak` leverages `tracemalloc.get_traced_memory()` to inspect the exact heap delta during the target function's lifetime.
</details>
