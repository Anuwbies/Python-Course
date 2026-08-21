# Lesson 2: Encapsulation, Properties & Magic Dunder Methods

Python favors explicit, readable code over rigid privacy modifiers like `private` or `protected` in other languages. In this lesson, you will master Pythonic data modeling, managed attributes via `@property`, and essential magic (dunder) methods that enable operator overloading and custom collection behaviors.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Apply Python naming conventions for privacy (`_protected` internal signals vs `__private` name mangling).
2. Validate and compute attributes dynamically using `@property`, `@setter`, and `@deleter`.
3. Distinguish and implement representation dunders: `__repr__` (developer debug representation) vs `__str__` (end-user display).
4. Overload arithmetic and comparison operators using `__add__`, `__sub__`, `__eq__`, `__lt__`, and `__bool__`.
5. Implement container protocols with `__len__`, `__getitem__`, and `__contains__`.

---

## 1. Encapsulation & Managed Attributes with `@property`

Instead of verbose Java-style getters and setters (`get_temperature()` / `set_temperature()`), Python uses the `@property` decorator to present attributes as standard public variables while executing underlying validation and calculations:

```python
class TemperatureSensor:
    def __init__(self, celsius: float = 0.0):
        # Setting via property setter to trigger validation on initialization
        self.celsius = float(celsius)

    @property
    def celsius(self) -> float:
        """Getter for celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Setter with validation: Physical Absolute Zero check."""
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C is physically impossible (below Absolute Zero -273.15°C)!")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        """Dynamically computed property (Read-Only)."""
        return (self._celsius * 9.0 / 5.0) + 32.0

# Usage:
sensor = TemperatureSensor(25.0)
print(f"Celsius: {sensor.celsius}°C | Fahrenheit: {sensor.fahrenheit}°F")

sensor.celsius = 100.0 # Invokes @celsius.setter transparently!
# sensor.celsius = -300.0 # ❌ Raises ValueError: physically impossible
```

---

## 2. Representation Dunders: `__repr__` vs `__str__`

- **`__str__`**: Human-readable, friendly string designed for end-users (`print()`, `str()`).
- **`__repr__`**: Unambiguous, technical representation for developers and logs, ideally matching valid Python instantiation syntax (`eval(repr(obj)) == obj`).

```python
class GeographicCoordinate:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self) -> str:
        # Developer syntax string
        return f"GeographicCoordinate(latitude={self.latitude}, longitude={self.longitude})"

    def __str__(self) -> str:
        # User-friendly coordinate string
        lat_dir = "N" if self.latitude >= 0 else "S"
        lon_dir = "E" if self.longitude >= 0 else "W"
        return f"{abs(self.latitude):.4f}°{lat_dir}, {abs(self.longitude):.4f}°{lon_dir}"

coord = GeographicCoordinate(37.7749, -122.4194)
print(str(coord))  # "37.7749°N, 122.4194°W"
print(repr(coord)) # "GeographicCoordinate(latitude=37.7749, longitude=-122.4194)"
```

---

---

## 4. Under the Hood: The Descriptor Protocol

Have you ever wondered how `@property` works internally? It is built on Python's **Descriptor Protocol**. A descriptor is an object attribute with "binding behavior" whose attribute access is overridden by methods in the descriptor protocol:
- `__get__(self, instance, owner=None)`
- `__set__(self, instance, value)`
- `__delete__(self, instance)`

When you access `obj.attribute`, if `attribute` defines `__get__`, Python executes that descriptor method instead of a standard dictionary lookup in `obj.__dict__`.

```python
class NonNegativeFloat:
    """Reusable descriptor enforcing positive float constraints across any class."""
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, 0.0)

    def __set__(self, instance, value):
        if float(value) < 0.0:
            raise ValueError(f"Value cannot be negative: {value}")
        setattr(instance, self.private_name, float(value))

class ServerSpec:
    cpu_ghz = NonNegativeFloat()
    ram_gb = NonNegativeFloat()

    def __init__(self, cpu: float, ram: float):
        self.cpu_ghz = cpu # Triggers NonNegativeFloat.__set__
        self.ram_gb = ram
```

---

## 5. Comparison Simplification with `@functools.total_ordering`

