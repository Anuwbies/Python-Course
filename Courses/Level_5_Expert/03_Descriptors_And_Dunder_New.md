# Lesson 3: Object Lifecycle & The Descriptor Protocol: `__new__` and Descriptors

In standard Python programming, you interact with attributes via standard dot notation (`obj.attr = val`). However, in framework engineering (such as Django ORM, Pydantic, or SQLAlchemy), attributes perform invisible validation, type coercion, database mapping, and lazy loading. This entire mechanism is powered by **The Descriptor Protocol** and low-level object allocation via **`__new__`**. In this lesson, you will master custom memory instantiation, Singleton patterns, and data descriptors.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Distinguish between object creation (**`__new__`**) and object initialization (**`__init__`**).
2. Implement strict Singleton and Flyweight patterns using `__new__`.
3. Master the **Descriptor Protocol** (`__get__`, `__set__`, `__delete__`, `__set_name__`).
4. Distinguish between **Data Descriptors** (defining `__set__`) and **Non-Data Descriptors** (defining only `__get__`).
5. Understand CPython's **Attribute Lookup Precedence Order**.
6. Understand how `@property`, `@classmethod`, and `@staticmethod` operate as descriptors internally.

---

## 1. Object Creation vs. Initialization: `__new__` vs. `__init__`

- **`__new__(cls, ...)`**: The static method responsible for allocating the raw memory instance and returning it.
- **`__init__(self, ...)`**: The instance method responsible for populating attributes on the instance returned by `__new__`.

```python
class ThreadSafeSingleton:
    """Guarantees only one physical instance of this class ever exists in RAM."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Allocate memory using superclass object.__new__
            cls._instance = super().__new__(cls)
        return cls._instance

s1 = ThreadSafeSingleton()
s2 = ThreadSafeSingleton()
print(s1 is s2) # True (Identical memory address!)
```

---

## 2. The Descriptor Protocol

A descriptor is any class that implements at least one of `__get__`, `__set__`, or `__delete__`:

```python
class ValidatedPositiveNumber:
    """Data Descriptor enforcing positive numeric values."""

    def __set_name__(self, owner, name):
        # Automatically captures attribute name (e.g. 'price' or 'stock')
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self # Accessed from class level (e.g. Product.price)
        return getattr(instance, self.private_name, 0.0)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError(f"Value must be a positive number: {value}")
        setattr(instance, self.private_name, float(value))
```

---

---

## 4. How Python Methods Bind (`function.__get__`)

In Python, regular functions are **Non-Data Descriptors**! When you call `instance.method()`, Python invokes `Class.method.__get__(instance, Class)`, dynamically returning a bound `types.MethodType` that binds `self` to the instance:

```python
def talk(self): return f"Hello, I am {self.name}"

class Person:
    name = "Elena"
    speak = talk # Non-data descriptor!

p = Person()
# Under the hood:
bound_method = Person.speak.__get__(p, Person)
print(bound_method()) # "Hello, I am Elena"
```

---

## 5. `__slots__` Under the Hood: `member_descriptor`

Declaring `__slots__ = ("x", "y")` suppresses the creation of `instance.__dict__`, allocating fixed C-struct offsets for attributes directly inside the `PyObject` structure:
- Reduces memory consumption by $\approx 60\%$.
- Attribute lookups are powered by C-level `member_descriptor` descriptors.

---

## 6. Flyweight Object Pool Pattern with `__new__`

