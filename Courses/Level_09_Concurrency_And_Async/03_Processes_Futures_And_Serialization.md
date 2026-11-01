# Lesson 3: Processes, Futures & Serialization

**Prerequisites:** Levels 1–8 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Processes_Futures_And_Serialization.py`.

Use separate processes for independent computational work when the workload justifies their overhead. Treat submitted arguments and returned values as messages rather than shared Python memory.

## 1. Submit an importable callable

ProcessPoolExecutor starts worker interpreters and serializes calls and results. In a spawn-based environment such as Windows, worker code must be importable. A top-level function is a suitable target; an arbitrary local closure or lambda normally is not.

```python
def square(number):
    return number * number
```

Protect launching code with `if __name__ == "__main__":` so importing the module in a worker does not recursively start more pools. This is an application entry-point requirement, not an optional formatting style.

## 2. Interpret futures and map order

submit returns a Future representing a pending result or exception. Calling result waits and propagates the worker's exception to the caller. Executor.map returns results in input order, which differs from completion-order iteration with as_completed.

Choose ordering according to the interface. A user report may require input order even when tasks finish differently. A progress display may prefer completion order while storing an explicit input identifier alongside each result.

## 3. Include transfer and lifecycle costs

Workers do not mutate the parent's ordinary list simply by changing a deserialized argument. Large data transfers can dominate small computations. Consider chunk size, process startup, memory duplication, and whether a long-lived pool is appropriate.

A with block shuts down the executor and waits according to its documented lifecycle. A worker crash and a raised task exception are different failure modes. Do not catch every failure and return a success-shaped zero result; surface enough context for the caller to decide what to retry.

## 4. Bound work and cancellation expectations

A future can be cancelled before work starts, but cancelling an already running process task is not equivalent to safely interrupting its function. Design small bounded units and explicit stop behavior where possible.

Processes help when independent CPU work is large enough to amortize overhead. The lesson's small square example teaches importability, result flow, and ordering; it is not a benchmark claiming process startup accelerates trivial arithmetic.

## Construct and consume the executor

Import ProcessPoolExecutor from concurrent.futures. `with ProcessPoolExecutor(max_workers=2) as executor:` owns two worker processes. `list(executor.map(square, [1, 2, 3]))` consumes their results in input order and observes task failures while consuming. Put that with block under the main guard, leaving square defined at module scope. Materializing this small result is intentional; for larger workloads, choose a bounded submission design rather than assuming map's result iterator bounds all pending work.

References: [Concurrent futures](https://docs.python.org/3.13/library/concurrent.futures.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the order returned by map even if completion order differs.
2. **Explain:** Explain why a main guard matters for spawned workers.
3. **Modify:** Move a nested worker function to an importable module scope.
4. **Debug:** Find a design that serializes a huge dataset for every tiny task.

<details>
<summary>Hints</summary>

The worker callable must be importable, and pool creation belongs under the entry-point guard.

</details>

## Independent task: processes, futures & serialization

In `Practice/03_Processes_Futures_And_Serialization.py`, complete this task:

Define square(number) at module scope. In a guarded main block, use ProcessPoolExecutor with two workers to map it over [1,2,3]. Materialize and print the results in input order. Use an executor context manager and do not launch a pool during import.

Expected output:

```text
[1, 4, 9]
```