Implementing all 6 comparison dunders (`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) is tedious. By decorating your class with `@total_ordering`, you only need to implement **`__eq__`** and **ONE of (`__lt__`, `__le__`, `__gt__`, `__ge__`)**—Python generates the rest automatically:

```python
from functools import total_ordering

@total_ordering
class TaskPriority:
    def __init__(self, level: int, label: str):
        self.level = level
        self.label = label

    def __eq__(self, other):
        return isinstance(other, TaskPriority) and self.level == other.level

    def __lt__(self, other):
        return isinstance(other, TaskPriority) and self.level < other.level

# Automatically supports <=, >, >=, !=, and sorted()!
p1 = TaskPriority(1, "Low")
p2 = TaskPriority(5, "Critical")
print(p1 <= p2) # True
```

---

## 6. Callable Objects (`__call__`)

Implementing `__call__` allows an instance of a class to be invoked directly like a function while maintaining state across invocations:

```python
class RateLimiter:
    def __init__(self, max_requests: int):
        self.max_requests = max_requests
        self.count = 0

    def __call__(self, client_ip: str) -> bool:
        self.count += 1
        return self.count <= self.max_requests

limiter = RateLimiter(max_requests=2)
print(limiter("192.168.1.1")) # True (Request 1)
print(limiter("192.168.1.1")) # True (Request 2)
print(limiter("192.168.1.1")) # False (Exceeded!)
```

---

## 💻 Code Example & Reference

The following real-life program models an **Institutional Equity Investment Portfolio & Asset Vector Engine**, demonstrating `@property`, mathematical operator overloading, sequence dunders, and custom string representations:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Institutional Equity Portfolio & Asset Engine
# =====================================================================

class AssetHolding:
    """Represents a specific stock position in a financial portfolio."""

    def __init__(self, ticker: str, shares: float, cost_basis_per_share: float):
        self.ticker = ticker.upper()
        self.shares = shares
        self.cost_basis = cost_basis_per_share
        self._current_market_price = cost_basis_per_share

    @property
    def shares(self) -> float:
        return self._shares

    @shares.setter
    def shares(self, value: float) -> None:
        if value < 0:
            raise ValueError(f"Share count cannot be negative: {value}")
        self._shares = float(value)

    @property
    def current_market_price(self) -> float:
        return self._current_market_price

    @current_market_price.setter
    def current_market_price(self, price: float) -> None:
        if price <= 0:
            raise ValueError(f"Market price must be positive: ${price}")
        self._current_market_price = float(price)

    @property
    def total_market_value(self) -> float:
        return self._shares * self._current_market_price

    @property
    def unrealized_pnl(self) -> float:
        return (self._current_market_price - self.cost_basis) * self._shares

    def __repr__(self) -> str:
        return f"AssetHolding(ticker='{self.ticker}', shares={self.shares}, cost_basis={self.cost_basis})"

    def __str__(self) -> str:
        sign = "+" if self.unrealized_pnl >= 0 else ""
        return f"{self.ticker:<6} | {self.shares:>8.2f} shs | Value: ${self.total_market_value:>10,.2f} | PnL: {sign}${self.unrealized_pnl:>9,.2f}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AssetHolding):
            return False
        return self.ticker == other.ticker

    def __lt__(self, other: 'AssetHolding') -> bool:
        # Allows sorting holdings by market valuation
        return self.total_market_value < other.total_market_value


class InvestmentPortfolio:
    """Container managing multiple asset holdings with custom container dunders."""

    def __init__(self, portfolio_name: str, cash_balance: float = 10_000.0):
        self.portfolio_name = portfolio_name
        self.cash_balance = cash_balance
        self._holdings: list[AssetHolding] = []

    def add_position(self, holding: AssetHolding) -> None:
        if holding in self:
            # Overloaded 'in' calls __contains__
            existing = self[holding.ticker]
            existing.shares += holding.shares
        else:
            self._holdings.append(holding)

    @property
    def total_nav(self) -> float:
        """Net Asset Value = Cash + All Equity Market Values."""
        return self.cash_balance + sum(h.total_market_value for h in self._holdings)

    # Container Protocol Dunders
    def __len__(self) -> int:
        return len(self._holdings)

    def __getitem__(self, key: any) -> AssetHolding:
        if isinstance(key, int):
            return self._holdings[key]
        if isinstance(key, str):
            for h in self._holdings:
                if h.ticker == key.upper():
                    return h
            raise KeyError(f"Ticker '{key}' not found in portfolio holdings.")
        raise TypeError("Index must be integer position or string ticker symbol.")

    def __contains__(self, item: any) -> bool:
        if isinstance(item, str):
            return any(h.ticker == item.upper() for h in self._holdings)
        if isinstance(item, AssetHolding):
            return item in self._holdings
        return False

    def __repr__(self) -> str:
        return f"InvestmentPortfolio(name='{self.portfolio_name}', positions={len(self)}, NAV=${self.total_nav:,.2f})"


# Execution Simulation
portfolio = InvestmentPortfolio("Apex Alpha Quantitative Fund", cash_balance=25_000.00)

h1 = AssetHolding("AAPL", 50.0, 150.00)
h1.current_market_price = 185.50 # Update price (invoking @setter)

h2 = AssetHolding("NVDA", 30.0, 420.00)
h2.current_market_price = 875.00

h3 = AssetHolding("MSFT", 40.0, 310.00)
h3.current_market_price = 425.00

portfolio.add_position(h1)
portfolio.add_position(h2)
portfolio.add_position(h3)

print("=" * 70)
print(f"{repr(portfolio):^70}")
print("=" * 70)
print(f"{'Position Count (len):':<30} {len(portfolio)} distinct equities")
print(f"{'Direct Key Lookup [NVDA]:':<30} {portfolio['NVDA']}")
print(f"{'Membership Check (TSLA in ptfl):':<30} {'TSLA' in portfolio}")
print("-" * 70)
print("PORTFOLIO ASSET RANKING (Sorted by Value via __lt__):")
for pos in sorted(portfolio._holdings, reverse=True):
    print(f"  {pos}")
print("-" * 70)
print(f"{'TOTAL NET ASSET VALUE (NAV):':<30} ${portfolio.total_nav:,.2f}")
print("=" * 70)
```
### 🔍 Code Explanation:
- **`@property` and `@setter`**: Protects share volume and stock price from invalid zero or negative inputs, while exposing clean attribute access (`h1.current_market_price = 185.50`).
- **`__len__` & `__getitem__`**: Enables `len(portfolio)` to return the asset count and `portfolio["NVDA"]` or `portfolio[0]` to fetch positions intuitively.
- **`__contains__`**: Enables natural `in` syntax (`"TSLA" in portfolio` or `h1 in portfolio`).
- **`__lt__` & `__repr__`**: Overloading `<` enables `sorted(portfolio._holdings)` to order assets automatically by total market valuation.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master properties, representation dunders, operator overloading, container protocols, descriptors, and callable objects:

### 🟢 Tier 1: Property Getters, Setters & Dunders (Exercises 1–3)
* **Exercise 1: Validated Bank Balance Property**: Class `Account` with `@property balance`. Setter raises `ValueError` if new balance is negative.
* **Exercise 2: Developer vs User Dunder Representations**: Class `ServerNode(ip: str, port: int)`. Implement `__str__` returning `"<ip>:<port>"` and `__repr__` returning `"ServerNode(ip='...', port=...)"`.
* **Exercise 3: Dynamic Read-Only Area Property**: Class `Circle` with mutable `radius`. Create read-only `@property area` calculating $\pi r^2$.

### 🟡 Tier 2: Operator Overloading & Total Ordering (Exercises 4–6)
* **Exercise 4: 2D Vector Addition & Scalar Multiplication**: Class `Vector2D(x, y)`. Implement `__add__(self, other)` and `__mul__(self, scalar)` returning a new `Vector2D`.
* **Exercise 5: Total Ordering Severity Level**: Class `Severity(level: int)`. Use `@total_ordering` with `__eq__` and `__lt__`. Test `<, <=, >, >=`.
* **Exercise 6: Equality & Value Object Hashing**: Class `UserID(code: str)`. Implement `__eq__` and `__hash__` so instances can be used as keys in a `dict` and elements in a `set`.

### 🟠 Tier 3: Container Protocols & Descriptors (Exercises 7–9)
* **Exercise 7: Custom Sequence Container (`__len__`, `__getitem__`)**: Class `Playlist`. Implement `__len__`, `__getitem__` (supporting integer index and slices), and `__contains__`.
* **Exercise 8: Reusable Non-Empty String Descriptor**: Create descriptor `NonEmptyString`. Apply it to `Employee.first_name` and `Employee.last_name` to reject empty strings.
* **Exercise 9: Stateful Callable Token Bucket Rate Limiter (`__call__`)**: Class `TokenBucket(capacity: int, refill_rate: float)`. Implement `__call__() -> bool` that consumes a token if available.

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)
* **Exercise 10: Multi-Currency Financial Value Object & Digital Wallet**: Implement `Money` value object with arithmetic operator overloading and currency mismatch safety, wrapped inside a `DigitalWallet` container dunder class.

