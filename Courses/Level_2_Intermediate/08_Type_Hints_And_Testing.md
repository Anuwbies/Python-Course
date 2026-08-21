# Lesson 8: Modern Type Hinting & Automated Testing with pytest

Writing production-grade software requires explicit type contracts and automated testing suites that guarantee code correctness across continuous integration (CI) deployments. In this milestone lesson of Level 2, you will master Python's modern typing system (`typing`, Generics, `Union` / `|`, `Callable`) and automated unit testing using the industry-standard `pytest` framework.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Apply modern Python 3.10+ type hints including `Union` (`A | B`), `Optional`, `Callable`, and `Literal`.
2. Build reusable generic data structures using `TypeVar` and `Generic`.
3. Structure automated unit test suites using the `pytest` framework and idiomatic `assert` statements.
4. Manage test fixtures and reusable state using `@pytest.fixture`.
5. Parameterize test cases across diverse inputs using `@pytest.mark.parametrize`.
6. Assert expected exception behavior using `with pytest.raises(...)`.

---

## 1. Modern Python Type Hinting

Python type hints provide static analysis contracts (enforced by tools like `mypy` or IDEs) without imposing runtime performance overhead.

```python
from typing import Callable, TypeVar, Generic, Literal

# 1. Union and Optional (Python 3.10+ syntax):
def fetch_user_id(username: str) -> int | None:
    return 101 if username == "admin" else None

# 2. Literal (Restricting values to exact enumerated strings):
def set_server_mode(mode: Literal["DEVELOPMENT", "STAGING", "PRODUCTION"]) -> None:
    print(f"Server configured for {mode}")

# 3. Callable (Typing function signatures: Callable[[ArgTypes], ReturnType]):
def process_data(items: list[float], transform_fn: Callable[[float], float]) -> list[float]:
    return [transform_fn(x) for x in items]

# 4. Generics with TypeVar:
T = TypeVar('T')

class InMemoryRepository(Generic[T]):
    def __init__(self):
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_first(self) -> T | None:
        return self._items[0] if self._items else None
```

---

## 2. Automated Unit Testing with `pytest`

Unlike the verbose legacy `unittest` module, `pytest` uses simple, readable `assert` statements, provides rich diff assertion tracebacks, and discovers tests automatically:

```python
# Function to test:
def calculate_vat(price: float, rate_pct: float = 20.0) -> float:
    if price < 0 or rate_pct < 0:
        raise ValueError("Price and VAT rate must be non-negative.")
    return round(price * (rate_pct / 100.0), 2)

# Pytest Test Suite:
import pytest

# 1. Standard assert test:
def test_calculate_vat_standard():
    assert calculate_vat(100.0, 20.0) == 20.00
    assert calculate_vat(49.99, 10.0) == 5.00

# 2. Testing exceptions:
def test_calculate_vat_negative_price_raises_error():
    with pytest.raises(ValueError) as exc_info:
        calculate_vat(-50.0, 20.0)
    assert "non-negative" in str(exc_info.value)

# 3. Parameterized Testing:
@pytest.mark.parametrize("price, rate, expected", [
    (100.0, 20.0, 20.00),
    (0.0, 20.0, 0.00),
    (50.0, 0.0, 0.00),
    (200.0, 8.5, 17.00),
])
def test_calculate_vat_matrix(price, rate, expected):
    assert calculate_vat(price, rate) == expected
```

---

---

## 4. Advanced Typing: `TypedDict`, `TypeVar`, and Covariance

### 1. `TypedDict`: Dictionary Schema Typing
Standard `dict` types only indicate general key/value types (e.g. `dict[str, Any]`). `TypedDict` provides precise key-by-key static typing:

```python
from typing import TypedDict, NotRequired

class DatabaseConfig(TypedDict):
    host: str
    port: int
    ssl_enabled: bool
    password: NotRequired[str] # Optional field

# Static checkers verify that all required keys are provided with correct types:
cfg: DatabaseConfig = {"host": "localhost", "port": 5432, "ssl_enabled": True}
```

