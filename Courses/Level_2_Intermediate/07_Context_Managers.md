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

## 3. Generator Context Managers with `contextlib`

Writing class boilerplate for simple setups can be verbose. The `@contextlib.contextmanager` decorator converts a simple generator function into a full context manager using a `try...yield...finally` pattern:

```python
import contextlib
import time

@contextlib.contextmanager
def benchmark_timer(label: str):
    start = time.perf_counter()
    try:
        yield # Code inside the 'with' block executes here
    finally:
        elapsed = time.perf_counter() - start
        print(f"⏱️ [{label}] Execution completed in {elapsed * 1000:.2f} ms")

with benchmark_timer("Data Ingestion Stage"):
    # Simulate work
    time.sleep(0.02)
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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import contextlib

# 1. Class-Based Session Context Manager (Level 2)
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
            return True # Suppress error for clean test runner shutdown


# 2. Generator-Based Environment Variable Context Manager (Level 2)
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


# 3. Execution Simulation
print("==================================================")
print("        SECURE API SESSION & CONTEXT RUNNER       ")
print("==================================================")

# Test 1: Clean test run
with SecureSessionLease("SESS-909", "Alpha Corp") as session:
    print(f"  -> Running integration tests with API Token: {session.session_id}")
    print(f"  -> Active status: {session.is_active}")

print()

# Test 2: Test run with suppressed error
with SecureSessionLease("SESS-910", "Beta LLC") as session:
    print("  -> Running test that encounters runtime assertion...")
    raise TimeoutError("Simulated API Timeout")

print("Program completed all test runs safely.")
print("==================================================")
```

**Explanation of the Solution:**
- `SecureSessionLease.__enter__` initializes credentials, and `__exit__` guarantees revocation even if the inner code raises `TimeoutError`.
- Returning `True` from `__exit__` suppresses the runtime test error, allowing the test suite runner to proceed.
</details>
