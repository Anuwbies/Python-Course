# Lesson 6: First-Class Functions, Closures & Decorators

In Python, functions are **first-class citizens**—they can be assigned to variables, passed as arguments into other functions, stored in collections, and returned from other functions. Building upon this foundation, **Decorators** allow engineers to dynamically inject cross-cutting behavior (such as authentication, caching, rate-limiting, timing, and error-retrying) around existing functions without modifying their underlying source code.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Treat functions as first-class objects (higher-order functions).
2. Understand lexical variable capture and build stateful **Closures** using the `nonlocal` keyword.
3. Write clean, reusable **Function Decorators** accepting arbitrary `*args` and `**kwargs`.
4. Preserve docstrings and function names using `functools.wraps`.
5. Implement advanced **Parameterized Decorators** that accept configuration arguments.
6. Chain multiple decorators together in proper execution order.

---

## 1. First-Class Functions & Higher-Order Functions

```python
def format_usd(amount: float) -> str:
    return f"${amount:,.2f}"

def format_eur(amount: float) -> str:
    return f"€{amount:,.2f}"

# Higher-order function: accepts a function as an argument
def print_invoice_item(name: str, price: float, formatter_fn) -> None:
    print(f"Item: {name:<20} | Price: {formatter_fn(price)}")

print_invoice_item("Cloud Server", 1450.00, format_usd)
print_invoice_item("Domain Name", 14.99, format_eur)
```

---

## 2. Lexical Closures & The `nonlocal` Keyword

A **Closure** is a nested function that remembers and accesses variables from its enclosing lexical scope, even after the outer function has finished executing:

```python
def create_rate_limiter(max_requests: int):
    """Factory creating an isolated rate counter closure."""
    call_count = 0 # Enclosed state variable

    def limiter():
        nonlocal call_count # Binds to outer call_count
        call_count += 1
        if call_count > max_requests:
            print(f"❌ Rate limit exceeded ({call_count}/{max_requests})!")
            return False
        print(f"✅ Request allowed ({call_count}/{max_requests})")
        return True

    return limiter

api_limiter = create_rate_limiter(max_requests=2)
api_limiter() # True (1/2)
api_limiter() # True (2/2)
api_limiter() # False (3/2 - Blocked)
```

---

## 3. Function Decorators & `functools.wraps`

A decorator is a syntactic wrapper around a function:
```python
@my_decorator
def target_function(): ...
# Equivalent to: target_function = my_decorator(target_function)
```

> [!IMPORTANT]
> Always decorate wrapper functions with `@functools.wraps(fn)`. Without `@wraps`, the decorated function loses its original `__name__` and `__doc__`, breaking debugging and reflection tools.

```python
import functools
import time

def execution_timer(func):
    """Measures wall-clock execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        print(f"⏱️ [{func.__name__}] Execution took {elapsed * 1000:.3f} ms")
        return result
    return wrapper

@execution_timer
def compute_heavy_hash(data: str) -> int:
    """Computes a mock cryptographic hash."""
    time.sleep(0.05)
    return hash(data)

compute_heavy_hash("payload_data")
print(f"Function name preserved: {compute_heavy_hash.__name__}") # 'compute_heavy_hash'
```

---

---

## 5. Under the Hood: Closures & `__closure__` Cells

When an inner function captures a variable from an outer scope, CPython creates a **`cell` object** on the heap to store the reference:

```python
def make_multiplier(factor: int):
    def multiply(x: int) -> int:
        return x * factor
    return multiply

double = make_multiplier(2)
# Inspecting the closure cell:
print(double.__closure__) # (<cell at 0x7f...: int object at 0x...>,)
print(double.__closure__[0].cell_contents) # 2
```

---

## 6. Class Decorators & Callable Class Decorators

### 1. Decorating Classes
You can apply decorators directly to class definitions to automatically inject attributes or register classes in a plugin registry:

```python
def add_audit_timestamp(cls):
    """Class decorator injecting a creation timestamp."""
    orig_init = cls.__init__
    def new_init(self, *args, **kwargs):
        self.created_at = time.time()
        orig_init(self, *args, **kwargs)
    cls.__init__ = new_init
    return cls

@add_audit_timestamp
class UserAccount:
    def __init__(self, username: str):
        self.username = username
```

