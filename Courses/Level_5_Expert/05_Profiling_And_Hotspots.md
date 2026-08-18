# Lesson 5: High-Performance Profiling: CPU & Memory Hotspots

Premature optimization is the root of all evil. Before rewriting Python code in C, you must use deterministic and statistical profilers to pinpoint exact bottlenecks.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Profile CPU time using deterministic `cProfile` and statistical sampling profilers (`py-spy`).
2. Track memory allocations and memory leaks using `tracemalloc`.
3. Profile line-by-line performance with `line_profiler` and `memory_profiler`.
4. Generate and read visual Flamegraphs.

---

## 1. CPU Profiling with `cProfile`

```python
import cProfile
import pstats
import io

def heavy_computation():
    total = 0
    for i in range(1_000_000):
        total += i ** 2
    return total

def main_app():
    return heavy_computation()

# Run profiler
pr = cProfile.Profile()
pr.enable()

main_app()

pr.disable()

# Format and print top time-consuming functions
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
ps.print_stats(10)
print(s.getvalue())
```

---

## 2. Memory Leak Tracking with `tracemalloc`

```python
import tracemalloc

tracemalloc.start()

# Code to inspect for memory leaks
leaky_list = [x for x in range(500_000)]

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ 🧠 Top 3 Memory Allocations ]")
for stat in top_stats[:3]:
    print(stat)

tracemalloc.stop()
```

---

## 📝 Quick Exercise

**Prompt**:
Profile a script that searches for duplicates across 100,000 strings using a list lookup vs a set lookup, logging call counts and total execution time.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import time

items = [f"item_{i}" for i in range(100_000)]
search_targets = [f"item_{i}" for i in range(99_000, 100_000)]

# Benchmark 1: List Lookup O(n)
start = time.perf_counter()
found_list = [x for x in search_targets if x in items]
time_list = time.perf_counter() - start

# Benchmark 2: Set Lookup O(1)
items_set = set(items)
start = time.perf_counter()
found_set = [x for x in search_targets if x in items_set]
time_set = time.perf_counter() - start

print(f"List Lookup Time: {time_list:.4f}s")
print(f"Set Lookup Time:  {time_set:.6f}s (Speedup: {time_list / time_set:.1f}x faster!)")
```
</details>
