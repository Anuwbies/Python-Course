# Lesson 2: User Input & Type Casting

In this lesson, you will learn how to make programs interactive by receiving input from a user and how to convert (cast) that data into numbers and other types.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Capture user input using the `input()` function.
2. Understand why `input()` always returns a string (`str`).
3. Safely cast strings into `int`, `float`, and `bool`.
4. Clean user inputs using string methods like `.strip()` and `.lower()`.

---

## 1. The `input()` Function

The `input()` function prompts the user to enter text in the terminal and pauses execution until the user presses <kbd>Enter</kbd>.

```python
user_name = input("Enter your username: ")
print(f"Welcome, {user_name}!")
```

> [!IMPORTANT]
> **The Golden Rule of `input()`**:
> `input()` **ALWAYS returns a string (`str`)**, even if the user types numeric digits like `42` or `99.9`.

```python
age = input("Enter your age: ")
print(type(age))  # <class 'str'>

# If you try this:
# next_age = age + 1  # ❌ TypeError: can only concatenate str to str, not int
```

---

## 2. Type Casting (Conversion)

To perform mathematical calculations on user inputs, you must convert (cast) the string to an integer or float.

### Standard Casting Functions:
- `int(value)`: Converts to whole integer.
- `float(value)`: Converts to decimal number.
- `str(value)`: Converts any data type to string.
- `bool(value)`: Converts to boolean.

```python
# Converting input directly to integer:
age = int(input("Enter your age: "))
next_year = age + 1
print(f"Next year you will be {next_year} years old.")

# Converting to float for prices or measurements:
price = float(input("Enter product price: $"))
tax_rate = 0.08
total = price * (1 + tax_rate)
print(f"Total with tax: ${total:.2f}")
```

---

## 3. Sanitizing User Input (`.strip()`, `.lower()`)

User input is often messy (extra spaces, uppercase/lowercase variations). Python provides useful string helper methods:

```python
raw_input = "   Yes   "
clean_input = raw_input.strip()       # "Yes" (removes surrounding whitespace)
lower_input = clean_input.lower()     # "yes" (converts to lowercase)

# Chained together in one line:
answer = input("Continue? (yes/no): ").strip().lower()
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_2.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Lessons/Lesson_2.py):

```python
name = input("Enter your name: ")
age = int(input("Enter your age: "))
had_birthday = input("Have you had your birthday this year? (yes/no): ").strip().lower()
birth_year = 2026 - age

if had_birthday == "no":
    birth_year -= 1
    print(f"Hello {name}! You were born in {birth_year}.")
elif had_birthday == "yes":
    print(f"Hello {name}! You were born in {birth_year}.")
else:
    print("Invalid input for birthday. Please enter 'yes' or 'no'.")
```

---

## 📝 Quick Exercise

**Prompt**:
1. Ask the user for their height in centimeters (`float`).
2. Ask for their weight in kilograms (`float`).
3. Calculate their Body Mass Index: $\text{BMI} = \frac{\text{weight}}{(\text{height} / 100)^2}$.
4. Print: `"Your calculated BMI is: 22.45"` (formatted to 2 decimal places).

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
height_cm = float(input("Enter your height in cm: "))
weight_kg = float(input("Enter your weight in kg: "))

height_m = height_cm / 100
bmi = weight_kg / (height_m ** 2)

print(f"Your calculated BMI is: {bmi:.2f}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What happens if a user inputs `"twenty"` and your code executes `int(input())`?**
   - A) It defaults to `0`
   - B) It crashes with a `ValueError`
   - C) It converts it to `20`
   - D) It converts it to `None`

2. **What does `bool("")` (an empty string) evaluate to?**
   - A) `True`
   - B) `False`
   - C) `None`
   - D) `SyntaxError`

3. **If `val = "  Python  "`, what is the value of `val.strip()`?**
   - A) `"Python"`
   - B) `"  Python  "`
   - C) `"python"`
   - D) `None`

<details>
<summary><b>View Answers</b></summary>
1: B (Strings containing non-digits throw a ValueError when passed to int())<br>
2: B (In Python, empty strings, 0, and empty collections are "falsy")<br>
3: A (strip() removes leading and trailing whitespace)
</details>
