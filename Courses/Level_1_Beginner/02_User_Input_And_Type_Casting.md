# Lesson 2: User Input & Type Casting

In Lesson 1, all program values were hardcoded literals. In this lesson, you will learn how to make software interactive by accepting dynamic user input from the console and converting (type casting) that input into numbers and booleans for data processing.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Capture keyboard input from the terminal using the `input()` function.
2. Master the **Golden Rule of `input()`**: why it always returns a `str` (string).
3. Safely cast raw strings into `int`, `float`, `str`, and `bool`.
4. Understand **Truthiness and Falsiness** when casting values to `bool`.
5. Sanitize and clean user text using string methods: `.strip()`, `.lower()`, `.upper()`, and `.title()`.
6. Anticipate and prevent runtime `ValueError` crashes caused by invalid type conversions.

---

## 1. The `input()` Function & Terminal I/O

The `input()` function pauses execution of your Python program, prints an optional prompt message to the terminal, and waits for the user to type text and press the <kbd>Enter</kbd> key.

```python
# The string inside input(...) is the prompt displayed to the user:
user_name = input("Please enter your name: ")
print(f"Welcome to the system, {user_name}!")
```

### ⚠️ The Golden Rule of `input()`
> [!IMPORTANT]
> **`input()` ALWAYS returns a string (`str`)**, regardless of what characters the user types.

Even if the user enters numeric digits like `42` or `9.99`, Python stores it as string text (`"42"` or `"9.99"`).

```python
user_age = input("Enter your age: ")
print(type(user_age))  # Output: <class 'str'>

# If you attempt arithmetic directly on a string:
# next_age = user_age + 1  # ❌ TypeError: can only concatenate str (not "int") to str

# If you attempt multiplication on a string:
# print(user_age * 2)     # If user typed 20, output is "2020" (string repetition!), NOT 40!
```

---

## 2. Explicit Type Casting (Type Conversion)

To perform mathematical calculations on numbers entered by users, you must convert the string into a numeric data type using Python's built-in type casting functions.

### The 4 Core Casting Functions:
1. **`int(value)`**: Converts a string or float into a whole integer.
2. **`float(value)`**: Converts a string or integer into a decimal floating-point number.
3. **`str(value)`**: Converts any data type into its string representation.
4. **`bool(value)`**: Converts a value into a boolean (`True` or `False`).

```python
# 1. Converting input to an integer:
raw_age = input("Enter your age: ")
age = int(raw_age)
print(f"In 5 years, you will be {age + 5} years old.")

# 2. Converting directly in a single line (Standard Idiom):
hourly_rate = float(input("Enter hourly wage ($): "))
hours_worked = float(input("Enter hours worked this week: "))
gross_pay = hourly_rate * hours_worked
print(f"Gross Pay: ${gross_pay:,.2f}")
```

### Type Conversion Rules & Edge Cases:

```
Source Data        Target Type      Resulting Value
---------------------------------------------------
"45"          -->  int("45")   -->  45 (int)
"19.95"       -->  float("19.95") -> 19.95 (float)
45            -->  float(45)   -->  45.0 (float)
19.95         -->  int(19.95)  -->  19 (int - truncates decimal!)
100           -->  str(100)    -->  "100" (str)
```

> [!CAUTION]
> **Conversion Gotchas**:
> - `int("3.14")` raises a `ValueError`! Python cannot parse a decimal point directly inside an integer string. You must do `int(float("3.14"))` if you want to truncate `3.14` to `3`.
> - `int("twenty")` raises a `ValueError` because alphabetic words cannot be parsed into numbers.

---

## 3. Truthiness & Boolean Casting: `bool()`

When casting values to `bool()`, Python follows strict rules regarding what is considered **Truthy** or **Falsy**:

### Falsy Values (evaluate to `False`):
- Empty string: `bool("")` $\rightarrow$ `False`
- Numeric zero: `bool(0)`, `bool(0.0)` $\rightarrow$ `False`
- `None` object: `bool(None)` $\rightarrow$ `False`

### Truthy Values (evaluate to `True`):
- Any non-empty string: `bool("Hello")` $\rightarrow$ `True`
- Any non-zero number: `bool(42)`, `bool(-5)`, `bool(0.001)` $\rightarrow$ `True`

> [!WARNING]
> **The Boolean String Trap**:
> `bool("False")` evaluates to **`True`** because `"False"` is a non-empty string of 5 characters! Only `bool("")` evaluates to `False`.

---

## 4. Sanitizing User Input with String Methods

Users frequently enter text with accidental leading/trailing spaces or inconsistent letter casing. Before casting or storing input, sanitize it using string helper methods:

| Method | Description | Example Input | Result |
| :--- | :--- | :--- | :--- |
| `.strip()` | Removes leading and trailing whitespace. | `"  Alice  ".strip()` | `"Alice"` |
| `.lower()` | Converts all characters to lowercase. | `"YES".lower()` | `"yes"` |
| `.upper()` | Converts all characters to uppercase. | `"usd".upper()` | `"USD"` |
| `.title()` | Capitalizes the first letter of each word. | `"san francisco".title()` | `"San Francisco"` |