### 2. Decorators Implemented as Classes (`__call__`)
```python
class CallCounter:
    """Decorator maintaining persistent invocation count."""
    def __init__(self, func):
        self.func = func
        self.count = 0
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"[{self.func.__name__}] Invocation #{self.count}")
        return self.func(*args, **kwargs)
```

---

## 7. Decorator Stacking Execution Order

When multiple decorators are stacked:
```python
@decorator_A
@decorator_B
def target(): pass
```
- **Definition Time (Wrapping)**: Evaluates from **Bottom to Top**: `target = decorator_A(decorator_B(target))`
- **Execution Time (Call)**: Evaluates from **Top to Bottom (Outside-In)**: `decorator_A` runs first $\rightarrow$ calls `decorator_B` $\rightarrow$ calls `target`.

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise API Endpoint Security, Caching & Resilience Stack**, combining closures, metadata preservation, parameterized retry logic, and role-based access enforcement:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Enterprise Microservice API Decorator Framework
# =====================================================================

import functools
import time

# 1. Parameterized RBAC Role-Guard Decorator (Lesson 6)
def require_role(allowed_roles: set[str]):
    """Enforces that the current authenticated context contains required roles."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_context: dict, *args, **kwargs):
            user_role = user_context.get("role", "GUEST")
            if user_role not in allowed_roles:
                raise PermissionError(f"Access Denied: Role '{user_role}' is unauthorized for {func.__name__}()")
            return func(user_context, *args, **kwargs)
        return wrapper
    return decorator


# 2. In-Memory Cache / Memoization Decorator with Closure (Lesson 6)
def memoize_cache(ttl_seconds: int = 60):
    """Caches deterministic API responses in a closure-backed memory cache."""
    def decorator(func):
        cache: dict[str, tuple[any, float]] = {} # Closure state

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create hashable cache key from arguments
            cache_key = f"{args[1:]}:{sorted(kwargs.items())}" # Skip user_context in key
            now = time.time()
            
            if cache_key in cache:
                cached_result, timestamp = cache[cache_key]
                if now - timestamp < ttl_seconds:
                    print(f"⚡ [CACHE HIT] {func.__name__} returned instant cached response.")
                    return cached_result

            # Compute and store fresh result
            result = func(*args, **kwargs)
            cache[cache_key] = (result, now)
            print(f"🔄 [CACHE MISS] {func.__name__} executed live database query.")
            return result
        return wrapper
    return decorator


# 3. Microservice Endpoint Definitions with Stacked Decorators
@require_role({"ADMIN", "BILLING_OPS"})
@memoize_cache(ttl_seconds=30)
def fetch_financial_audit(user_context: dict, quarter: str, fiscal_year: int) -> dict:
    """Simulates expensive database financial report generation."""
    # Simulated database work
    return {
        "fiscal_period": f"{quarter}-{fiscal_year}",
        "gross_revenue": 4_850_000.00,
        "operating_margin_pct": 24.5,
        "audited_by": user_context["username"]
    }


# 4. System Execution Simulation
admin_user = {"username": "Elena Rostova", "role": "ADMIN"}
guest_user = {"username": "Anonymous", "role": "GUEST"}

print("=" * 70)
print(f"{'MICROSERVICE SECURITY & CACHING DECORATOR SUITE':^70}")
print("=" * 70)

# Request 1: Initial call (Cache Miss + Admin Approved)
print("\n--- Request #1: Admin queries Q3-2026 ---")
report1 = fetch_financial_audit(admin_user, "Q3", 2026)
print(f"Report: {report1['fiscal_period']} | Revenue: ${report1['gross_revenue']:,.2f}")

# Request 2: Immediate duplicate call (Cache Hit)
print("\n--- Request #2: Admin re-queries Q3-2026 ---")
report2 = fetch_financial_audit(admin_user, "Q3", 2026)
print(f"Report: {report2['fiscal_period']} | Revenue: ${report2['gross_revenue']:,.2f}")

# Request 3: Unauthorized role access attempt
print("\n--- Request #3: Guest attempts to access financial audit ---")
try:
    fetch_financial_audit(guest_user, "Q3", 2026)
except PermissionError as auth_err:
    print(f"🚨 Security Guard Blocked Request: {auth_err}")

print("=" * 70)
```

### 🔍 Code Explanation:
- **`require_role` (Parameterized Decorator)**: Intercepts function execution to inspect incoming `user_context` before permitting access to protected business routines.
- **`memoize_cache` (Stateful Closure)**: Maintains an isolated `cache` dictionary across function calls, serving cached answers transparently on matching parameters.
- **Decorator Stacking**: `@require_role` and `@memoize_cache` combine orthogonally to provide clean separation of concerns without cluttering the business function.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master higher-order functions, closures, `functools.wraps`, parameterized decorators, class decorators, and memoization:

---

### 🟢 Tier 1: Closures & Basic Function Decorators (Exercises 1–3)

#### 🔹 Exercise 1: Multiplier Factory Closure
* **Goal**: Write `make_multiplier(n: int)` returning a closure that multiplies any input by `n`.

#### 🔹 Exercise 2: Function Call Logger Decorator
* **Goal**: Write `@log_call` printing function name, passed `*args`, and returned result using `@functools.wraps`.

#### 🔹 Exercise 3: Uppercase String Return Decorator
* **Goal**: Write `@uppercase_output` decorator that automatically converts string return values to uppercase.

---

### 🟡 Tier 2: Stateful Closures & Performance Decorators (Exercises 4–6)

#### 🔹 Exercise 4: Stateful Running Average Closure
* **Goal**: Write `create_averager()` maintaining cumulative sum and count using `nonlocal`.

#### 🔹 Exercise 5: Wall-Clock Benchmark Timer
* **Goal**: Write `@benchmark` decorator measuring and printing execution duration with `time.perf_counter()`.

#### 🔹 Exercise 6: In-Memory Memoization / Cache Decorator
* **Goal**: Write `@memoize` caching results in a closure dictionary `cache[(args, tuple(kwargs.items()))]`. Test on recursive Fibonacci.

---

### 🟠 Tier 3: Parameterized & Class Decorators (Exercises 7–9)

#### 🔹 Exercise 7: Parameterized Rate Limiter Decorator
* **Goal**: Write `@rate_limit(max_per_minute: int)` decorator enforcing a maximum call frequency.

#### 🔹 Exercise 8: Parameterized Retry Decorator
* **Goal**: Write `@retry(retries=3, delay_sec=0.1)` retrying transient network errors before raising.

#### 🔹 Exercise 9: Class-Based Decorator (`__call__`)
* **Goal**: Implement `class ExecutionCounter` tracking invocation count as a class instance and decorating functions.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Database Query Retry & Performance Profiler Suite
* **Goal**: Combine `@audit_profile` (execution duration instrumentation) and `@retry_query(max_retries=3)` (error catch and retry) over a flaky SQL query simulation.

---

## 📝 Quick Exercise: Database Query Retry & Performance Profiler Decorator Framework

### 🏢 Real-Life Scenario
You are developing the database driver resiliency middleware for a high-traffic web application. Database queries occasionally encounter transient network dropouts. You must build a `@retry_query(max_retries=3)` decorator that automatically catches transient exceptions, retries the query, and an `@audit_profile` decorator that records the execution time.

### 📋 Requirements
1. **Define `@audit_profile` Decorator**:
   - Uses `time.perf_counter()` to measure function duration.
   - Preserves metadata using `@functools.wraps`.
   - Prints `f"[AUDIT] Query '{func.__name__}' finished in {elapsed_ms:.2f}ms"`.
2. **Define `@retry_query(max_retries=3)` Parameterized Decorator**:
   - Accepts `max_retries: int = 3`.
   - Attempts executing the wrapped function.
   - If an exception occurs, catches the error, prints `f"⚠️ Attempt {attempt}/{max_retries} failed: {err}. Retrying..."`, and continues.
   - If all attempts fail, raises the final exception.
3. **Decorate Mock Query Function `execute_db_query(query_sql: str, should_fail_times: int)`**:
   - Uses an internal closure or counter to simulate failing a specific number of times before succeeding.
4. Execute test queries and observe the automatic retries and execution profiling.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 decorators, closures, `functools.wraps`, and custom error handling with Level 1 loops, functions, and string formatting.

### 🎯 Expected Output
```text
==================================================
        DATABASE RESILIENCE DECORATOR SUITE       
==================================================
--- Test 1: Query failing twice before succeeding ---
⚠️ Attempt 1/3 failed: Transient network drop. Retrying...
⚠️ Attempt 2/3 failed: Transient network drop. Retrying...
[AUDIT] Query 'execute_db_query' finished in 0.12ms
✅ Query Succeeded: Returned 14 records for 'SELECT * FROM users'
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Decorator Suite & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Database Resilience Decorator Suite
# =====================================================================
import functools
import time

def audit_profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        print(f"[AUDIT] Query '{func.__name__}' finished in {elapsed_ms:.2f}ms")
        return result
    return wrapper


def retry_query(max_retries: int = 3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    last_exception = err
                    print(f"⚠️ Attempt {attempt}/{max_retries} failed: {err}. Retrying...")
            raise last_exception
        return wrapper
    return decorator


call_counter = 0

@audit_profile
@retry_query(max_retries=3)
def execute_db_query(query_sql: str, failures_to_simulate: int = 2) -> dict:
    global call_counter
    call_counter += 1
    if call_counter <= failures_to_simulate:
        raise ConnectionResetError("Transient network drop")
    return {"status": "SUCCESS", "rows": 14, "query": query_sql}


print("==================================================")
print("        DATABASE RESILIENCE DECORATOR SUITE       ")
print("==================================================")
print("--- Test 1: Query failing twice before succeeding ---")

try:
    res = execute_db_query("SELECT * FROM users", failures_to_simulate=2)
    print(f"✅ Query Succeeded: Returned {res['rows']} records for '{res['query']}'")
except Exception as fatal_err:
    print(f"❌ Fatal Failure: {fatal_err}")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
def make_multiplier(n: int):
    return lambda x: x * n

# Ex 2:
def log_call(fn):
    @functools.wraps(fn)
    def w(*args, **kw):
        res = fn(*args, **kw)
        print(f"[{fn.__name__}] args={args} -> res={res}")
        return res
    return w

# Ex 3:
def uppercase_output(fn):
    @functools.wraps(fn)
    def w(*args, **kw):
        return str(fn(*args, **kw)).upper()
    return w

# Ex 4:
def create_averager():
    tot, cnt = 0.0, 0
    def averager(val: float) -> float:
        nonlocal tot, cnt
        tot += val
        cnt += 1
        return tot / cnt
    return averager

# Ex 5:
def benchmark(fn):
    @functools.wraps(fn)
    def w(*args, **kw):
        t0 = time.perf_counter()
        r = fn(*args, **kw)
        print(f"{fn.__name__} took {(time.perf_counter()-t0)*1000:.2f}ms")
        return r
    return w

# Ex 6:
def memoize(fn):
    cache = {}
    @functools.wraps(fn)
    def w(*args):
        if args not in cache: cache[args] = fn(*args)
        return cache[args]
    return w

# Ex 7:
def rate_limit(max_calls: int):
    def dec(fn):
        cnt = 0
        @functools.wraps(fn)
        def w(*a, **kw):
            nonlocal cnt
            cnt += 1
            if cnt > max_calls: raise RuntimeError("Rate exceeded")
            return fn(*a, **kw)
        return w
    return dec

# Ex 8:
# Parameterized retry decorator demonstrated in main Exercise 10 above.

# Ex 9:
class ExecutionCounter:
    def __init__(self, fn):
        self.fn, self.calls = fn, 0
        functools.update_wrapper(self, fn)
    def __call__(self, *a, **kw):
        self.calls += 1
        return self.fn(*a, **kw)
```
</details>