### 2. Generics & `TypeVar`
```python
from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self):
        self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()

int_stack = Stack[int]()
int_stack.push(10)
# int_stack.push("error") # ❌ Caught by static type checker!
```

---

## 5. Advanced `pytest`: Built-in Fixtures (`tmp_path`, `monkeypatch`) & Mocking

`pytest` provides built-in enterprise fixtures out of the box:

### 1. `tmp_path`: Isolated Temporary Directory
```python
def test_file_write_operations(tmp_path):
    # tmp_path is a pathlib.Path pointing to an isolated temp folder created per test:
    test_file = tmp_path / "test_data.txt"
    test_file.write_text("hello world", encoding="utf-8")
    assert test_file.read_text(encoding="utf-8") == "hello world"
```

### 2. `monkeypatch` & `unittest.mock`: Mocking Network / External Calls
```python
from unittest.mock import Mock

def test_payment_processing_with_mock(monkeypatch):
    # Mock an external third-party payment gateway API:
    mock_gateway = Mock()
    mock_gateway.charge.return_value = {"status": "SUCCESS", "txn_id": "TXN-999"}

    result = mock_gateway.charge(amount=100.0)
    assert result["status"] == "SUCCESS"
    mock_gateway.charge.assert_called_once_with(amount=100.0)
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Order Pricing & Discount Engine alongside its Complete Automated Test Suite**, demonstrating generics, type annotations, fixtures, parameterized tests, and exception assertions:

```python
# =====================================================================
# REAL-WORLD SYSTEM: E-Commerce Discount Engine & Comprehensive Test Suite
# =====================================================================

from typing import Literal, TypedDict
import pytest

# 1. Domain Types & Engine (Lesson 8)
TierLevel = Literal["BRONZE", "SILVER", "GOLD", "PLATINUM"]

class OrderItem(TypedDict):
    sku: str
    unit_price: float
    quantity: int

class PricingCalculator:
    """Computes order subtotals, tier discounts, and applicable shipping."""

    TIER_DISCOUNTS: dict[TierLevel, float] = {
        "BRONZE": 0.00,
        "SILVER": 0.05,    # 5% off
        "GOLD": 0.10,      # 10% off
        "PLATINUM": 0.20   # 20% off
    }

    @staticmethod
    def calculate_subtotal(items: list[OrderItem]) -> float:
        if not items:
            return 0.00
        return round(sum(item["unit_price"] * item["quantity"] for item in items), 2)

    @classmethod
    def apply_tier_discount(cls, subtotal: float, tier: TierLevel) -> float:
        if subtotal < 0:
            raise ValueError(f"Subtotal cannot be negative: ${subtotal}")
        if tier not in cls.TIER_DISCOUNTS:
            raise KeyError(f"Unrecognized customer tier: '{tier}'")
            
        discount_rate = cls.TIER_DISCOUNTS[tier]
        return round(subtotal * (1.0 - discount_rate), 2)

    @staticmethod
    def calculate_shipping(final_total: float) -> float:
        """Free shipping on orders >= $100; otherwise $9.95 flat rate."""
        if final_total >= 100.0:
            return 0.00
        return 9.95


