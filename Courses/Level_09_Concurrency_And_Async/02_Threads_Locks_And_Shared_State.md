# Lesson 2: Threads, Locks & Shared State

**Prerequisites:** Levels 1–8 and Lesson 1 of this level. **Practice file:** `Practice/02_Threads_Locks_And_Shared_State.py`.

Coordinate threads around an invariant rather than relying on incidental execution order. A shared object needs an explicit rule for who may change it and when readers can observe a completed result.

## 1. Launch and join work

A Thread receives a target callable and arguments. start schedules it to run; join waits for its completion. Calling the target directly just executes it synchronously in the caller.

```python
from threading import Thread

results = []
def work():
    results.append("finished")

thread = Thread(target=work)
thread.start()
thread.join()
print(results)
```

Do not assume scheduling order matches creation order. Join before interpreting final state. An exception in a raw thread is not automatically returned to the launching thread as a normal function exception; futures can provide a more convenient result/error boundary.

## 2. Protect a read-modify-write operation

An increment can involve reading a value, computing a new value, and storing it. The GIL is not a public guarantee that every multi-step operation on application state is atomic. Use a Lock around the whole invariant-preserving update.

With a lock's context manager, acquisition occurs on entry and release on exit, including exceptional exit. Protecting only the final assignment can still allow two threads to compute from the same old value. Readers may also require the same lock when they need a consistent intermediate snapshot.

## 3. Minimize the critical section

Do expensive independent computation outside the lock, then protect only the shared state transition. Holding a lock while waiting for slow I/O can serialize otherwise independent work. Acquiring several locks in inconsistent orders can create deadlock.

A lock does not make the underlying algorithm correct. Define which state it protects, which operations must acquire it, and what invariant holds when it is released. Avoid a mix of protected and unprotected writes to the same state.

## 4. Make completion and errors observable

Use explicit join or an executor context rather than relying on process shutdown. Daemon threads can be stopped during interpreter exit without completing application cleanup. A cooperative stopping signal is often more useful than abandoning work.

For repeatable demonstrations, report the final joined result rather than a particular interleaving of diagnostic prints. That result should be derived from actual completed operations, not the number of threads you intended to start.

## Supply arguments and a shared lock

`Thread(target=work, args=(counter,))` passes counter to work in the new thread. The comma makes a one-element argument tuple. Import `Lock` from threading and create it once for the state it protects. `with lock:` acquires it before the body and releases it afterward. Every method changing the same shared counter must acquire that same lock; constructing a new lock inside each call would not coordinate those calls.

References: [Locks](https://docs.python.org/3.13/library/threading.html#lock-objects).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict why final output must follow joins.
2. **Explain:** Explain the invariant protected by a counter lock.
3. **Modify:** Move independent calculation outside a critical section.
4. **Debug:** Find an unprotected update that bypasses an otherwise correct lock.

<details>
<summary>Hints</summary>

Use one lock shared by all increments of that same counter.

</details>

## Independent task: threads, locks & shared state

In `Practice/02_Threads_Locks_And_Shared_State.py`, complete this task:

Define a Counter with an integer value and a Lock. Its increment method must protect the full value update. Start four threads, each calling increment 1000 times, join them all, and print the actual final value. Do not set the value directly to the expected total.

Expected output:

```text
4000
```
