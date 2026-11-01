# Level 9 capstone: Bounded concurrent local-file processor

**Prerequisites:** [all lessons in Level 9](../../Courses/Level_09_Concurrency_And_Async/README.md). **Submission:** `Practice/project.py`.

Count whitespace-separated words in real UTF-8 files while bounding concurrent and queued work. Use a fixed set of async workers and a bounded asyncio.Queue. File reads are blocking operations delegated through asyncio.to_thread; they are not performed directly on the event-loop thread.

A documented per-file read/decode failure becomes an error result for that file; unexpected programming errors remain failures of the task group. Cancellation propagates, and each retrieved queue item has matching task_done accounting. The worker count must be positive.

The input is a bounded list of paths with unique file names. Results use those names as identifiers. Each worker reads one complete file, so memory can still depend on file sizes; this is bounded job concurrency, not a claim of constant memory for arbitrarily large files.

## Project task

Implement async `count_files(paths, workers=2)` returning a dictionary by unique file name. Each result is either {"count": integer} or {"error": exception_type_name}. Reject nonpositive workers or duplicate names. Use a queue of capacity workers*2, exactly workers worker tasks in a TaskGroup, one None sentinel per worker, and task_done in finally. Catch only OSError and UnicodeError as per-file failures.

Demonstrate two actual temporary files a.txt containing `one two` and b.txt containing `three`, plus a missing.txt path. Print alphabetical outcomes. Do not hardcode counts or fabricate a missing-file result without attempting the read.

Expected output:

```text
a.txt: 2
b.txt: 1
missing.txt: ERROR FileNotFoundError
```
