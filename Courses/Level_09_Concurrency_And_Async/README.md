# Level 9: Concurrency & Async

**Stage:** Advanced. **Prerequisites:** Levels 1–8.

Choose a concurrency model for the workload, bound the relevant resources, and demonstrate correct result, failure, shutdown, and cancellation behavior.

## Reading order

| Lesson | Guide | Saved task |
| --- | --- | --- |
| 1 | [Workloads, Concurrency & Measurement](01_Workloads_Concurrency_And_Measurement.md) | [Practice](Practice/01_Workloads_Concurrency_And_Measurement.py) |
| 2 | [Threads, Locks & Shared State](02_Threads_Locks_And_Shared_State.md) | [Practice](Practice/02_Threads_Locks_And_Shared_State.py) |
| 3 | [Processes, Futures & Serialization](03_Processes_Futures_And_Serialization.md) | [Practice](Practice/03_Processes_Futures_And_Serialization.py) |
| 4 | [Coroutines & Event Loops](04_Coroutines_And_Event_Loops.md) | [Practice](Practice/04_Coroutines_And_Event_Loops.py) |
| 5 | [Cancellation, Timeouts & Task Groups](05_Cancellation_Timeouts_And_Task_Groups.md) | [Practice](Practice/05_Cancellation_Timeouts_And_Task_Groups.py) |
| 6 | [Bounds, Backpressure & Work Queues](06_Bounds_Backpressure_And_Work_Queues.md) | [Practice](Practice/06_Bounds_Backpressure_And_Work_Queues.py) |

Continue with the [Bounded concurrent local-file processor capstone](../../Capstones/Level_09_Concurrency_And_Async/README.md).

## Working through this level

Read the detailed explanation, trace the examples, and complete the practice ladder before the independent task. Each file in `Practice/` contains the full task, accepted inputs, and expected behavior as comments. Write your own implementation below those comments. Reference implementations are in `Solutions/`; compare them after an attempt.

Ask the assistant to review your saved submission when ready. Progress is recorded manually after review, including revisions and topics to revisit. Independent-task sections contain only the assignment and its expected behavior.

## Environment and run commands

All references use the standard library and Python 3.13. Run multiprocessing scripts as files with their main guards. Async references own their top-level event loop through asyncio.run; do not paste that launcher inside an already running notebook loop.

## Advancement

Choose a concurrency model for the workload, bound the relevant resources, and demonstrate correct result, failure, shutdown, and cancellation behavior.

Demonstrate the capstone with its documented normal, boundary, and failure cases and explain one small requirement change. Record evidence in [the Level 9 progress record](../../Progress/Level_09_Concurrency_And_Async.md). Running a reference does not complete your own submission.

## Scope and next steps

The file processor reads whole files and assumes a bounded input list. Network services and durable multiuser data arrive in Level 10; operational queues and recovery policies follow in Level 11.
