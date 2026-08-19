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

## 3. Operator Overloading & Container Dunders

Special "dunder" (double underscore) methods allow custom classes to integrate with native Python operators and built-in functions:

| Dunder Method | Triggered By | Purpose |
| :--- | :--- | :--- |
| `__eq__(self, other)` | `a == b` | Equality comparison |
| `__lt__(self, other)` | `a < b` | Less-than (enables `sorted()`) |
| `__add__(self, other)` | `a + b` | Arithmetic addition |
| `__len__(self)` | `len(obj)` | Number of elements in container |
| `__getitem__(self, key)` | `obj[key]` | Index or key subscript lookup |
| `__contains__(self, item)`| `item in obj` | Membership testing |
| `__bool__(self)` | `bool(obj)`, `if obj:` | Truth value testing |

```python
class SecurityCluster:
    def __init__(self, cluster_id: str):
        self.cluster_id = cluster_id
        self._nodes = []

    def add_node(self, hostname: str) -> None:
        self._nodes.append(hostname)

    def __len__(self) -> int:
        return len(self._nodes)

    def __getitem__(self, index: int) -> str:
        return self._nodes[index]

    def __contains__(self, hostname: str) -> bool:
        return hostname in self._nodes

    def __bool__(self) -> bool:
        # Truthy if at least one node is present
        return len(self._nodes) > 0
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

## 📝 Quick Exercise: Multi-Currency Money & Digital Wallet Container Engine

### 🏢 Real-Life Scenario
You are developing the core financial arithmetic engine for a cross-border fintech payment wallet (such as Wise or Revolut). In fintech software, floating-point rounding errors and currency mismatches cause severe accounting discrepancies. You will implement an encapsulated `Money` class with operator overloading (`+`, `-`, `*`, `==`, `<`) and a container `DigitalWallet` class.

### 📋 Requirements
1. **Define the `Money` Class**:
   - Constructor: `__init__(self, amount: float, currency: str = "USD")`
   - Managed Property `@property` for `amount`: Validates that `amount >= 0.0` (raises `ValueError` on negative values).
   - Representation:
     - `__repr__(self)`: Returns `f"Money({self.amount:.2f}, '{self.currency}')"`.
     - `__str__(self)`: Returns `f"${self.amount:,.2f} {self.currency}"`.
   - Operator Overloading:
     - `__add__(self, other: 'Money') -> 'Money'`: Verifies both objects are `Money` instances and share the same currency. Returns new `Money` object with combined amounts. If currencies differ, raises `ValueError`.
     - `__sub__(self, other: 'Money') -> 'Money'`: Verifies same currency. If `self.amount < other.amount`, raises `ValueError("Insufficient funds for subtraction")`.
     - `__mul__(self, multiplier: float) -> 'Money'`: Multiplies `amount * multiplier` (for interest / exchange scaling).
     - `__eq__(self, other: object) -> bool`: True if currencies and amounts match.
     - `__lt__(self, other: 'Money') -> bool`: Compares amounts when currencies match.
2. **Define the `DigitalWallet` Class**:
   - Constructor: `__init__(self, owner: str)`
   - Container state: `self._balances: dict[str, Money] = {}`
   - Methods:
     - `deposit(self, money: Money) -> None`: Adds `Money` to currency balance.
     - `__len__(self) -> int`: Returns number of distinct currency holdings.
     - `__getitem__(self, currency_code: str) -> Money`: Returns `Money` object for that currency (or `Money(0.0, currency_code)` if not present).
     - `__str__(self)`: Returns formatted summary.
3. Test wallet operations with sample deposits, transactions, and currency arithmetic.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 properties, dunders, operator overloading, and exception handling with Level 1 data types, formatting, and dictionaries.

### 🎯 Expected Output
```text
==================================================
              FINTECH DIGITAL WALLET              
