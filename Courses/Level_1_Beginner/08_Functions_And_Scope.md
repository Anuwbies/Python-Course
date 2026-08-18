# Lesson 8: Functions & Scope

Functions are reusable, named blocks of code that perform a specific task. They are the backbone of modular programming and code reuse.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Define custom functions using `def` and call them.
2. Pass positional, keyword, and default arguments.
3. Understand `return` values vs simply printing to console.
4. Understand Local vs Global variable scope.
5. Use variable positional arguments (`*args`) and keyword arguments (`**kwargs`).

---

## 1. Defining & Calling Functions

```python
# Function Definition
def greet_user(name):
    """Docstring: Prints a friendly greeting to the user."""
    print(f"Hello, {name}! Welcome aboard.")

# Calling the Function
greet_user("Alex")
greet_user("Samantha")
```

---

## 2. Returning Values (`return`)

A function should typically process inputs and **return** a result back to the caller rather than just printing it:

```python
def calculate_cylinder_volume(radius, height):
    pi = 3.14159265
    volume = pi * (radius ** 2) * height
    return volume

# Receiving and using the returned value:
tank_volume = calculate_cylinder_volume(3.5, 10.0)
print(f"Total Tank Volume: {tank_volume:.2f} cubic meters.")
```

> [!NOTE]
> If a function has no `return` statement, it automatically returns `None`.

---

## 3. Default & Keyword Arguments

```python
# 'discount' has a default parameter value of 0.0
def calculate_bill(subtotal, tax_rate=0.08, discount=0.0):
    total = (subtotal - discount) * (1 + tax_rate)
    return total

# Calling with default parameters:
bill1 = calculate_bill(100.0) # Uses tax 0.08, discount 0.0

# Calling with explicit keyword arguments:
bill2 = calculate_bill(100.0, discount=15.0)
bill3 = calculate_bill(tax_rate=0.10, subtotal=200.0)
```

---

## 4. Variable Scope (Local vs Global)

- **Local Scope**: Variables created inside a function exist **only** inside that function.
- **Global Scope**: Variables defined at the top-level script are accessible everywhere, but modifying them inside a function requires care.

```python
app_version = "1.0.0" # Global variable

def process_data():
    local_counter = 42 # Local variable
    print(f"Running on version {app_version}")
    print(f"Counter: {local_counter}")

process_data()
# print(local_counter) # ❌ NameError: name 'local_counter' is not defined
```

---

## 5. Flexible Arguments: `*args` and `**kwargs`

- **`*args`**: Collects arbitrary positional arguments as a **tuple**.
- **`**kwargs`**: Collects arbitrary keyword arguments as a **dictionary**.

```python
def sum_all(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

print(sum_all(1, 2, 3, 4, 5)) # 15

def print_profile(**user_data):
    for key, value in user_data.items():
        print(f"{key}: {value}")

print_profile(name="Jordan", role="Engineer", location="Seattle")
```

---

## 📝 Quick Exercise

**Prompt**:
Write a function `is_prime(n)`:
1. Returns `False` if $n \le 1$.
2. Uses a `for` loop to check if any number from $2$ up to $\sqrt{n}$ evenly divides $n$.
3. Returns `True` if it is a prime number, else `False`.
4. Test it on numbers `2`, `7`, `10`, `29`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import math

def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    # Check divisors up to square root of n:
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Test cases:
for test in [2, 7, 10, 29, 1, 0, 49]:
    print(f"is_prime({test}) -> {is_prime(test)}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is returned by a function that has no `return` statement?**
   - A) `0`
   - B) `False`
   - C) `None`
   - D) `""`

2. **Can default parameters appear BEFORE non-default parameters in a function definition?**
   - A) Yes, parameter order doesn't matter
   - B) No, default parameters must always follow non-default parameters (`SyntaxError`)
   - C) Only in Python 3.12+
   - D) Yes, if specified with type hints

3. **Inside a function, how is `*args` represented?**
   - A) As a `list`
   - B) As a `tuple`
   - C) As a `dict`
   - D) As a `set`

<details>
<summary><b>View Answers</b></summary>
1: C (Functions default to returning None)<br>
2: B (Non-default arguments cannot follow default arguments)<br>
3: B (*args captures positional arguments as an immutable tuple)
</details>