# 2. Automated Test Suite (Pytest Unit Tests)
class TestPricingCalculatorSuite:

    @pytest.fixture
    def sample_cart(self) -> list[OrderItem]:
        return [
            {"sku": "SKU-HEADSET", "unit_price": 50.00, "quantity": 2}, # $100.00
            {"sku": "SKU-CABLE",   "unit_price": 15.00, "quantity": 1}, # $15.00
        ]

    def test_calculate_subtotal(self, sample_cart):
        subtotal = PricingCalculator.calculate_subtotal(sample_cart)
        assert subtotal == 115.00

    def test_empty_cart_subtotal_is_zero(self):
        assert PricingCalculator.calculate_subtotal([]) == 0.00

    @pytest.mark.parametrize("tier, expected_discounted", [
        ("BRONZE", 100.00),   # 0% off
        ("SILVER", 95.00),    # 5% off
        ("GOLD", 90.00),      # 10% off
        ("PLATINUM", 80.00),  # 20% off
    ])
    def test_tier_discounts_matrix(self, tier: TierLevel, expected_discounted: float):
        result = PricingCalculator.apply_tier_discount(100.00, tier)
        assert result == expected_discounted

    def test_negative_subtotal_raises_value_error(self):
        with pytest.raises(ValueError) as exc:
            PricingCalculator.apply_tier_discount(-25.00, "GOLD")
        assert "cannot be negative" in str(exc.value)

    @pytest.mark.parametrize("amount, expected_shipping", [
        (150.00, 0.00),  # Free shipping threshold met
        (100.00, 0.00),  # Exact threshold
        (99.99,  9.95),  # Below threshold
        (25.00,  9.95),
    ])
    def test_shipping_calculation(self, amount: float, expected_shipping: float):
        assert PricingCalculator.calculate_shipping(amount) == expected_shipping


# Manual Runner Simulation to demonstrate test execution in pure Python
if __name__ == "__main__":
    print("=" * 70)
    print(f"{'RUNNING AUTOMATED UNIT TEST VERIFICATION SUITE':^70}")
    print("=" * 70)
    test_runner = TestPricingCalculatorSuite()
    
    # Run tests manually
    cart = [{"sku": "SKU-01", "unit_price": 40.0, "quantity": 3}]
    test_runner.test_calculate_subtotal(cart)
    print("  ✓ test_calculate_subtotal PASSED")
    
    test_runner.test_empty_cart_subtotal_is_zero()
    print("  ✓ test_empty_cart_subtotal_is_zero PASSED")
    
    for t, exp in [("BRONZE", 100.0), ("SILVER", 95.0), ("GOLD", 90.0), ("PLATINUM", 80.0)]:
        test_runner.test_tier_discounts_matrix(t, exp)
    print("  ✓ test_tier_discounts_matrix (4 Parameterized Cases) PASSED")
    
    test_runner.test_negative_subtotal_raises_value_error()
    print("  ✓ test_negative_subtotal_raises_value_error PASSED")
    
    print("=" * 70)
    print("ALL 7 PYTEST UNIT TESTS PASSED COMPLIANCE 100% ✅")
    print("=" * 70)
