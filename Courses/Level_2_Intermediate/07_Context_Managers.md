# Lesson 7: Resource Management: Context Managers & `contextlib`

In production engineering, resource leaks—such as unclosed database connections, dangling socket file descriptors, or unreleased thread locks—degrade server performance and lead to catastrophic crashes. **Context Managers** provide deterministic resource acquisition and teardown (`setup -> execute -> cleanup`) via the `with` statement. In this lesson, you will master the Context Manager Protocol (`__enter__`, `__exit__`) and generator-based context utilities using `contextlib`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the lifecycle of resource management (`setup` $\rightarrow$ `work` $\rightarrow$ `teardown`).
2. Implement class-based Context Managers using `__enter__` and `__exit__`.
3. Handle and selectively suppress runtime exceptions inside `__exit__`.
4. Build lightweight generator-based context managers using `@contextlib.contextmanager`.
5. Manage non-file resources (database transactions, thread locks, timing blocks, temporary environment settings).

---

## 1. The Context Manager Protocol (`__enter__` and `__exit__`)

Any class that implements `__enter__()` and `__exit__()` satisfies Python's Context Manager protocol:

```
with MyContextManager() as resource:
    1. Python calls obj.__enter__() and assigns return value to 'resource'
    2. Executes indented code block
    3. Python unconditionally calls obj.__exit__(exc_type, exc_val, exc_tb)
```

```python
class DatabaseConnectionLock:
    """Manages acquisition and release of a database connection lock."""
    
    def __init__(self, db_name: str):
        self.db_name = db_name

    def __enter__(self):
        print(f"🔒 [ENTER] Acquired exclusive lock on database '{self.db_name}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"🔓 [EXIT] Released exclusive lock on database '{self.db_name}'")
        # Returning None (or False) allows any raised exception to propagate upward

# Usage:
with DatabaseConnectionLock("CustomerMasterDB") as conn:
    print("  -> Performing critical schema migration...")
# Lock is guaranteed to be released even if migration raises an error!
```

---

## 2. Exception Handling in `__exit__`

The `__exit__` method receives 3 arguments describing any exception raised within the `with` block:
- `exc_type`: The exception class (e.g. `ValueError`)
- `exc_val`: The exception instance object
- `exc_tb`: The traceback object

> [!NOTE]
> If `__exit__` returns `True`, Python **suppresses the exception**, preventing it from bubbling up to crash the program. If it returns `False` or `None`, the exception is re-raised.

```python
class ErrorSuppressor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"⚠️ [SUPPRESSED] Intercepted and handled: {exc_val}")
            return True # Suppresses the error!

with ErrorSuppressor():
    result = 100 / 0 # Would normally crash with ZeroDivisionError
print("Program continues safely after suppressed error.")
```

---

---

## 4. Advanced Resource Orchestration with `contextlib.ExitStack`

When you need to open an arbitrary, dynamic number of resources (such as opening 10 files simultaneously whose filenames are supplied at runtime), nesting `with` statements becomes impossible. **`ExitStack`** manages a dynamic stack of context managers programmatically:

```python
from contextlib import ExitStack
from pathlib import Path

def merge_log_files(input_paths: list[Path], output_path: Path):
    with ExitStack() as stack:
        # Dynamically acquire and manage all input file handles:
        files = [stack.enter_context(open(p, "r", encoding="utf-8")) for p in input_paths]
        out_file = stack.enter_context(open(output_path, "w", encoding="utf-8"))

        for f in files:
            out_file.write(f.read() + "\n")
    # All files are unconditionally closed simultaneously here!
```

---

## 5. Built-in `contextlib` Power Utilities

Python provides ready-to-use context managers in the standard library:

### 1. `contextlib.suppress(*exceptions)`
Replaces noisy `try...except Pass:` blocks:
```python
import contextlib
import os

# Safely remove file without crashing if it doesn't exist:
with contextlib.suppress(FileNotFoundError):
    os.remove("temp_cache.tmp")
```

### 2. `contextlib.redirect_stdout`
Redirects `print()` outputs directly to a file or in-memory string stream:
```python
import io
import contextlib

buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    print("This goes into the buffer, not the terminal!")

captured_text = buffer.getvalue()
```

---

## 💻 Code Example & Reference