---

## 📝 Quick Exercise: Multi-Currency Value Object & Digital Wallet System

### 🏢 Real-Life Scenario
You are developing a financial ledger engine for a global multi-currency fintech application (such as Stripe or Revolut). The engine must represent monetary values securely as immutable value objects, enforce strict mathematical rules (e.g. preventing adding USD to EUR without conversion), overload operators for natural syntax, and store balances across currencies inside a custom container `DigitalWallet`.

### 📋 Requirements
1. **Define the `Money` Class**:
   - Constructor: `__init__(self, amount: float, currency: str = "USD")`
   - Properties: `@property amount` with `@amount.setter`: Rejects negative amounts and rounds to 2 decimal places.
   - Magic Dunder Methods: `__repr__`, `__str__`, `__add__`, `__sub__`, `__mul__`, `__eq__`, `__lt__`.
2. **Define the `DigitalWallet` Class**:
   - Constructor: `__init__(self, owner: str)`
   - Methods: `deposit`, `__len__`, `__getitem__`, `__str__`.

<details>
<summary><b>🔍 View Exercise Solutions (Digital Wallet & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Digital Wallet Engine
# =====================================================================
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.currency = currency.upper()
        self.amount = amount

    @property
    def amount(self) -> float:
        return self._amount
    
    @amount.setter
    def amount(self, value: float):
        if value < 0: raise ValueError("Negative amount")
        self._amount = round(float(value), 2)

    def __repr__(self) -> str: return f"Money({self.amount:.2f}, '{self.currency}')"
    def __str__(self) -> str: return f"${self.amount:,.2f} {self.currency}"

    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency: raise ValueError("Mismatch")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency: raise ValueError("Mismatch")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, m: float) -> 'Money': return Money(self.amount * m, self.currency)
    def __eq__(self, o) -> bool: return self.currency == o.currency and self.amount == o.amount
    def __lt__(self, o) -> bool: 
        if self.currency != o.currency: raise ValueError("Mismatch")
        return self.amount < o.amount