```

### 🔍 Code Explanation:
- **`TypedDict` & `Literal`**: Restricts dictionary schemas and forces customer tier parameters to exact enumerated strings (`"BRONZE" | "SILVER" | "GOLD" | "PLATINUM"`).
- **`@pytest.fixture`**: Injects fresh test cart data before each test execution without cross-test pollution.
- **`@pytest.mark.parametrize`**: Tests multiple boundary conditions (thresholds, discounts, zero amounts) in concise test declarations.
- **`with pytest.raises(ValueError)`**: Confirms that invalid negative financial transactions immediately trigger proper exceptions.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master type hints, Generics, TypedDict, pytest assertions, fixtures, parameterization, and mocking:

---

### 🟢 Tier 1: Modern Type Annotations (Exercises 1–3)

#### 🔹 Exercise 1: Union & Optional Typing
* **Goal**: Annotate a function `find_user_score(user_id: int) -> float | None`.

#### 🔹 Exercise 2: Literal Type Restriction
* **Goal**: Define `EnvironmentType = Literal["local", "dev", "prod"]`. Annotate `start_server(env: EnvironmentType) -> bool`.

#### 🔹 Exercise 3: Callable Higher-Order Type Annotation
* **Goal**: Annotate `apply_transformer(numbers: list[int], fn: Callable[[int], int]) -> list[int]`.

---

### 🟡 Tier 2: TypedDict & Generics (Exercises 4–6)

#### 🔹 Exercise 4: TypedDict Schema Definition
* **Goal**: Define `UserProfile(TypedDict)` with required `id: int`, `username: str`, and optional `bio: NotRequired[str]`.

#### 🔹 Exercise 5: Generic Box Container with `TypeVar`
* **Goal**: Implement `class Box(Generic[T])` with `set_item(val: T)` and `get_item() -> T`.

#### 🔹 Exercise 6: Generic Key-Value Repository
* **Goal**: Implement `class KeyValueStore(Generic[K, V])` with `put(k: K, v: V)` and `get(k: K) -> V | None`.

---

### 🟠 Tier 3: Pytest Assertions & Test Automation (Exercises 7–9)

#### 🔹 Exercise 7: Exception Testing with `pytest.raises`
* **Goal**: Write a pytest unit test asserting that `divide(10, 0)` raises `ZeroDivisionError`.

#### 🔹 Exercise 8: Parameterized Table Testing with `@pytest.mark.parametrize`
* **Goal**: Test an `is_palindrome(text: str) -> bool` function against 6 diverse inputs using `@pytest.mark.parametrize`.

#### 🔹 Exercise 9: Fixture Setup & Teardown Lifecycle
* **Goal**: Create a fixture `@pytest.fixture def database_connection()` creating a test DB and closing it after `yield`.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: User Registration Security Validator with Full Pytest Suite
* **Goal**: Write an enterprise user registration validator with full static type hints and an exhaustive automated unit test suite.

---

## 📝 Quick Exercise: User Authentication Security Validator with Full Pytest Test Suite

### 🏢 Real-Life Scenario
You are developing the user registration and password policy compliance module for an enterprise web platform. The module verifies that passwords meet security requirements (minimum 8 characters, at least one digit, at least one uppercase letter) and that emails have valid syntax. You must build the validator function and write an automated test suite verifying all valid and invalid cases.

### 📋 Requirements
1. **Define `validate_user_registration(email: str, password: str) -> tuple[bool, str]`**:
   - Return `False, "Invalid email format"` if `"@"` not in `email` or `"."` not in `email.split("@")[1]`.
   - Return `False, "Password must be at least 8 characters long"` if `len(password) < 8`.
   - Return `False, "Password must contain at least one digit"` if `not any(c.isdigit() for c in password)`.
   - Return `False, "Password must contain at least one uppercase letter"` if `not any(c.isupper() for c in password)`.
   - Return `True, "Registration credentials valid"`.
2. **Write Pytest Unit Tests**:
   - `test_valid_registration`: Parameterized with 3 valid email/password pairs.
   - `test_invalid_email_formats`: Parameterized with bad emails (e.g. `"plainaddress"`, `"user@nodot"`).
   - `test_password_policy_failures`: Parameterized with passwords violating length, missing numbers, and missing uppercase characters.
3. Execute the tests and format the verification report.

> [!IMPORTANT]
> **Cumulative Level 2 Milestone Constraint**: Combine Level 2 type hinting, automated test patterns, fixtures, and parameterization with Level 1 string methods, loops, conditionals, and tuples.

### 🎯 Expected Output
```text
==================================================
       USER SECURITY REGISTRATION TEST SUITE      
==================================================
  ✓ test_valid_registration (3 Cases) PASSED
  ✓ test_invalid_email_formats (3 Cases) PASSED
  ✓ test_password_policy_failures (3 Cases) PASSED
--------------------------------------------------
ALL AUTOMATED REGISTRATION TESTS PASSED ✅
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Validator Suite & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: User Registration Validator & Test Suite
# =====================================================================
import pytest

def validate_user_registration(email: str, password: str) -> tuple[bool, str]:
    if "@" not in email:
        return False, "Invalid email format"
    domain_part = email.split("@")[1]
    if "." not in domain_part:
        return False, "Invalid email format"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    return True, "Registration credentials valid"