The following real-life program models an **Atomic Financial Database Transaction Manager with Automatic Rollback and Audit Sandboxing**, demonstrating class-based and generator-based context managers:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Atomic Financial Database Transaction Manager
# =====================================================================

import copy
import contextlib

class DatabaseTransaction:
    """Class-based context manager for atomic database transaction units.
    
    Guarantees ACID atomicity: If an error occurs within the transaction block,
    all changes are rolled back to the initial snapshot state.
    """

    def __init__(self, database_table: dict, transaction_id: str):
        self.table = database_table
        self.txn_id = transaction_id
        self._snapshot = None

    def __enter__(self):
        # Create an isolated backup snapshot before work begins
        self._snapshot = copy.deepcopy(self.table)
        print(f"🔄 [BEGIN TXN: {self.txn_id}] Snapshot created. In-flight modifications starting...")
        return self.table

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # An error occurred: Revert table state to snapshot
            self.table.clear()
            self.table.update(self._snapshot)
            print(f"🚨 [ROLLBACK TXN: {self.txn_id}] Error detected: {exc_val}")
            print(f"    -> All database modifications safely reverted to pre-transaction snapshot.")
            return False # Propagate error to caller for audit logging
        else:
            # Success: Commit changes
            print(f"✅ [COMMIT TXN: {self.txn_id}] Transaction committed successfully to disk.")
            return True


# Generator-based temporary configuration override context manager
@contextlib.contextmanager
def temporary_security_level(system_config: dict, temp_level: str):
    original_level = system_config.get("SECURITY_MODE", "STANDARD")
    system_config["SECURITY_MODE"] = temp_level
    print(f"🛡️ [SECURITY CONTEXT] Elevated to '{temp_level}' mode.")
    try:
        yield system_config
    finally:
        system_config["SECURITY_MODE"] = original_level
        print(f"🛡️ [SECURITY CONTEXT] Restored back to '{original_level}' mode.")


# System Simulation Run
master_ledger = {
    "ACC-101": {"owner": "Elena", "balance": 1000.00},
    "ACC-102": {"owner": "Marcus", "balance": 500.00},
}
system_settings = {"SECURITY_MODE": "STANDARD"}

print("=" * 70)
print(f"{'ATOMIC TRANSACTION CONTEXT MANAGER PIPELINE':^70}")
print("=" * 70)

# Test 1: Successful Atomic Wire Transfer
print("\n--- Test 1: Successful Transfer of $200 from Elena to Marcus ---")
try:
    with DatabaseTransaction(master_ledger, "TXN-SUCCESS-01") as db:
        db["ACC-101"]["balance"] -= 200.00
        db["ACC-102"]["balance"] += 200.00
except Exception as err:
    print(f"Caught error: {err}")

print(f"Ledger Balances: Elena: ${master_ledger['ACC-101']['balance']:.2f} | Marcus: ${master_ledger['ACC-102']['balance']:.2f}")

# Test 2: Failed Transfer (Mid-transaction crash triggers atomic rollback)
print("\n--- Test 2: Transfer with Mid-Flight Failure (Triggering Rollback) ---")
try:
    with DatabaseTransaction(master_ledger, "TXN-FAIL-02") as db:
        db["ACC-101"]["balance"] -= 500.00 # Elena debited
        # Unexpected network failure before Marcus is credited:
        raise ConnectionResetError("Lost socket connectivity to banking interchange!")
        db["ACC-102"]["balance"] += 500.00
except ConnectionResetError as net_err:
    print(f"Caught expected error in caller: {net_err}")

print(f"Ledger Balances: Elena: ${master_ledger['ACC-101']['balance']:.2f} | Marcus: ${master_ledger['ACC-102']['balance']:.2f}")

# Test 3: Generator Context Manager Test
print("\n--- Test 3: Temporary Security Elevation Block ---")
with temporary_security_level(system_settings, "AIR_GAPPED_MAX_ENCRYPTION"):
    print(f"  -> Currently running inside protected block: {system_settings['SECURITY_MODE']}")
