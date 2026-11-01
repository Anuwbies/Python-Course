# Lesson 6: Bounds, Backpressure & Work Queues

**Prerequisites:** Levels 1–8 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Bounds_Backpressure_And_Work_Queues.py`.

Limit active operations and pending work separately. A concurrency limit is meaningful only when you identify the resource it protects and the amount of state still retained elsewhere.

## 1. Limit active access with a semaphore

An asyncio.Semaphore starts with a capacity. Entering its async context acquires a slot; leaving releases it even when an exception occurs. Put the actual resource-consuming operation inside that context.

```python
import asyncio

async def operation(value, semaphore):
    async with semaphore:
        await asyncio.sleep(0)
        return value * 2
```

Creating one task for every input and protecting each with a semaphore bounds active work, but still creates all task objects. That can be appropriate for a small bounded list and inappropriate for an enormous stream.

## 2. Apply backpressure to production

A queue with maxsize makes await queue.put wait when pending capacity is full. A fixed number of workers consume items. This bounds queued pending jobs independently of the source's production rate.

Call task_done exactly once for each successful get, including sentinel items if they were queued. Queue.join waits for that accounting to reach zero. Missing a task_done on an error path can make the application wait indefinitely even though no useful work remains.

## 3. Stop workers intentionally

A reserved sentinel such as None can tell each worker to stop. Queue one sentinel per worker after real jobs have been produced. The sentinel must be outside the valid job domain, or a legitimate input could be mistaken for shutdown.

Use a TaskGroup so unexpected worker errors cancel related work instead of leaving a producer waiting forever. Recoverable per-item errors should become explicit result records. Cancellation should propagate through cleanup rather than be converted into another normal item.

## 4. Measure the intended bound

An event-loop-owned active counter can record how many coroutine operations occupy a semaphore at once when all changes occur on that event loop without an intervening await. This is a specific cooperative-state design, not a general thread-safety guarantee.

Record a maximum and compare it with the configured limit. Do not require the maximum to equal the limit: workload size and scheduling may keep actual overlap lower. The capstone uses a queue to also bound pending jobs and real threaded file reads rather than simulated sleeps.

## Combine a bounded queue with owned workers

This small complete pattern has one worker and a queue that can hold two pending numbers. A retrieved None ends the worker; it is not a valid number in this example.

```python
import asyncio

async def queued_total(values):
    queue = asyncio.Queue(maxsize=2)
    total = 0
    async def worker():
        nonlocal total
        while True:
            value = await queue.get()
            try:
                if value is None:
                    return
                total += value
            finally:
                queue.task_done()
    async with asyncio.TaskGroup() as group:
        group.create_task(worker())
        for value in values:
            await queue.put(value)
        await queue.put(None)
        await queue.join()
    return total

if __name__ == "__main__":
    print(asyncio.run(queued_total([2, 3])))  # 5
```

Queue.get waits for an item; queue.put waits for capacity. TaskGroup.create_task registers a child whose completion belongs to the group. For several fixed workers, create that many children and send that many sentinels. To record a high-water mark, `maximum = max(maximum, active)` retains the larger numeric value. Update the counter without an await between reading and writing it, and decrement in finally. Do not use that event-loop assumption for shared state modified by worker threads.

References: [Asyncio queues](https://docs.python.org/3.13/library/asyncio-queue.html), [Semaphores](https://docs.python.org/3.13/library/asyncio-sync.html#semaphore).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict how a semaphore limit differs from the number of created task objects.
2. **Explain:** Explain why queue.task_done belongs in a finally path.
3. **Modify:** Reserve one sentinel outside the valid input domain.
4. **Debug:** Find a producer/worker failure that leaves queue.join waiting forever.

<details>
<summary>Hints</summary>

Increment after acquiring a slot and decrement in finally before releasing it.

</details>

## Independent task: bounds, backpressure & work queues

In `Practice/06_Bounds_Backpressure_And_Work_Queues.py`, complete this task:

Define async run_bounded(values, limit) for positive integer limit. Use a semaphore around each operation, track active and maximum active counts in event-loop-owned state, yield with sleep(0), and return input-order doubled results plus the observed maximum. Print results for [1,2,3] at limit 2 and whether the maximum was at most 2. Reject a nonpositive limit with ValueError.

Expected output:

```text
[2, 4, 6]
Within limit: True
```