```python
class ColorFlyweight:
    _pool = {}

    def __new__(cls, r: int, g: int, b: int):
        key = (r, g, b)
        if key not in cls._pool:
            cls._pool[key] = super().__new__(cls)
        return cls._pool[key]
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master `__new__`, descriptors, method binding, `__slots__`, and flyweight allocation:

---

### 🟢 Tier 1: `__new__` Allocation Basics (Exercises 1–3)

#### 🔹 Exercise 1: Custom Instance Allocator
* **Goal**: Override `__new__` to log physical memory allocation before `__init__` executes.

#### 🔹 Exercise 2: Class-Level Singleton
* **Goal**: Implement a Singleton class that returns the same instance across multiple `ClassName()` calls.

#### 🔹 Exercise 3: Immutable Subclassing (Subclassing `tuple` / `int`)
* **Goal**: Subclass immutable `int` using `__new__` to enforce non-negative values.

---

### 🟡 Tier 2: Non-Data & Data Descriptors (Exercises 4–6)

#### 🔹 Exercise 4: Non-Data Descriptor (Cached Property)
* **Goal**: Implement a custom `@lazy_property` descriptor that computes a value once and caches it in `instance.__dict__`.

#### 🔹 Exercise 5: Auto-Naming Descriptor (`__set_name__`)
* **Goal**: Write a descriptor that automatically captures the target property name without hardcoding.

#### 🔹 Exercise 6: Read-Only Data Descriptor
* **Goal**: Implement a descriptor defining `__get__` and a `__set__` that raises `AttributeError("Read-only field")`.

---

### 🟠 Tier 3: Lookup Precedence & Memory Optimization (Exercises 7–9)

#### 🔹 Exercise 7: Attribute Lookup Precedence Shadowing Test
* **Goal**: Demonstrate how a Data Descriptor shadows an instance dict key, while a Non-Data Descriptor is shadowed by an instance dict key.

#### 🔹 Exercise 8: High-Throughput Point Cloud with `__slots__`
* **Goal**: Benchmark memory consumption of 1,000,000 coordinate objects with and without `__slots__`.

#### 🔹 Exercise 9: Flyweight Immutable Particle Pool
* **Goal**: Implement a Flyweight pool using `__new__` sharing 100 particle textures across 100,000 game entities.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Validated Climate Telemetry Descriptor Suite
* **Goal**: Build an enterprise industrial sensor descriptor engine validating temperature and percentage boundary limits across telemetry models.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Type-Safe ORM Field Schema & Singleton Database Configuration Engine**, demonstrating custom `__new__` allocation, descriptor protocols, and automatic attribute name binding:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Performance ORM Model & Descriptor Engine
# =====================================================================

from typing import Any

# 1. Type-Safe Data Descriptor Fields (Lesson 3 Descriptors)
class StringField:
    def __init__(self, max_length: int = 255, nullable: bool = False):
        self.max_length = max_length
        self.nullable = nullable

    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, None)

    def __set__(self, instance: Any, value: Any) -> None:
        if value is None:
            if not self.nullable:
                raise ValueError(f"Field '{self.storage_name[1:]}' cannot be null.")
            setattr(instance, self.storage_name, None)
            return

        if not isinstance(value, str):
            raise TypeError(f"Field '{self.storage_name[1:]}' expects a string, got {type(value).__name__}")

        if len(value) > self.max_length:
            raise ValueError(f"String exceeds maximum length of {self.max_length} characters: '{value}'")

        setattr(instance, self.storage_name, value)


class NumberField:
    def __init__(self, min_value: float = 0.0, max_value: float = float("inf")):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: type, name: str) -> None:
        self.storage_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.storage_name, 0.0)

    def __set__(self, instance: Any, value: Any) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError(f"Field '{self.storage_name[1:]}' expects a numeric value.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Value {value} out of allowable bounds [{self.min_value}, {self.max_value}].")
        setattr(instance, self.storage_name, float(value))


# 2. Domain ORM Model utilizing Descriptors
class ProductCatalogRecord:
    # Class-level descriptors managing instance state
    sku = StringField(max_length=12, nullable=False)
    title = StringField(max_length=80, nullable=False)
    unit_price = NumberField(min_value=0.01, max_value=100_000.0)
    stock_quantity = NumberField(min_value=0, max_value=1_000_000)

    def __init__(self, sku: str, title: str, unit_price: float, stock_quantity: int):
        # Descriptors intercept assignments transparently!
        self.sku = sku
        self.title = title
        self.unit_price = unit_price
        self.stock_quantity = stock_quantity

    def __repr__(self) -> str:
        return f"ProductRecord(sku='{self.sku}', title='{self.title}', price=${self.unit_price:,.2f}, stock={int(self.stock_quantity)})"


# 3. Execution Simulation
print("=" * 80)
print(f"{'CPYTHON DESCRIPTOR PROTOCOL & ORM FIELD SCHEMA SUITE':^80}")
print("=" * 80)

# Valid Record
item = ProductCatalogRecord("SKU-9941", "Mechanical Keyboard RGB", 149.99, 50)
print(f"✅ Successfully instantiated validated record:\n   {item}")

# Modify through descriptor
item.unit_price = 129.95
print(f"  -> Updated price via descriptor: ${item.unit_price:.2f}")

# Test Descriptor Validation Violations
print("\n--- Testing Descriptor Type & Bounds Rejections ---")

try:
    item.unit_price = -25.00 # Violates min_value
except ValueError as val_err:
    print(f"🚨 NumberField Guard: {val_err}")

try:
    item.sku = "VERY_LONG_SKU_CODE_EXCEEDING_TWELVE_CHARS" # Violates max_length
except ValueError as len_err:
    print(f"🚨 StringField Guard: {len_err}")

try:
    item.title = 12345 # Violates type
except TypeError as type_err:
    print(f"🚨 StringField Type Guard: {type_err}")

print("=" * 80)
```

### 🔍 Code Explanation:
- **`__set_name__(self, owner, name)`**: Called automatically when the class is constructed, binding `self.storage_name` to `_sku`, `_title`, etc.
- **`__set__` & `__get__`**: Intercepts read and write operations at the class level, executing type checking and boundary validations transparently.
- **Precedence**: Because `StringField` and `NumberField` implement `__set__`, they act as **Data Descriptors**, overriding any conflicting instance `__dict__` keys.