print(f"  -> Outside block: {system_settings['SECURITY_MODE']}")
print("=" * 70)
```

### 🔍 Code Explanation:
- **`DatabaseTransaction.__enter__`**: Deep-copies the dictionary table state to create a restore point.
- **`DatabaseTransaction.__exit__`**: Detects exceptions, restores the table snapshot, and logs the rollback action before allowing the caller to catch the error.
- **`@contextlib.contextmanager`**: `temporary_security_level` temporarily overrides system flags and guarantees restoration via its `finally` clause.

---

## 📝 Quick Exercise: Temporary API Key Lease & Sandbox Isolation Context Manager

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master the context manager protocol, `__enter__`, `__exit__`, error suppression, `contextlib.contextmanager`, `ExitStack`, and resource leasing:

---

### 🟢 Tier 1: Basic Context Managers (Exercises 1–3)

#### 🔹 Exercise 1: Console Header/Footer Banner Manager
* **Goal**: Write `class BannerBox` printing `=== START ===` on enter and `=== END ===` on exit.

#### 🔹 Exercise 2: File Handle Wrapper with Explicit Close
* **Goal**: Implement `class ManagedFileReader` wrapping a file open/close lifecycle using `__enter__` and `__exit__`.

#### 🔹 Exercise 3: Temporary Working Directory Switcher
* **Goal**: Using `os.chdir()`, write `class ChangeDir(target_path)` switching directory on enter and restoring previous path on exit.

---

### 🟡 Tier 2: Exception Handling & Generator Contexts (Exercises 4–6)

#### 🔹 Exercise 4: Selective Error Suppressor
* **Goal**: Class `SuppressSpecific(*exceptions)` returning `True` in `__exit__` only if raised error matches given types.

#### 🔹 Exercise 5: Benchmark Timer with `@contextlib.contextmanager`
* **Goal**: Write `@contextmanager def time_block(label: str)` yielding control and printing elapsed milliseconds in `finally`.

#### 🔹 Exercise 6: In-Memory List Snapshot Rollback
* **Goal**: Write `@contextmanager def list_transaction(target_list)` deep-copying list on enter and restoring on exception.

---

### 🟠 Tier 3: Advanced Resource Orchestration (Exercises 7–9)

#### 🔹 Exercise 7: Dynamic Multi-File Merger with `contextlib.ExitStack`
* **Goal**: Use `ExitStack` to open $N$ dynamic input text files and concatenate their contents into a master file.

#### 🔹 Exercise 8: Temporary Mock System Config
* **Goal**: Generator context manager overriding `os.environ` keys during the `with` block and restoring them afterwards.

#### 🔹 Exercise 9: Stdout Output Interceptor
* **Goal**: Write `@contextmanager def capture_stdout()` redirecting `sys.stdout` to a `StringIO` buffer and returning the captured string.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Temporary API Key Lease & Sandbox Isolation Context Manager
* **Goal**: Implement `SecureSessionLease` class manager with safe error suppression, paired with `@temporary_env_var` configuration sandbox.

---

## 📝 Quick Exercise: Temporary API Key Lease & Sandbox Isolation Context Manager

### 🏢 Real-Life Scenario
You are developing a secure multi-tenant cloud test runner. Test suites require leasing a temporary cryptographic API token and executing in an isolated sandbox environment. When the test finishes (or crashes with an assertion error), the context manager must revoke the token, clean up allocated test files, and return resource metrics.

### 📋 Requirements
1. **Define Class `SecureSessionLease`**:
   - Constructor: `__init__(self, session_id: str, tenant_name: str)`
   - `__enter__(self)`:
     - Sets `self.is_active = True`.
     - Prints `f"🔑 [SESSION LEASED] ID: {self.session_id} for tenant '{self.tenant_name}'"`.
     - Returns `self`.
   - `__exit__(self, exc_type, exc_val, exc_tb)`:
     - Sets `self.is_active = False`.
     - Prints `f"🔒 [SESSION REVOKED] ID: {self.session_id} has been revoked and purged"`.
     - If `exc_type` is not `None`, print `f"⚠️ Session terminated due to error: {exc_val}"`.
     - Returns `True` to safely suppress and handle the exception cleanly.
2. **Define Generator `@contextlib.contextmanager def temporary_env_var(env_dict: dict, key: str, value: str)`**:
   - Sets `env_dict[key] = value`.
   - Yields control.
   - In `finally`: Restores original key value (or deletes key if it didn't exist).
3. Execute test runs inside both context managers and verify teardown.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 context managers, `__enter__`, `__exit__`, and `contextlib` with Level 1 dictionaries, conditionals, and formatted outputs.

### 🎯 Expected Output
```text
==================================================
        SECURE API SESSION & CONTEXT RUNNER       
