# Lesson 1: Workloads, Concurrency & Measurement

**Prerequisites:** Levels 1–8. **Practice file:** `Practice/01_Workloads_Concurrency_And_Measurement.py`.

Distinguish making progress on several tasks from executing Python work in parallel. Choose a model based on where time is spent and what resources the work consumes.

## 1. Identify waiting and computation

I/O-bound work spends substantial time waiting for files, sockets, databases, or other external operations. CPU-bound work spends time performing computation. Real applications often mix them, so classify a measured stage rather than attaching one permanent label to an entire program.

Concurrency allows several tasks to make progress over overlapping lifetimes. Parallelism executes work at the same time on multiple processing units. A single event loop can be concurrent while running Python instructions on one thread.

## 2. Understand the interpreter assumption

In a conventional GIL-enabled CPython build, threads do not generally run CPU-bound Python bytecode in parallel. Threads can still help overlap many blocking I/O operations. Processes have separate interpreter state and can use multiple cores, at the cost of startup, serialization, and interprocess communication.

Free-threaded builds change some assumptions and are studied explicitly in Level 12. Record the interpreter build before interpreting a benchmark. Do not claim that every thread-based program is faster or that every CPU operation benefits from a process pool.

## 3. Time an operation honestly

```python
from time import perf_counter_ns

def measure(operation):
    start = perf_counter_ns()
    result = operation()
    elapsed = perf_counter_ns() - start
    return result, elapsed

result, elapsed = measure(lambda: sum(range(10)))
print(result)  # 45
```

The result establishes what work was performed; elapsed describes that invocation. Repeat with a controlled workload before drawing a conclusion. Include task creation and data transfer when those costs are part of the application operation you intend to improve.

## 4. Bound the resource you actually consume

More concurrent tasks can exhaust file descriptors, database connections, memory, or service limits. Limit the active resource and describe whether pending tasks are also bounded. A semaphore can limit active operations while an already-created million-task list still consumes substantial memory.

A synthetic sleep can demonstrate scheduling but does not establish real network throughput. The capstone uses real local file reads and reports correct per-file outcomes rather than promising a hardware-dependent speedup.

References: [Threading](https://docs.python.org/3.13/library/threading.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the result of the measured sum before considering its duration.
2. **Explain:** Explain why concurrency and parallelism are distinct.
3. **Modify:** Time setup separately from repeated operations and label both scopes.
4. **Debug:** Find a benchmark that confuses simulated waiting with measured external I/O.

<details>
<summary>Hints</summary>

Return both the real result and the observed duration; they answer different questions.

</details>

## Independent task: workloads, concurrency & measurement

In `Practice/01_Workloads_Concurrency_And_Measurement.py`, complete this task:

Implement measure(operation) returning the callable's result and an actual perf_counter_ns elapsed duration. Measure sum(range(1000)). Print the result and whether the observed duration is nonnegative. Do not hardcode a timing value or use sleep as the measured computation.

Expected output:

```text
Result: 499500
Nonnegative duration: True
```
