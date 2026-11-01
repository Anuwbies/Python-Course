# Lesson 5: Custom Context Managers

**Prerequisites:** Levels 1–6 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Custom_Context_Managers.py`.

Express a resource lifetime as one visible block, including the failure path. A context manager should release what it owns and suppress an exception only when that is an explicit part of its contract.

## 1. Enter and exit the block

A context manager implements entry and exit behavior for with. In the class protocol, __enter__ returns the value bound after as, and __exit__ receives exception information when the body fails. A truthy return from __exit__ suppresses that exception, which can be a serious unintended change in behavior.

Use a context manager for ownership, such as opening a resource, acquiring a lock, or installing temporary state. It is not needed merely to group ordinary statements visually. The block should tell a reader which lifetime is controlled.

## 2. Build the protocol from a generator

The contextlib.contextmanager decorator adapts a generator with one yield into a context manager. Code before yield enters; the yielded value becomes the as binding; code afterward completes the exit. Put required cleanup in finally so it also runs when the with body raises.

```python
from contextlib import contextmanager

@contextmanager
def session(events):
    events.append("enter")
    try:
        yield "active"
    finally:
        events.append("exit")
```

Yield exactly once for an entered manager. Returning before yield or yielding several times violates the protocol. The decorator handles the mechanics, but your cleanup and suppression policy remain your responsibility.

## 3. Preserve failure information

If a body raises ValueError, the exception is delivered back into the generator at the yield point. A finally block can clean up and allow the error to propagate. An except that silently passes could instead turn a failed operation into an apparently successful block.

A resource cleanup failure can itself obscure an earlier exception. Keep cleanup narrow, idempotent when appropriate, and understandable. Use existing standard-library managers when they already implement the intended lifetime correctly.

## 4. Consume lazy work inside its resource lifetime

A generator reading a file requires the handle to stay open during iteration. Yielding a stream from a managed block is useful only when the caller consumes it inside that same with block. Returning a lazy iterator after closing its file creates a lifetime mismatch.

The capstone combines a context-managed source with a lazy parser and a separate aggregator. Each part needs a contract for both values and resource ownership; the pipeline is not correct merely because each function works independently on a list.

References: [Contextlib](https://docs.python.org/3.13/library/contextlib.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the event order when a with body raises.
2. **Explain:** Explain why finally is needed around the yield.
3. **Modify:** Use the yielded value without giving the caller ownership of cleanup.
4. **Debug:** Find a context manager that accidentally swallows every body exception.

<details>
<summary>Hints</summary>

Catch outside the managed block so the event order exposes cleanup during propagation.

</details>

## Independent task: custom context managers

In `Practice/05_Custom_Context_Managers.py`, complete this task:

Implement `session(events)` using contextmanager: append `"enter"` on entry, yield `"active"`, and append `"exit"` in finally on every exit. Preserve exceptions raised by the body. Use it once successfully, appending its yielded value to events. Use it a second time with a deliberate ValueError in the body, catch that error outside the with, and append `"caught"`. Print the final event list. Cleanup must occur before caught.

Expected output:

```text
['enter', 'active', 'exit', 'enter', 'exit', 'caught']
```
