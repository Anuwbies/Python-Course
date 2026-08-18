# Lesson 8: Modern Type Hinting & Testing with pytest

Writing robust software requires clear type contracts and automated testing. In this lesson, you will master Python's modern typing system (`typing`) and unit testing using industry-standard `pytest`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Annotate functions, classes, and collections using modern Python type hints.
2. Use `Union`, `Optional`, `Callable`, and `Generic` types.
3. Write automated unit tests and assertions using `pytest`.
4. Create reusable test fixtures with `@pytest.fixture`.

---

## 1. Modern Python Type Hinting

Python type hints are not enforced at runtime by default, but they enable static type checkers (`mypy`), IDE autocompletion, and self-documenting code.

```python
from typing import Optional, Callable

# Modern built-in generic collections (Python 3.9+)
def get_user_scores(user_ids: list[str]) -> dict[str, float]:
    return {"user_1": 95.5, "user_2": 88.0}

# Optional (value or None) and Union (one of multiple types)
def find_user_by_id(user_id: int) -> Optional[dict[str, str]]:
    if user_id == 1:
        return {"name": "Alice"}
    return None

# Higher-order function accepting a callback
def transform_values(items: list[int], operation: Callable[[int], int]) -> list[int]:
    return [operation(x) for x in items]
```

---

## 2. Unit Testing with `pytest`

`pytest` makes testing intuitive with plain `assert` statements and powerful fixtures.

### Writing Test Functions:
```python
# calculator.py
def add(a: float, b: float) -> float:
    return a + b

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b
```

```python
# test_calculator.py
import pytest

def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_divide_success():
    assert divide(10, 2) == 5.0

def test_divide_by_zero_raises_error():
    with pytest.raises(ValueError, match="Division by zero"):
        divide(10, 0)
```

---

## 3. Pytest Fixtures

Fixtures provide a clean way to set up test data or database connections before tests run:

```python
import pytest

@pytest.fixture
def sample_user():
    """Provides a fresh user dict for each test."""
    return {"id": 101, "name": "Elena", "role": "admin", "balance": 150.0}

def test_user_has_admin_role(sample_user):
    assert sample_user["role"] == "admin"

def test_user_balance_is_positive(sample_user):
    assert sample_user["balance"] > 0
```

---

## 📝 Quick Exercise

**Prompt**:
1. Write a function `calculate_discount(price: float, percentage: float) -> float`.
2. Ensure it raises a `ValueError` if `percentage < 0` or `percentage > 100`.
3. Write 3 `pytest` test cases: standard discount, 0% discount, and invalid discount raising `ValueError`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import pytest

def calculate_discount(price: float, percentage: float) -> float:
    if not (0 <= percentage <= 100):
        raise ValueError(f"Discount percentage {percentage}% must be between 0 and 100.")
    return price * (1 - percentage / 100)

# Pytest Test Cases:
def test_standard_discount():
    assert calculate_discount(100.0, 20.0) == 80.0

def test_zero_discount():
    assert calculate_discount(50.0, 0.0) == 50.0

def test_invalid_negative_discount():
    with pytest.raises(ValueError):
        calculate_discount(100.0, -10.0)

def test_invalid_over_hundred_discount():
    with pytest.raises(ValueError):
        calculate_discount(100.0, 150.0)
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the difference between `str | None` and `Optional[str]` in Python 3.10+?**
   - A) `str | None` is faster
   - B) They are completely equivalent syntax
   - C) `Optional[str]` allows numbers
   - D) `str | None` is invalid syntax
   *(Answer: B)*

2. **How do you test that a specific exception is raised in `pytest`?**
   - A) `try ... except`
   - B) `with pytest.raises(ExpectedException):`
   - C) `assert raises(ExpectedException)`
   - D) `pytest.expect_error()`
   *(Answer: B)*
