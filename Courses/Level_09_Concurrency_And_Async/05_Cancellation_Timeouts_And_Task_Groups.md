# Lesson 5: Cancellation, Timeouts & Task Groups

**Prerequisites:** Levels 1–8 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Cancellation_Timeouts_And_Task_Groups.py`.

Give concurrent work a parent lifetime and an explicit failure policy. A task that is no longer needed should release its resources without hiding cancellation from the code that owns it.

## 1. Treat cancellation as control flow

Task cancellation requests that CancelledError be raised at a suspension point. Cleanup should usually occur in finally and then allow cancellation to propagate. Swallowing that signal can interfere with task groups and timeouts that rely on it.

CancelledError is a BaseException subtype, so a normal except Exception does not generally catch it. A catch-all BaseException handler is therefore especially risky. If cleanup itself awaits work, understand its cancellation and lifetime requirements instead of assuming a print statement establishes that resources are released.

## 2. Put a deadline around an operation

`asyncio.timeout(seconds)` is an async context manager. If its deadline expires, it cancels the current task internally and transforms the corresponding cancellation into TimeoutError when leaving the context. Catch TimeoutError outside the block.

```python
import asyncio

async def main():
    try:
        async with asyncio.timeout(0):
            await asyncio.sleep(1)
    except TimeoutError:
        print("Timed out")

if __name__ == "__main__":
    asyncio.run(main())
```

A zero deadline is already due and cancellation occurs at the next opportunity to suspend. This example does not assert an exact wall-clock duration. A timeout cannot preempt ordinary CPU code that never yields control to the event loop.

## 3. Own child tasks with a TaskGroup

An async TaskGroup waits for its child tasks when the block exits. A child failure generally triggers cancellation of siblings and is reported through grouped exceptions. Exception groups can be handled with except* for selected member types; that syntax partitions group members rather than catching a single ordinary exception.

Use a group when the children form one operation with a shared lifetime. If each input should yield an independent success/error report, catch documented per-item failures inside the worker and return a structured result. Let unexpected programming failures still abort the group.

An async context manager implements `__aenter__` and `__aexit__`, which can themselves await work. `contextlib.asynccontextmanager` adapts a one-yield async generator, analogous to the synchronous contextmanager from Level 7. Keep required release in finally. API lifespan hooks later use this pattern to own client and engine cleanup.

## 4. Distinguish cancellation from external interruption

Cancelling a coroutine does not guarantee an external service rolled back its side effects. A request may have reached a server before its client stopped waiting. A blocked thread may continue after its async wrapper is cancelled.

Use operation identifiers, idempotent effects, and bounded external timeouts where the application requires them. This lesson demonstrates local cleanup order, which is one necessary part of correct cancellation rather than a claim about every external effect.

References: [Cancellation and timeouts](https://docs.python.org/3.13/library/asyncio-task.html#task-cancellation).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether finally runs before TimeoutError is caught outside the block.
2. **Explain:** Explain why a blocking CPU loop can defeat a cooperative timeout.
3. **Modify:** Give child tasks a TaskGroup owner rather than leaving them unobserved.
4. **Debug:** Remove a catch-all handler that turns cancellation into an apparent success.

<details>
<summary>Hints</summary>

The finally block belongs inside the operation; the timeout handler belongs outside the timeout context.

</details>

## Independent task: cancellation, timeouts & task groups

In `Practice/05_Cancellation_Timeouts_And_Task_Groups.py`, complete this task:

Define async work(events) that awaits a long cooperative sleep and appends closed in finally. In main, await it inside asyncio.timeout(0), catch TimeoutError outside, print Timed out, and then print whether events equals ["closed"]. The cleanup must be real, not a fixed success flag.

Expected output:

```text
Timed out
Cleaned up: True
```
