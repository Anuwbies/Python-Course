# Lesson 6: First-Class Functions, Closures & Decorators

Decorators are one of Python's most powerful, expressive, and distinctive design patterns. They allow you to dynamically modify, extend, or monitor the behavior of functions and methods without modifying their source code.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand First-Class Functions (passing and returning functions).
2. Create lexical Closures.
3. Write custom function decorators.
4. Use `functools.wraps` to preserve function signatures and docstrings.
5. Create decorators that accept arguments (e.g. `@retry(max_attempts=3)`).

---

## 1. First-Class Functions & Closures

In Python, functions are **first-class citizens**: they can be assigned to variables, passed as arguments, and returned from other functions.

```python
def make_multiplier(factor):
    # Inner function forms a closure over 'factor'
    def multiplier(number):
        return number * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5)) # 10
print(triple(5)) # 15
```

---

## 2. Anatomy of a Decorator

A decorator is simply a function that takes another function as input, wraps it with extra behavior, and returns the wrapped function.

```python
import time
import functools

def timer_decorator(func):
    """Measures and logs the execution time of any function."""
    @functools.wraps(func) # Preserves func.__name__ and docstrings
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"⏱️ [{func.__name__}] executed in {duration:.6f} seconds.")
        return result
    return wrapper

# Applying the decorator using @ syntax:
@timer_decorator
def calculate_heavy_sum(n):
    return sum(i * i for i in range(n))

calculate_heavy_sum(1_000_000)
```

---

## 3. Real-World Decorator: Retry Logic on Failure

```python
import time
import functools

def retry(max_attempts=3, delay_seconds=1.0):
    """Decorator factory that retries flaky network/database calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    attempts += 1
                    print(f"⚠️ Attempt {attempts}/{max_attempts} failed for '{func.__name__}': {error}")
                    if attempts >= max_attempts:
                        raise error
                    time.sleep(delay_seconds)
        return wrapper
    return decorator

@retry(max_attempts=3, delay_seconds=0.5)
def fetch_remote_data():
    # Simulating a flaky network request
    import random
    if random.random() < 0.7:
        raise ConnectionError("Server unavailable")
    return {"status": 200, "data": "Success!"}
```

---

## 📝 Quick Exercise

**Prompt**:
Write an `@auth_required(role)` decorator:
1. Accepts a required role string (e.g. `"admin"`).
2. Inspects a keyword argument `current_user = {"name": "...", "role": "..."}` passed to the decorated function.
3. If the user's role matches, execute the function; otherwise raise a `PermissionError("Access Denied")`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import functools

def auth_required(required_role: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if not user or user.get("role") != required_role:
                raise PermissionError(f"Access Denied: Requires '{required_role}' role.")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@auth_required("admin")
def delete_database_record(record_id: int, current_user: dict = None):
    print(f"✅ Record {record_id} successfully deleted by {current_user['name']}.")

# Testing:
admin_user = {"name": "Alice", "role": "admin"}
guest_user = {"name": "Bob", "role": "guest"}

delete_database_record(42, current_user=admin_user) # Works!
# delete_database_record(42, current_user=guest_user) # ❌ Raises PermissionError
```
</details>

---

## 🧠 Self-Check Quiz

1. **What does `@my_decorator` placed directly above `def my_func():` do behind the scenes?**
   - A) Compiles the function to C
   - B) Executes `my_func = my_decorator(my_func)`
   - C) Deletes the function
   - D) Runs the function in a background process
   *(Answer: B)*

2. **Why is `@functools.wraps(func)` used inside a custom decorator wrapper?**
   - A) To prevent memory leaks
   - B) To ensure the original function name (`__name__`) and docstring (`__doc__`) are preserved
   - C) It is required by Python syntax
   - D) To make recursion faster
   *(Answer: B)*
