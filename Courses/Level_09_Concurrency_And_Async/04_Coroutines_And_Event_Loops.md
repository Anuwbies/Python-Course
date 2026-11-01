# Lesson 4: Coroutines & Event Loops

**Prerequisites:** Levels 1–8 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Coroutines_And_Event_Loops.py`.

Express cooperative waiting with async and await while keeping blocking work out of the event-loop thread. Calling a coroutine function creates an awaitable; it does not automatically finish the operation.

## 1. Enter an async operation

`async def` defines a coroutine function. Calling it creates a coroutine object. `await` runs or waits for an awaitable within an async function, allowing the event loop to make progress on other ready tasks when the awaited operation suspends.

```python
import asyncio

async def double(value):
    await asyncio.sleep(0)
    return value * 2

async def main():
    print(await double(3))

if __name__ == "__main__":
    asyncio.run(main())
```

The zero-duration sleep deliberately yields control for this scheduling example. It is not a network request and does not establish I/O throughput. `asyncio.run` owns a top-level event-loop lifetime and should not be nested inside an already running event loop.

## 2. Schedule overlap deliberately

Awaiting one operation and then another runs those lifetimes sequentially. Creating tasks or using gather can schedule several coroutine operations concurrently. Gather returns successful results in input order, even when completion order differs.

An unawaited coroutine can produce a warning rather than a result. A created task also needs an owner that observes its completion or failure. Losing task references or ignoring exceptions does not make the work reliably run in the background.

## 3. Do not block cooperative progress

A normal time.sleep inside an async function blocks its executing thread. A long CPU loop also monopolizes the event loop until it yields. Use a suitable async I/O library or asyncio.to_thread for a blocking I/O call that is safe to run in a worker thread.

To_thread does not generally make CPU-bound Python work parallel on a GIL-enabled interpreter, and cancelling the awaiting task does not forcibly interrupt an already running blocking thread function. The underlying operation still needs its own bounded lifetime when that matters.

## 4. Preserve interface and error ownership

An async function still has input, result, side-effect, and failure contracts. Scheduling syntax does not replace them. Decide whether a collection of tasks fails as a unit or collects individual errors; the next lesson develops structured failure and cancellation.

For this task, return actual values after an await point and display them from the launcher. Avoid predicting a particular sequence of diagnostic prints from concurrently scheduled bodies unless ordering itself is part of the design.

## Call gather and offload a real blocking call

For a bounded group, `await asyncio.gather(double(1), double(2))` returns an input-order list. With an existing sequence, `await asyncio.gather(*(double(value) for value in values))` uses a generator expression and star expansion, both from Level 7, to supply separate awaitables. Keep this construction for a known bounded input.

For a blocking text read, `await asyncio.to_thread(path.read_text, encoding="utf-8")` passes the bound read_text callable and its keyword argument to a worker thread. Passing `path.read_text(...)` instead would perform the blocking call immediately before to_thread can offload it. Catch documented read/decode exceptions around the await that observes that call's failure.

References: [Asyncio tasks](https://docs.python.org/3.13/library/asyncio-task.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the returned order from gather for three input coroutines.
2. **Explain:** Explain why a coroutine object is not its eventual result.
3. **Modify:** Replace a blocking wait in an async body with a cooperative wait.
4. **Debug:** Find a created coroutine that is never awaited or scheduled.

<details>
<summary>Hints</summary>

Gather receives awaitables; the launcher must itself be awaited by the top-level runner.

</details>

## Independent task: coroutines & event loops

In `Practice/04_Coroutines_And_Event_Loops.py`, complete this task:

Define async_double(value) that awaits asyncio.sleep(0) and returns twice the value. In an async main, use gather for inputs 1,2,3 and print the resulting list. Launch with asyncio.run under a main guard. Do not hardcode the result list.

Expected output:

```text
[2, 4, 6]
```