class DigitalWallet:
    def __init__(self, owner: str):
        self.owner = owner
        self._balances: dict[str, Money] = {}

    def deposit(self, money: Money):
        if money.currency in self._balances: self._balances[money.currency] += money
        else: self._balances[money.currency] = money

    def __len__(self): return len(self._balances)
    def __getitem__(self, currency_code: str):
        return self._balances.get(currency_code.upper(), Money(0.0, currency_code))

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
class Account:
    def __init__(self, b: float): self.balance = b
    @property
    def balance(self): return self._b
    @balance.setter
    def balance(self, v):
        if v < 0: raise ValueError("Negative balance disallowed")
        self._b = v

# Ex 2:
class ServerNode:
    def __init__(self, ip: str, port: int): self.ip, self.port = ip, port
    def __str__(self): return f"{self.ip}:{self.port}"
    def __repr__(self): return f"ServerNode(ip='{self.ip}', port={self.port})"

# Ex 3:
import math
class Circle:
    def __init__(self, r: float): self.radius = r
    @property
    def area(self): return math.pi * (self.radius ** 2)

# Ex 4:
class Vector2D:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, o): return Vector2D(self.x + o.x, self.y + o.y)
    def __mul__(self, s): return Vector2D(self.x * s, self.y * s)
    def __repr__(self): return f"Vector2D({self.x}, {self.y})"

# Ex 5:
from functools import total_ordering
@total_ordering
class Severity:
    def __init__(self, lvl: int): self.lvl = lvl
    def __eq__(self, o): return self.lvl == o.lvl
    def __lt__(self, o): return self.lvl < o.lvl

# Ex 6:
class UserID:
    def __init__(self, code: str): self.code = code
    def __eq__(self, o): return isinstance(o, UserID) and self.code == o.code
    def __hash__(self): return hash(self.code)

# Ex 7:
class Playlist:
    def __init__(self, songs): self._songs = list(songs)
    def __len__(self): return len(self._songs)
    def __getitem__(self, idx): return self._songs[idx]
    def __contains__(self, s): return s in self._songs

# Ex 8:
class NonEmptyString:
    def __set_name__(self, owner, name): self.name = f"_{name}"
    def __get__(self, inst, owner): return getattr(inst, self.name, "")
    def __set__(self, inst, val):
        if not val or not isinstance(val, str): raise ValueError("Must be non-empty string")
        setattr(inst, self.name, val)

# Ex 9:
class TokenBucket:
    def __init__(self, cap: int): self.cap = cap
    def __call__(self):
        if self.cap > 0:
            self.cap -= 1
            return True
        return False
```
</details>