```python
# Chaining sanitization methods directly onto input():
city_name = input("Enter your city: ").strip().title()
country_code = input("Enter 3-letter country code: ").strip().upper()

print(f"Destination: {city_name}, {country_code}")
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_02_User_Input_And_Type_Casting.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_02_User_Input_And_Type_Casting.py):

```python
# Unit Converter: Gallons to Liters
GALLONS_TO_LITERS = 3.78541

user_name = input("Enter operator name: ").strip().title()
gallons_input = float(input("Enter volume in Gallons: "))

liters_calculated = gallons_input * GALLONS_TO_LITERS

print(f"Operator: {user_name}")
print(f"Volume:   {gallons_input:.2f} gal = {liters_calculated:.2f} L")
```

---

## 📝 Quick Exercise: Freelance Billing & Invoice Calculator

### 🏢 Real-Life Scenario
You are building an automated invoicing utility for freelance software consultants. The program prompts the consultant for client details, hourly billing rate, billable project hours, and any software/cloud infrastructure expenses incurred. It then calculates the labor subtotal, total invoice amount, estimated income tax withholding, and expected net earnings.

### 📋 Requirements
1. Prompt for and sanitize the following inputs:
   - `client_name`: Prompt with `"Enter client business name: "` and format with `.strip().title()`.
   - `project_title`: Prompt with `"Enter project title: "` and format with `.strip()`.
2. Prompt and cast numerical inputs:
   - `hourly_rate`: Prompt with `"Enter hourly billing rate ($): "` and cast to `float`.
   - `hours_worked`: Prompt with `"Enter total billable hours: "` and cast to `float`.
   - `expenses`: Prompt with `"Enter cloud/hardware expenses incurred ($): "` and cast to `float`.
3. Perform the following financial calculations:
   - `labor_cost = hourly_rate * hours_worked`
   - `invoice_total = labor_cost + expenses`
   - `tax_withholding = invoice_total * 0.22` (estimated 22% tax reserve)
   - `net_earnings = invoice_total - tax_withholding`
4. Using **f-strings**, output a clean, formatted billing summary with all monetary amounts formatted to 2 decimal places (`:.2f`).

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 and 2 (variables, primitives, `input()`, `int()`, `float()`, `str()`, string sanitization methods, arithmetic, f-strings, and `print()`). Do **not** use `if` statements, loops, functions, or collections.

### 🎯 Sample Interactive Run
```text
Enter client business name:    quantum leap technologies   
Enter project title: Cloud API Migration
Enter hourly billing rate ($): 85.00
Enter total billable hours: 32.5
Enter cloud/hardware expenses incurred ($): 120.50

==================================================
           FREELANCE INVOICE SUMMARY              
==================================================
Client:        Quantum Leap Technologies
Project:       Cloud API Migration
--------------------------------------------------
Hours Logged:  32.50 hrs @ $85.00/hr
Labor Cost:    $2,762.50
Expenses:      $120.50
--------------------------------------------------
INVOICE TOTAL: $2,883.00
Est. Tax (22%):$634.26
NET EARNINGS:  $2,248.74
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Capture and sanitize text inputs
client_name = input("Enter client business name: ").strip().title()
project_title = input("Enter project title: ").strip()

# 2. Capture and cast numeric inputs
hourly_rate = float(input("Enter hourly billing rate ($): "))
hours_worked = float(input("Enter total billable hours: "))
expenses = float(input("Enter cloud/hardware expenses incurred ($): "))

# 3. Perform calculations
labor_cost = hourly_rate * hours_worked
invoice_total = labor_cost + expenses
tax_withholding = invoice_total * 0.22
net_earnings = invoice_total - tax_withholding

# 4. Formatted invoice display
print("\n==================================================")
print("           FREELANCE INVOICE SUMMARY              ")
print("==================================================")
print(f"Client:        {client_name}")
print(f"Project:       {project_title}")
print("--------------------------------------------------")
print(f"Hours Logged:  {hours_worked:.2f} hrs @ ${hourly_rate:.2f}/hr")
print(f"Labor Cost:    ${labor_cost:,.2f}")
print(f"Expenses:      ${expenses:,.2f}")
print("--------------------------------------------------")
print(f"INVOICE TOTAL: ${invoice_total:,.2f}")
print(f"Est. Tax (22%):${tax_withholding:,.2f}")
print(f"NET EARNINGS:  ${net_earnings:,.2f}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the return type of the expression `input("Enter number: ")` if the user types `99`?**
   - A) `int`
   - B) `float`
   - C) `str`
   - D) `None`

2. **What is the result of `bool("   ")` (a string containing spaces)?**
   - A) `False`
   - B) `True`
   - C) `ValueError`
   - D) `None`

3. **Which statement correctly cleans a user's input of extra whitespace and capitalizes the first letter of each word?**
   - A) `input().clean().capitalize()`
   - B) `input().strip().title()`
   - C) `input().lower().trim()`
   - D) `str(input()).remove_spaces()`

<details>
<summary><b>View Answers</b></summary>
1: C (input() unconditionally returns a str)<br>
2: B (Any string with length > 0 is truthy; only empty string "" is falsy)<br>
3: B (.strip() removes surrounding whitespace and .title() capitalizes each word)
</details>