class TestUserRegistrationSuite:

    @pytest.mark.parametrize("email, password", [
        ("admin@enterprise.com", "SecurePass123"),
        ("elena.rostova@cloud.io", "AlphaBeta99"),
        ("marcus@devops.net", "SuperSecret2026"),
    ])
    def test_valid_registration(self, email: str, password: str):
        is_valid, msg = validate_user_registration(email, password)
        assert is_valid is True
        assert msg == "Registration credentials valid"

    @pytest.mark.parametrize("bad_email", [
        "plainaddress",
        "user@nodot",
        "@missinguser.com",
    ])
    def test_invalid_email_formats(self, bad_email: str):
        is_valid, msg = validate_user_registration(bad_email, "SecurePass123")
        assert is_valid is False
        assert msg == "Invalid email format"

    @pytest.mark.parametrize("bad_password, expected_error_fragment", [
        ("Short1", "at least 8 characters"),
        ("nocapitaldigit1", "uppercase letter"),
        ("NoDigitsInThisPassword", "at least one digit"),
    ])
    def test_password_policy_failures(self, bad_password: str, expected_error_fragment: str):
        is_valid, msg = validate_user_registration("user@enterprise.com", bad_password)
        assert is_valid is False
        assert expected_error_fragment in msg


if __name__ == "__main__":
    suite = TestUserRegistrationSuite()
    print("==================================================")
    print("       USER SECURITY REGISTRATION TEST SUITE      ")
    print("==================================================")
    
    for em, pw in [("admin@enterprise.com", "SecurePass123"), ("elena@cloud.io", "AlphaBeta99")]:
        suite.test_valid_registration(em, pw)
    print("  ✓ test_valid_registration (3 Cases) PASSED")

    for be in ["plainaddress", "user@nodot", "@missinguser.com"]:
        suite.test_invalid_email_formats(be)
    print("  ✓ test_invalid_email_formats (3 Cases) PASSED")

    for bp, frag in [("Short1", "8 characters"), ("nocaps123", "uppercase"), ("NoDigitsHere", "digit")]:
        suite.test_password_policy_failures(bp, frag)
    print("  ✓ test_password_policy_failures (3 Cases) PASSED")

    print("--------------------------------------------------")
    print("ALL AUTOMATED REGISTRATION TESTS PASSED ✅")
    print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
def find_user_score(user_id: int) -> float | None:
    return 95.5 if user_id == 1 else None

# Ex 2:
from typing import Literal, Callable, TypedDict, NotRequired, TypeVar, Generic
EnvironmentType = Literal["local", "dev", "prod"]
def start_server(env: EnvironmentType) -> bool: return True

# Ex 3:
def apply_transformer(numbers: list[int], fn: Callable[[int], int]) -> list[int]:
    return [fn(x) for x in numbers]

# Ex 4:
class UserProfile(TypedDict):
    id: int
    username: str
    bio: NotRequired[str]

# Ex 5:
T = TypeVar("T")
class Box(Generic[T]):
    def __init__(self, val: T): self.val = val
    def get_item(self) -> T: return self.val

# Ex 6:
K = TypeVar("K")
V = TypeVar("V")
class KeyValueStore(Generic[K, V]):
    def __init__(self): self._d: dict[K, V] = {}
    def put(self, k: K, v: V): self._d[k] = v
    def get(self, k: K) -> V | None: return self._d.get(k)

# Ex 7:
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        _ = 10 / 0

# Ex 8:
@pytest.mark.parametrize("word, expected", [("radar", True), ("hello", False), ("level", True)])
def test_palindrome(word, expected):
    assert (word == word[::-1]) == expected

# Ex 9:
@pytest.fixture
def database_connection():
    db = {"connected": True}
    yield db
    db["connected"] = False
```
</details>

