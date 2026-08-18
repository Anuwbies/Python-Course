# Lesson 7: Context Managers & the with Statement

Resources like open files, database connections, locks, and network sockets must be closed when your program is done with them. In this lesson, you will learn how to write custom **Context Managers** to guarantee deterministic resource cleanup.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the Context Manager protocol (`__enter__` and `__exit__`).
2. Write Class-Based Context Managers.
3. Write Generator-Based Context Managers using `@contextlib.contextmanager`.
4. Suppress or handle exceptions inside context managers.

---

## 1. The Context Manager Protocol (`__enter__` and `__exit__`)

When you write `with ContextObject() as alias:`, Python executes:
1. `__enter__()`: Sets up the resource and optionally returns an object for the `as` alias.
2. The code block inside the `with` statement runs.
3. `__exit__(exc_type, exc_val, exc_tb)`: Guarantees teardown cleanup, even if an unhandled exception occurred!

```python
import time

class PerformanceTimer:
    """Class-based context manager that measures block execution time."""
    def __init__(self, label: str):
        self.label = label
        self.start_time = 0.0

    def __enter__(self):
        print(f"⏳ Starting [{self.label}]...")
        self.start_time = time.perf_counter()
        return self # Value passed to 'as timer'

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.perf_counter() - self.start_time
        print(f"⏱️ [{self.label}] took {duration:.4f} seconds.")
        # Return False so any unhandled exceptions propagate upwards normally
        return False

# Usage:
with PerformanceTimer("Heavy Calculation") as timer:
    result = sum(i ** 2 for i in range(1_000_000))
```

---

## 2. Generator-Based Context Managers with `@contextmanager`

Instead of creating a full class with `__enter__` and `__exit__`, you can write a generator function decorated with `@contextlib.contextmanager`:

```python
from contextlib import contextmanager
import os

@contextmanager
def temporary_working_directory(new_dir: str):
    """Safely switches current directory and restores original directory upon exit."""
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield # Control yields to code inside the with block
    finally:
        # Guarantees switching back even if code inside with fails!
        os.chdir(previous_dir)
```

---

## 3. Suppressing Exceptions with `contextlib.suppress`

```python
from contextlib import suppress

# Instead of clumsy try/except pass for expected file missing errors:
with suppress(FileNotFoundError):
    os.remove("temp_cache.tmp")
```

---

## 📝 Quick Exercise

**Prompt**:
Create a context manager `DatabaseTransaction`:
1. `__enter__`: Prints `"Beginning DB transaction..."` and returns a mock connection object.
2. `__exit__`: If no exceptions occurred, prints `"✅ Commit transaction"`. If an exception occurred, prints `"❌ Rollback transaction due to error!"` and allows the error to propagate.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class DatabaseTransaction:
    def __enter__(self):
        print("▶️ Beginning DB transaction...")
        return {"connection": "active_conn_#1"}

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            print("✅ Commit transaction successfully!")
        else:
            print(f"❌ Rollback transaction due to error: {exc_val}")
        return False # Propagate error to caller

# Testing successful commit:
with DatabaseTransaction() as tx:
    print("Writing records...")

# Testing automatic rollback:
try:
    with DatabaseTransaction() as tx:
        print("Writing records...")
        raise RuntimeError("Disk write failure!")
except RuntimeError:
    print("Caught error outside context manager.")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What must `__exit__` return if you want to swallow/suppress an exception raised in the with block?**
   - A) `None`
   - B) `True`
   - C) `False`
   - D) `1`
   *(Answer: B)*

2. **In `@contextmanager`, where does setup code go relative to the `yield` statement?**
   - A) After `yield`
   - B) Inside `__init__`
   - C) Before `yield`
   - D) Setup code is not allowed
   *(Answer: C)*