==================================================
Wallet Owner:     Elena Rostova
Distinct Currencies (len): 2 currencies
--------------------------------------------------
USD Balance:      $1,250.00 USD
EUR Balance:      €850.00 EUR
--------------------------------------------------
TRANSACTION ARITHMETIC TESTS:
  ✓ Add Money:     $500.00 USD + $250.00 USD = Money(750.00, 'USD')
  ✓ Multiply (Fee):$750.00 USD * 0.98 = Money(735.00, 'USD')
  ✓ Subtraction:   $750.00 USD - $250.00 USD = Money(500.00, 'USD')
  ✓ Direct Wallet Lookup [USD]: $1,250.00 USD
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Money Domain Value Object (Level 2)
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.currency = currency.upper()
        self.amount = amount # Invokes property setter

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        if value < 0:
            raise ValueError(f"Money amount cannot be negative: {value}")
        self._amount = round(float(value), 2)

    def __repr__(self) -> str:
        return f"Money({self.amount:.2f}, '{self.currency}')"

    def __str__(self) -> str:
        symbol = "€" if self.currency == "EUR" else "$"
        return f"{symbol}{self.amount:,.2f} {self.currency}"

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Operand must be a Money instance")
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: Cannot add {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Operand must be a Money instance")
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: Cannot subtract {self.currency} and {other.currency}")
        if self.amount < other.amount:
            raise ValueError("Insufficient funds for subtraction")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: float) -> 'Money':
        if not isinstance(multiplier, (int, float)):
            raise TypeError("Multiplier must be a numeric value")
        return Money(self.amount * multiplier, self.currency)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return False
        return self.currency == other.currency and self.amount == other.amount

    def __lt__(self, other: 'Money') -> bool:
        if self.currency != other.currency:
            raise ValueError("Cannot compare different currencies")
        return self.amount < other.amount


# 2. Digital Wallet Container (Level 2)
class DigitalWallet:
    def __init__(self, owner: str):
        self.owner = owner
        self._balances: dict[str, Money] = {}

    def deposit(self, money: Money) -> None:
        if money.currency in self._balances:
            self._balances[money.currency] = self._balances[money.currency] + money
        else:
            self._balances[money.currency] = money

    def __len__(self) -> int:
        return len(self._balances)

    def __getitem__(self, currency_code: str) -> Money:
        code = currency_code.upper()
        return self._balances.get(code, Money(0.0, code))


# 3. Execution Simulation
wallet = DigitalWallet("Elena Rostova")
wallet.deposit(Money(1000.00, "USD"))
wallet.deposit(Money(250.00, "USD"))
wallet.deposit(Money(850.00, "EUR"))

m1 = Money(500.00, "USD")
m2 = Money(250.00, "USD")
m_sum = m1 + m2
m_mult = m_sum * 0.98
m_sub = m_sum - m2

print("==================================================")
print("              FINTECH DIGITAL WALLET              ")
print("==================================================")
print(f"Wallet Owner:     {wallet.owner}")
print(f"Distinct Currencies (len): {len(wallet)} currencies")
print("--------------------------------------------------")
print(f"USD Balance:      {wallet['USD']}")
print(f"EUR Balance:      {wallet['EUR']}")
print("--------------------------------------------------")
print("TRANSACTION ARITHMETIC TESTS:")
print(f"  ✓ Add Money:     {m1} + {m2} = {repr(m_sum)}")
print(f"  ✓ Multiply (Fee):{m_sum} * 0.98 = {repr(m_mult)}")
print(f"  ✓ Subtraction:   {m_sum} - {m2} = {repr(m_sub)}")
print(f"  ✓ Direct Wallet Lookup [USD]: {wallet['USD']}")
print("==================================================")
```

**Explanation of the Solution:**
- `Money` implements a robust value object preventing invalid currency operations and rounding errors.
- Operator dunders (`__add__`, `__sub__`, `__mul__`, `__eq__`, `__lt__`) enable natural mathematical syntax between financial amounts.
- `DigitalWallet` utilizes container dunders (`__len__`, `__getitem__`) for clean key-based currency lookups.
</details>