==================================================
🔑 [SESSION LEASED] ID: SESS-909 for tenant 'Alpha Corp'
  -> Running integration tests with API Token: SESS-909
  -> Active status: True
🔒 [SESSION REVOKED] ID: SESS-909 has been revoked and purged

🔑 [SESSION LEASED] ID: SESS-910 for tenant 'Beta LLC'
  -> Running test that encounters runtime assertion...
🔒 [SESSION REVOKED] ID: SESS-910 has been revoked and purged
⚠️ Session terminated due to error: Simulated API Timeout
Program completed all test runs safely.
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Session Lease & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Secure Session Lease Engine
# =====================================================================
import contextlib

class SecureSessionLease:
    def __init__(self, session_id: str, tenant_name: str):
        self.session_id = session_id
        self.tenant_name = tenant_name
        self.is_active = False

    def __enter__(self):
        self.is_active = True
        print(f"🔑 [SESSION LEASED] ID: {self.session_id} for tenant '{self.tenant_name}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.is_active = False
        print(f"🔒 [SESSION REVOKED] ID: {self.session_id} has been revoked and purged")
        if exc_type is not None:
            print(f"⚠️ Session terminated due to error: {exc_val}")
            return True


@contextlib.contextmanager
def temporary_env_var(env_dict: dict, key: str, value: str):
    had_key = key in env_dict
    old_value = env_dict.get(key)
    env_dict[key] = value
    try:
        yield
    finally:
        if had_key:
            env_dict[key] = old_value
        else:
            env_dict.pop(key, None)


print("==================================================")
print("        SECURE API SESSION & CONTEXT RUNNER       ")
print("==================================================")

with SecureSessionLease("SESS-909", "Alpha Corp") as session:
    print(f"  -> Running integration tests with API Token: {session.session_id}")
    print(f"  -> Active status: {session.is_active}")

print()

with SecureSessionLease("SESS-910", "Beta LLC") as session:
    print("  -> Running test that encounters runtime assertion...")
    raise TimeoutError("Simulated API Timeout")

print("Program completed all test runs safely.")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
class BannerBox:
    def __enter__(self): print("=== START ==="); return self
    def __exit__(self, *a): print("=== END ===")

# Ex 2:
class ManagedFileReader:
    def __init__(self, path: str, mode="r"): self.p, self.m = path, mode
    def __enter__(self): self.f = open(self.p, self.m); return self.f
    def __exit__(self, *a): self.f.close()

# Ex 3:
import os
class ChangeDir:
    def __init__(self, p): self.p, self.prev = p, None
    def __enter__(self): self.prev = os.getcwd(); os.chdir(self.p)
    def __exit__(self, *a): os.chdir(self.prev)

# Ex 4:
class SuppressSpecific:
    def __init__(self, *errs): self.errs = errs
    def __enter__(self): return self
    def __exit__(self, t, v, tb): return t is not None and issubclass(t, self.errs)

# Ex 5:
import time
@contextlib.contextmanager
def time_block(label: str):
    t0 = time.perf_counter()
    try: yield
    finally: print(f"{label}: {(time.perf_counter()-t0)*1000:.2f}ms")

# Ex 6:
import copy
@contextlib.contextmanager
def list_transaction(lst):
    snap = copy.deepcopy(lst)
    try: yield lst
    except Exception:
        lst.clear()
        lst.extend(snap)
        raise

# Ex 7:
from contextlib import ExitStack
def merge_files(paths, out):
    with ExitStack() as s:
        ins = [s.enter_context(open(p)) for p in paths]
        o = s.enter_context(open(out, "w"))
        for f in ins: o.write(f.read() + "\n")

# Ex 8:
@contextlib.contextmanager
def mock_env(k, v):
    old = os.environ.get(k)
    os.environ[k] = v
    try: yield
    finally:
        if old is None: os.environ.pop(k, None)
        else: os.environ[k] = old

# Ex 9:
import io, sys
@contextlib.contextmanager
def capture_stdout():
    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try: yield buf
    finally: sys.stdout = old
```
</details>

