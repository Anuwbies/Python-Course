# Capstone Project 3.1: Multi-Process Priority Job Queue & Worker Pool

## 📌 Project Overview
Build a resilient, high-throughput **Multi-Process Background Job Queue System** in pure Python (similar to Celery or RQ). The system coordinates a Master Broker process and multiple Worker processes across CPU cores, scheduling computational tasks based on priority using a custom Binary Min-Heap, handling worker heartbeats, managing dead-letter retry queues, and ensuring clean graceful shutdowns upon `SIGINT`/`SIGTERM`.

---

## 🎯 Learning Objectives
- **Multiprocessing**: Spawning and managing child worker processes using `multiprocessing.Process`, `multiprocessing.Queue`, and `multiprocessing.Event`.
- **Custom Data Structures**: Implementing an in-memory thread/process-safe Binary Min-Heap priority queue from scratch.
- **Inter-Process Synchronization (IPC)**: Passing serialized tasks, heartbeats, and result payloads between master and worker processes without race conditions.
- **Fault Tolerance**: Implementing automatic task retries with exponential backoff and dead-letter queue routing for failing jobs.
- **Graceful Signal Handling**: Intercepting termination signals to allow running workers to finish active jobs before exit.

---

## 🏗️ System Architecture

```text
               +----------------------------------+
               |        Master Job Broker         |
               |  (Priority Min-Heap Scheduler)   |
               +----------------------------------+
                     |                      ^
   [Task Ingestion]  |                      | [Results & Heartbeats]
                     v                      |
           +-------------------+  +-------------------+
           |    Task Queue     |  |   Result Queue    |
           | (multiprocessing) |  | (multiprocessing) |
           +-------------------+  +-------------------+
                     |                      ^
         +-----------+-----------+          |
         |                       |          |
         v                       v          |
+-----------------+     +-----------------+ |
| Worker Process 1|     | Worker Process 2| |
| (CPU Core 0)    |     | (CPU Core 1)    | |
| + execute_task()|     | + execute_task()| |
+-----------------+     +-----------------+ |
         |                       |          |
         +-----------------------+----------+
```

---

## 📋 Functional Requirements

### 1. Custom Min-Heap Priority Task Scheduler
Tasks are assigned a priority integer ($1 = \text{CRITICAL}$, $2 = \text{HIGH}$, $3 = \text{NORMAL}$, $4 = \text{LOW}$). Implement a binary heap where popping returns the highest-priority task in $O(\log N)$ time:
```python
@dataclass(order=True)
class Task:
    priority: int
    task_id: str = field(compare=False)
    func_name: str = field(compare=False)
    args: tuple = field(compare=False)
    kwargs: dict = field(compare=False)
    max_retries: int = field(compare=False, default=3)
    retry_count: int = field(compare=False, default=0)
```

### 2. Multi-Process Worker Pool
- Master spawns $N$ independent worker processes (where $N = \text{os.cpu\_count()}$).
- Workers continuously pull tasks from the shared IPC queue, execute the target callable dynamically, capture stdout/return values/exceptions, and publish status updates to a result queue.
- If a task raises an unhandled exception, the broker increments `retry_count`. If `retry_count < max_retries`, it re-queues the task with exponential backoff. Otherwise, it transfers it to a `DeadLetterQueue`.

### 3. Heartbeat & Worker Health Monitor
Workers report periodic heartbeats every 2 seconds. If a worker process hangs or is killed by the OS (OOM), the broker detects the missing heartbeat, logs the failure, restarts the worker process, and reschedules the abandoned task.

### 4. Signal Handling & Graceful Teardown
When the user presses `Ctrl+C` (`SIGINT`):
1. Stop accepting new tasks.
2. Signal workers to finish their current job via `multiprocessing.Event`.
3. Wait up to 5 seconds for workers to terminate (`worker.join(timeout=5)`).
4. Terminate any unresponsive processes and persist uncompleted queue state to disk (`queue_snapshot.json`).

---

## 📐 Phased Implementation Guide

### Phase 1: Binary Min-Heap Priority Queue
```python
class PriorityTaskQueue:
    def __init__(self):
        self._heap = []
        self._lock = threading.Lock()

    def push(self, task: Task) -> None:
        with self._lock:
            self._heap.append(task)
            self._sift_up(len(self._heap) - 1)

    def pop(self) -> Task:
        with self._lock:
            if not self._heap:
                raise IndexError("Queue is empty")
            # Swap root with last element
            root = self._heap[0]
            last = self._heap.pop()
            if self._heap:
                self._heap[0] = last
                self._sift_down(0)
            return root
```

### Phase 2: Worker Process Loop
Implement the standalone top-level worker process function listening on IPC task queues.

### Phase 3: Broker Coordinator & CLI Dashboard
Build the master coordinator orchestrating job ingestion, result aggregation, and terminal metrics display.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Priority Preemption** | Enqueue 5 LOW tasks, then enqueue 1 CRITICAL task | Worker immediately picks CRITICAL task before remaining LOW tasks |
| **Worker Crash Simulation** | Run a task that executes `os._exit(1)` | Master detects worker exit, respawns replacement worker, reschedules task |
| **Flaky Task Retries** | Task fails on first 2 attempts, succeeds on 3rd | Successfully retries twice and records success on 3rd attempt |
| **Graceful Teardown** | Send `SIGINT` while 4 CPU-heavy tasks are running | Master waits for active tasks to complete before cleanly exiting |

---

## 🚀 Bonus Challenges
- **Shared Memory Cache**: Use `multiprocessing.shared_memory.SharedMemory` to pass large arrays/data payloads between processes with zero copy overhead.
- **Web UI Dashboard**: Add an interactive terminal curses UI showing real-time worker CPU utilization and processed task rates.
