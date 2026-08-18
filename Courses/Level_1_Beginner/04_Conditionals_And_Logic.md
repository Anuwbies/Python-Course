# Lesson 4: Conditional Statements (`if`, `elif`, `else`)

Conditionals allow your software to make decisions, execute branching logic, and handle different scenarios based on dynamic conditions.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand Python's indentation-based code blocks.
2. Construct single and multi-branch decision trees (`if`, `elif`, `else`).
3. Use chained comparison syntax (`18 <= age <= 65`).
4. Perform membership tests using the `in` and `not in` operators.

---

## 1. Python Block Structure & Indentation

Unlike languages that rely on curly braces `{ ... }`, **Python uses strict indentation (4 spaces)** to define code blocks.

```python
score = 88

if score >= 50:
    print("Congratulations!")    # Part of the if block
    print("You passed the exam.") # Part of the if block

print("Execution continues.")    # Outside the if block (always runs)
```

---

## 2. Multi-Way Branching: `if` - `elif` - `else`

- **`if`**: The initial condition evaluated.
- **`elif`** (*short for else-if*): Evaluated only if previous checks evaluated to `False`. You can chain multiple `elif` blocks.
- **`else`**: The fallback block executed if **none** of the previous conditions were met.

```python
score = int(input("Enter exam score (0-100): "))

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is: {grade}")
```

> [!NOTE]
> Python tests conditions top-to-bottom and exits the entire `if-elif-else` structure immediately upon executing the first matching branch.

---

## 3. Chained Comparisons & Nested Conditions

Python features unique and clean chained comparison operators:

```python
age = 25

# Standard approach in other languages:
# if age >= 18 and age <= 64:

# Pythonic chained comparison:
if 18 <= age <= 64:
    print("Working-age adult")
```

### Nested Conditionals:
```python
has_passport = True
is_ticket_valid = False

if has_passport:
    if is_ticket_valid:
        print("Boarding allowed.")
    else:
        print("Invalid ticket: Boarding denied.")
else:
    print("Missing passport: Boarding denied.")
```

---

## 4. The Membership Operator: `in`

You can test whether an item or character exists inside a string, list, or collection using `in`:

```python
email = input("Enter email address: ")

if "@" in email and "." in email:
    print("Email contains required symbols.")
else:
    print("Invalid email format.")
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_4.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Lessons/Lesson_4.py):

```python
user_age = int(input("Enter your age: "))

if user_age < 5:
    price = 0
elif user_age >= 5 and user_age <= 17:
    price = 10
elif user_age >= 18 and user_age <= 64:
    price = 20
elif user_age >= 65:
    price = 12

print(f"Your ticket price is ${price}.")
```

---

## 📝 Quick Exercise

**Prompt**:
Build a simple **Leap Year Checker**:
A year is a leap year if:
1. It is divisible by 4, **AND**
2. It is NOT divisible by 100, **UNLESS** it is also divisible by 400.

*(E.g., 2000 is a leap year, 1900 is not, 2024 is a leap year).*

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
year = int(input("Enter a year: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} is a Leap Year! 🎉")
else:
    print(f"{year} is NOT a leap year.")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is printed by the following code?**
   ```python
   x = 15
   if x < 10:
       print("Small")
   elif x < 20:
       print("Medium")
   elif x < 30:
       print("Large")
   else:
       print("Huge")
   ```
   - A) `Small`
   - B) `Medium`
   - C) `Medium` and `Large`
   - D) `Large`

2. **Which of the following is equivalent to `not (a and b)`?**
   - A) `not a and not b`
   - B) `not a or not b` (De Morgan's Law)
   - C) `a or b`
   - D) `not (a or b)`

3. **What happens if you leave an `if` block empty without code?**
   - A) It runs fine
   - B) It produces an `IndentationError` / `SyntaxError` (unless you use the `pass` keyword)
   - C) It crashes at runtime
   - D) It defaults to `None`

<details>
<summary><b>View Answers</b></summary>
1: B (Exits after the first matching condition)<br>
2: B (De Morgan's Law: not(A and B) == (not A or not B))<br>
3: B (Python requires at least one indented line inside a block; use 'pass' for a placeholder)
</details>