---

## 📝 Quick Exercise: Validated Temperature & Percentage Descriptor Engine

### 🏢 Real-Life Scenario
You are developing a telemetry data model for an industrial climate control system. Metrics require strict validation:
1. `TemperatureCelsius`: Cannot be below Absolute Zero ($-273.15^\circ\text{C}$) and cannot exceed $1500.0^\circ\text{C}$.
2. `PercentageField`: Must be a float strictly between $0.0\%$ and $100.0\%$.

### 📋 Requirements
1. **Define Descriptor `PercentageField`**:
   - Implements `__set_name__`, `__get__`, and `__set__`.
   - Validates that values are floats/ints between `0.0` and `100.0` (raises `ValueError` on violation).
2. **Define Descriptor `TemperatureField`**:
   - Implements `__set_name__`, `__get__`, and `__set__`.
   - Validates that values are $\ge -273.15$ and $\le 1500.0$.
3. **Define Class `ClimateSensorModel`**:
   - Fields: `humidity = PercentageField()`, `temperature = TemperatureField()`.
   - `__init__(self, temp: float, humidity: float)`.
4. Test valid assignments and test catching invalid boundary violations.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 5 descriptor protocol with Level 2 properties/OOP and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        CLIMATE TELEMETRY DESCRIPTOR SUITE        
==================================================
✅ Valid Sensor Ingest: 23.50°C | Humidity: 65.0%
🚨 Temperature Guard: Temperature -300.00°C is below Absolute Zero (-273.15°C)!
🚨 Humidity Guard: Humidity 115.0% out of allowable range [0.0%, 100.0%]!
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Telemetry Descriptors & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Climate Telemetry Descriptor Suite
# =====================================================================
class PercentageField:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, 0.0)

    def __set__(self, instance, value):
        if not (0.0 <= value <= 100.0):
            raise ValueError(f"Humidity {value}% out of allowable range [0.0%, 100.0%]!")
        setattr(instance, self.name, float(value))


class TemperatureField:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.name, 0.0)

    def __set__(self, instance, value):
        if value < -273.15:
            raise ValueError(f"Temperature {value:.2f}°C is below Absolute Zero (-273.15°C)!")
        if value > 1500.0:
            raise ValueError(f"Temperature {value:.2f}°C exceeds sensor physical limit (1500°C)!")
        setattr(instance, self.name, float(value))


class ClimateSensorModel:
    temperature = TemperatureField()
    humidity = PercentageField()

    def __init__(self, temp: float, humidity: float):
        self.temperature = temp
        self.humidity = humidity


sensor = ClimateSensorModel(23.5, 65.0)
print("==================================================")
print("        CLIMATE TELEMETRY DESCRIPTOR SUITE        ")
print("==================================================")
print(f"✅ Valid Sensor Ingest: {sensor.temperature:.2f}°C | Humidity: {sensor.humidity:.1f}%")

try:
    sensor.temperature = -300.0
except ValueError as err:
    print(f"🚨 Temperature Guard: {err}")

try:
    sensor.humidity = 115.0
except ValueError as err:
    print(f"🚨 Humidity Guard: {err}")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Custom __new__
class MemoryLogger:
    def __new__(cls, *a, **kw):
        inst = super().__new__(cls)
        return inst

# Ex 2: Singleton
class AppConfig:
    _inst = None
    def __new__(cls):
        if cls._inst is None: cls._inst = super().__new__(cls)
        return cls._inst

# Ex 3: Subclass int
class PositiveInt(int):
    def __new__(cls, val):
        if val < 0: raise ValueError("Must be positive")
        return super().__new__(cls, val)

# Ex 4: Lazy Property
class LazyProp:
    def __init__(self, fn): self.fn = fn
    def __get__(self, inst, owner):
        if inst is None: return self
        v = self.fn(inst)
        inst.__dict__[self.fn.__name__] = v
        return v

# Ex 5: __set_name__
class AutoName:
    def __set_name__(self, owner, name): self.name = name

# Ex 6: Read-Only Descriptor
class ReadOnly:
    def __set__(self, inst, val): raise AttributeError("Read-only")

# Ex 7: Lookup Precedence
# Data Descriptor (__set__) > Instance __dict__ > Non-Data (__get__ only)

# Ex 8: __slots__
class FastPoint:
    __slots__ = ("x", "y")
    def __init__(self, x, y): self.x, self.y = x, y

# Ex 9: Flyweight Pool
class Particle:
    _pool = {}
    def __new__(cls, tex):
        if tex not in cls._pool: cls._pool[tex] = super().__new__(cls)
        return cls._pool[tex]
```
</details>
