# Lesson 4: Custom Exceptions & Exception Hierarchies

In professional software development, catching generic `Exception` everywhere hides bugs. You need domain-specific exceptions to communicate exactly what went wrong in your application.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Create custom exception classes inheriting from `Exception`.
2. Build domain-specific **Exception Hierarchies**.
3. Attach custom metadata and error codes to exceptions.
4. Chain exceptions using `raise ... from original_error`.

---

## 1. Defining Custom Exceptions

To create a custom exception, create a class that inherits from Python's built-in `Exception`:

```python
class InsufficientFundsError(Exception):
    """Raised when an account withdrawal exceeds available balance."""
    def __init__(self, requested: float, available: float):
        self.requested = requested
        self.available = available
        super().__init__(
            f"Cannot withdraw ${requested:.2f}; only ${available:.2f} available."
        )

# Raising and catching:
def withdraw_funds(balance: float, amount: float) -> float:
    if amount > balance:
        raise InsufficientFundsError(requested=amount, available=balance)
    return balance - amount

try:
    withdraw_funds(50.0, 100.0)
except InsufficientFundsError as err:
    print(f"❌ Error: {err}")
    print(f"Deficit: ${err.requested - err.available:.2f}")
```

---

## 2. Building an Exception Hierarchy

In large systems (e.g. an API or database driver), define a root base exception so callers can catch all errors from your library with a single clause:

```python
# Root Base Exception for your application/library
class AppError(Exception):
    """Base exception for all errors in this application."""
    pass

# Specific Sub-exceptions
class DatabaseError(AppError):
    pass

class RecordNotFoundError(DatabaseError):
    pass

class AuthenticationError(AppError):
    pass

class TokenExpiredError(AuthenticationError):
    pass
```

```python
# Caller can catch specifically or broadly:
try:
    raise TokenExpiredError("Session has timed out.")
except AuthenticationError as e:
    # Catches TokenExpiredError because it is a subclass of AuthenticationError!
    print(f"Auth issue: {e}")
except AppError as e:
    print(f"General app error: {e}")
```

---

## 3. Exception Chaining (`raise ... from`)

When translating a low-level error (like `sqlite3.OperationalError`) into a business-level error (`DatabaseConnectionError`), chain them so the original traceback is not lost:

```python
try:
    # Low-level network socket failure
    raise ConnectionResetError("Socket reset by peer")
except ConnectionResetError as original_error:
    raise DatabaseError("Unable to query database") from original_error
```

---

## 📝 Quick Exercise

**Prompt**:
1. Create a base exception `ValidationError(Exception)`.
2. Create two subclasses: `InvalidEmailError` and `WeakPasswordError` (with a `min_length` attribute).
3. Write a `register_user(email, password)` function that validates both and raises the appropriate custom exception.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class ValidationError(Exception):
    """Base exception for user validation failures."""
    pass

class InvalidEmailError(ValidationError):
    """Raised when email lacks @ or domain."""
    pass

class WeakPasswordError(ValidationError):
    """Raised when password length is below required minimum."""
    def __init__(self, length: int, min_length: int = 8):
        self.length = length
        self.min_length = min_length
        super().__init__(f"Password length ({length}) is too short! Minimum is {min_length} characters.")

def register_user(email: str, password: str) -> bool:
    if "@" not in email or "." not in email:
        raise InvalidEmailError(f"'{email}' is not a valid email address.")
    if len(password) < 8:
        raise WeakPasswordError(len(password), min_length=8)
    print("User registered successfully! 🎉")
    return True

# Testing:
try:
    register_user("testuser", "secret123")
except ValidationError as e:
    print(f"Validation failed: {e}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **Why should custom exceptions inherit from `Exception` instead of `BaseException`?**
   - A) `BaseException` is reserved for system-exiting exceptions like `KeyboardInterrupt` and `SystemExit`
   - B) `BaseException` cannot be caught with `try`
   - C) `Exception` is 10x faster
   - D) Python doesn't allow subclassing `BaseException`
   *(Answer: A)*

2. **If class `B(A)` and class `C(B)`, what does `except A:` catch?**
   - A) Only instances of `A`
   - B) Instances of `A`, `B`, and `C`
   - C) Only instances of `C`
   - D) Nothing
   *(Answer: B)*
