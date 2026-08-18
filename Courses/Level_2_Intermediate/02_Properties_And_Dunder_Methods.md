# Lesson 2: Encapsulation, Properties & Magic Dunder Methods

Python favors explicit, readable code over rigid privacy modifiers like `private` or `protected` in other languages. In this lesson, you will master Pythonic data modeling, managed attributes via `@property`, and essential magic (dunder) methods.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand Python's naming conventions for privacy (`_protected` and `__private`).
2. Use `@property` and `@setter` to validate and compute attributes cleanly.
3. Master representation dunders: `__repr__` vs `__str__`.
4. Overload operators and container behaviors using `__eq__`, `__len__`, and `__getitem__`.

---

## 1. Encapsulation & Managed Attributes with `@property`

Instead of clumsy Java-style `get_age()` and `set_age()`, Python uses the `@property` decorator to make getters and setters look like standard attribute access while maintaining strict validation.

```python
class Temperature:
    def __init__(self, celsius: float = 0.0):
        self._celsius = float(celsius) # Leading underscore signals 'internal/protected'

    @property
    def celsius(self) -> float:
        """Getter for celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Setter with validation: Absolute zero check."""
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C is below Absolute Zero (-273.15°C)!")
        self._celsius = float(value)

    @property
    def fahrenheit(self) -> float:
        """Computed property: converts C to F dynamically."""
        return (self._celsius * 9 / 5) + 32

# Usage:
temp = Temperature(25.0)
print(f"Celsius: {temp.celsius}°C | Fahrenheit: {temp.fahrenheit}°F")

temp.celsius = 100.0 # Invokes @celsius.setter automatically!
# temp.celsius = -300 # ❌ Raises ValueError: below Absolute Zero
```

---

## 2. Representation Dunders: `__str__` vs `__repr__`

* **`__str__`**: Designed for the end-user (clean, human-readable).
* **`__repr__`**: Designed for developers and debugging (unambiguous, matches code syntax).

```python
class Point2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Point2D(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

p = Point2D(3, 4)
print(str(p))   # (3, 4)
print(repr(p))  # Point2D(x=3, y=4)
```

---

## 3. Operator Overloading & Container Dunders

You can make your custom objects support native operators like `+`, `==`, `len()`, and indexing `[ ]`:

```python
class ShoppingCart:
    def __init__(self, owner: str):
        self.owner = owner
        self.items: list[dict] = []

    def add_item(self, name: str, price: float) -> None:
        self.items.append({"name": name, "price": price})

    # len(cart)
    def __len__(self) -> int:
        return len(self.items)

    # cart[0]
    def __getitem__(self, index: int) -> dict:
        return self.items[index]

    # cart1 == cart2
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ShoppingCart):
            return False
        return sum(item["price"] for item in self.items) == sum(item["price"] for item in other.items)

cart = ShoppingCart("Alex")
cart.add_item("Keyboard", 80.0)
cart.add_item("Mouse", 40.0)

print(f"Total items in cart: {len(cart)}") # Calls __len__ -> 2
print(f"First item: {cart[0]['name']}")      # Calls __getitem__ -> Keyboard
```

---

## 📝 Quick Exercise

**Prompt**:
Create a `Money` class:
1. Attributes: `amount` (float), `currency` (str, e.g. `"USD"`).
2. Validate with `@property` that `amount >= 0`.
3. Implement `__add__` so that `Money(10, "USD") + Money(25, "USD")` returns `Money(35, "USD")`. Raise a `ValueError` if currencies don't match.
4. Implement `__repr__` returning `f"Money({self.amount}, '{self.currency}')"`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.currency = currency.upper()
        self.amount = amount # Calls property setter

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        if value < 0:
            raise ValueError("Money amount cannot be negative!")
        self._amount = float(value)

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            raise TypeError("Can only add Money to another Money object")
        if self.currency != other.currency:
            raise ValueError(f"Cannot add different currencies: {self.currency} and {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self) -> str:
        return f"Money({self.amount:.2f}, '{self.currency}')"

m1 = Money(50.0, "USD")
m2 = Money(25.50, "USD")
m3 = m1 + m2
print(repr(m3)) # Money(75.50, 'USD')
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the convention for indicating an attribute is internal/private in Python?**
   - A) Prefixing with `private ` keyword
   - B) A single leading underscore `_attr` or double `__attr`
   - C) Capitalizing the attribute name
   - D) Adding `.private` at the end
   *(Answer: B)*

2. **Which magic method enables the `+` addition operator on instances of your class?**
   - A) `__plus__`
   - B) `__add__`
   - C) `__sum__`
   - D) `__concat__`
   *(Answer: B)*

3. **If a class defines `__repr__` but NOT `__str__`, what happens when you call `print(obj)`?**
   - A) It raises an `AttributeError`
   - B) Python falls back to using `__repr__`
   - C) It outputs an empty string
   - D) It crashes the interpreter
   *(Answer: B)*
