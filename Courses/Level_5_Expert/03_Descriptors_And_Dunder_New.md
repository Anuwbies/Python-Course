# Lesson 3: Advanced Metaprogramming: Descriptors & __new__

Descriptors are the low-level mechanism powering Python's `@property`, `@classmethod`, `@staticmethod`, and ORM model field definitions.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master the Descriptor Protocol (`__get__`, `__set__`, `__delete__`, `__set_name__`).
2. Differentiate between Data Descriptors and Non-Data Descriptors.
3. Understand the exact difference between instance allocation `__new__` and initialization `__init__`.
4. Implement a Single-Instance Singleton pattern via `__new__`.

---

## 1. Building a Type-Validating Data Descriptor

```python
class TypedField:
    """Descriptor that validates types on attribute assignment."""
    def __init__(self, expected_type):
        self.expected_type = expected_type
        self.name = None

    def __set_name__(self, owner, name):
        # Automatically captures attribute name (e.g. 'age')
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"Attribute '{self.name}' must be of type {self.expected_type.__name__}, got {type(value).__name__}")
        instance.__dict__[self.name] = value

class UserProfile:
    # Declarative descriptors
    name = TypedField(str)
    age = TypedField(int)

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# Usage:
u = UserProfile("Elena", 28)
# u.age = "twenty-eight" # ❌ Raises TypeError: Attribute 'age' must be of type int, got str
```

---

## 2. Overriding Object Allocation with `__new__` (Singleton Pattern)

```python
class DatabaseConnectionManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Allocate the one and only instance
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

## 📝 Quick Exercise

**Prompt**:
Create a `BoundedNumber` descriptor that enforces both type validation and a range limit (`min_val <= val <= max_val`).

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
class BoundedNumber:
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"'{self.name}' must be a number")
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(f"'{self.name}' ({value}) must be between {self.min_val} and {self.max_val}")
        instance.__dict__[self.name] = value

class GamePlayer:
    health = BoundedNumber(0, 100)

    def __init__(self, health: int):
        self.health = health

player = GamePlayer(75)
# player.health = 150 # ❌ Raises ValueError: 'health' (150) must be between 0 and 100
```
</details>
