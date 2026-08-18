# Lesson 3: Operators & Arithmetic Expressions

Operators are special symbols in Python that carry out arithmetic calculations, comparisons, and logical decision making.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master all 7 arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`).
2. Use floor division (`//`) and modulus (`%`) for real-world algorithms.
3. Understand shorthand augmented assignment operators (`+=`, `-=`, etc.).
4. Combine boolean comparisons with logical operators (`and`, `or`, `not`).

---

## 1. Arithmetic Operators

| Operator | Name | Syntax | Example | Result |
| :--- | :--- | :--- | :--- | :--- |
| `+` | Addition | `a + b` | `10 + 4` | `14` |
| `-` | Subtraction | `a - b` | `10 - 4` | `6` |
| `*` | Multiplication | `a * b` | `10 * 4` | `40` |
| `/` | True Division | `a / b` | `10 / 4` | `2.5` *(Always returns `float`)* |
| `//` | **Floor Division** | `a // b` | `10 // 4` | `2` *(Rounds down to nearest integer)* |
| `%` | **Modulus (Remainder)** | `a % b` | `10 % 4` | `2` *(Remainder after division)* |
| `**` | **Exponentiation (Power)** | `a ** b` | `2 ** 3` | `8` ($2^3$) |

### 💡 Why `//` and `%` are Essential in Computer Science:
1. **Time Breakdown**:
   ```python
   total_seconds = 135
   mins = total_seconds // 60  # 2 minutes
   secs = total_seconds % 60   # 15 seconds
   ```
2. **Even vs Odd Numbers**:
   ```python
   is_even = (number % 2 == 0)
   ```
3. **Digit Extraction**:
   ```python
   num = 457
   last_digit = num % 10  # 7
   ```

---

## 2. Augmented Assignment Operators

Instead of retyping variable names (`x = x + 5`), Python provides concise shorthand:

```python
score = 100
score += 20   # score = score + 20 (now 120)
score -= 15   # score = score - 15 (now 105)
score *= 2    # score = score * 2  (now 210)
score //= 5   # score = score // 5 (now 42)
score %= 10   # score = score % 10 (now 2)
```

---

## 3. Comparison Operators

Comparison operators evaluate expressions and return a boolean: `True` or `False`.

| Operator | Meaning | Example | Result |
| :--- | :--- | :--- | :--- |
| `==` | Equal to | `5 == 5` | `True` |
| `!=` | Not equal to | `5 != 3` | `True` |
| `>` | Greater than | `10 > 5` | `True` |
| `<` | Less than | `3 < 2` | `False` |
| `>=` | Greater than or equal to | `10 >= 10` | `True` |
| `<=` | Less than or equal to | `7 <= 6` | `False` |

> [!CAUTION]
> **Single `=` vs Double `==`**:
> - `=` is an **assignment statement** (`x = 10` assigns `10` to `x`).
> - `==` is an **equality check** (`x == 10` checks if `x` equals `10`).

---

## 4. Logical Operators (`and`, `or`, `not`)

Used to chain multiple conditional expressions together:

* **`and`**: Returns `True` if **all** operands are `True`.
* **`or`**: Returns `True` if **at least one** operand is `True`.
* **`not`**: Inverts truth value (`not True` becomes `False`).

```python
age = 21
has_id = True
has_ticket = False

# Both must be true
can_enter = has_ticket and (age >= 18)  # False

# At least one must be true
is_vip = True
gets_entry = has_ticket or is_vip       # True

# Inverting condition
is_banned = False
allowed = not is_banned                 # True
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_3.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Lessons/Lesson_3.py):

```python
total_seconds = int(input("Enter total seconds: "))
minutes = total_seconds // 60
seconds = total_seconds % 60

print(f"{total_seconds} seconds is {minutes} minutes and {seconds} seconds.")
```

---

## 📝 Quick Exercise

**Prompt**:
Write a program that takes an integer number of cents (e.g. `287`) and determines the change in:
- Quarters ($0.25 = 25¢$)
- Dimes ($0.10 = 10¢$)
- Nickels ($0.05 = 5¢$)
- Pennies ($0.01 = 1¢$)

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
total_cents = int(input("Enter total cents: "))

quarters = total_cents // 25
remaining = total_cents % 25

dimes = remaining // 10
remaining = remaining % 10

nickels = remaining // 5
pennies = remaining % 5

print(f"Change for {total_cents}¢:")
print(f"- Quarters (25¢): {quarters}")
print(f"- Dimes (10¢): {dimes}")
print(f"- Nickels (5¢): {nickels}")
print(f"- Pennies (1¢): {pennies}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the result of `23 // 5` and `23 % 5`?**
   - A) `4.6` and `3`
   - B) `4` and `3`
   - C) `5` and `2`
   - D) `4` and `0.6`

2. **What does `10 / 2` evaluate to in Python?**
   - A) `5` (`int`)
   - B) `5.0` (`float`)
   - C) `5.5`
   - D) `SyntaxError`

3. **What is the result of `True and not (5 > 10 or 3 == 3)`?**
   - A) `True`
   - B) `False`
   - C) `None`
   - D) `Error`

<details>
<summary><b>View Answers</b></summary>
1: B (23 // 5 is 4, 23 % 5 is 3)<br>
2: B (In Python 3, single '/' division always produces a float)<br>
3: B (3 == 3 is True, so the 'or' is True; 'not True' is False; 'True and False' is False)
</details>
