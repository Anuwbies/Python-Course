# Lesson 1: Printing, Variables & Primitive Data Types

Welcome to your first Python lesson! In computer science, software development begins with data: how we represent information, store it in memory, transform it, and present it clearly to users.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master terminal output using `print()`, including the `sep` and `end` parameters.
2. Understand computer memory variables, reference assignment, and dynamic typing.
3. Distinguish and use the 4 core primitive data types (`int`, `float`, `str`, `bool`).
4. Inspect data types dynamically using the built-in `type()` function.
5. Format numbers and text cleanly using modern **f-strings** with precision and alignment specifiers.
6. Follow standard Python naming conventions (**PEP 8**).

---

## 1. Outputting Data with `print()`

The `print()` function sends formatted text and values to the standard output stream (your terminal or console).

```python
# 1. Printing basic strings:
print("Hello, World!")
print('Single quotes work identically in Python!')

# 2. Printing multiple values (Python automatically separates arguments with a single space):
print("Student:", "Alex Vance", "| ID:", 4092, "| Status: Active")

# 3. Escape Sequences:
# \n -> Newline (moves cursor to next line)
# \t -> Tab (inserts a horizontal tab indent)
# \\ -> Literal backslash
# \" or \' -> Literal quotes inside strings
print("Department:\tEngineering\nLocation:\tBuilding B, Room 304")
print("She said, \"Python is incredibly readable!\"")
```

### Advanced `print()` Arguments: `sep` and `end`
By default, `print()` places a space between items and ends with a newline character (`\n`). You can customize this behavior:

```python
# Custom separator using 'sep':
print("2026", "08", "19", sep="-")          # Output: 2026-08-19
print("home", "user", "docs", sep="/")       # Output: home/user/docs

# Custom line ending using 'end' (suppresses the default newline):
print("Loading data", end="...")
print(" [DONE]")                             # Output: Loading data... [DONE]
```

---

## 2. Variables & The Python Memory Model

A **variable** is a symbolic name that references an object stored in computer memory.

### Static vs. Dynamic Typing
In statically typed languages (like C++, Java, or C#), you must declare the type upfront:
```cpp
// C++ example:
int userAge = 25;
```

In **Python**, typing is **dynamic**. You do not declare types. Python determines the type at runtime based on the object assigned to the variable:

```python
# Assignment syntax: variable_name = value
employee_name = "Sarah Jenkins"  # Python creates a string object in memory
hourly_rate = 42.50              # Python creates a float object in memory
hours_worked = 40                # Python creates an integer object in memory
is_full_time = True              # Python creates a boolean object in memory
```

```
Variable Name           Memory Object
[ employee_name ] ----> "Sarah Jenkins" (str)
[ hourly_rate   ] ----> 42.50           (float)
[ hours_worked  ] ----> 40              (int)
[ is_full_time  ] ----> True            (bool)
```

### Variable Naming Rules & Conventions (PEP 8)
1. **Allowed Characters**: Letters (`a-z`, `A-Z`), digits (`0-9`), and underscores (`_`).
2. **First Character**: Must be a letter or underscore (`_`). **Cannot start with a digit** (e.g., `1st_account` is illegal).
3. **Case-Sensitive**: `total_cost`, `Total_Cost`, and `TOTAL_COST` are three distinct variables.
4. **Reserved Keywords**: You cannot use Python reserved keywords as variable names (e.g., `class`, `for`, `if`, `def`, `return`, `import`, `True`, `False`, `None`).
5. **Python Community Convention (PEP 8)**: Use `snake_case` for all variable and function names (all lowercase words joined by underscores).

```python
# ✅ Good PEP 8 snake_case names:
student_gpa = 3.85
max_retry_attempts = 5
user_email_address = "developer@example.com"

# ❌ Bad / Non-standard names:
# studentGPA = 3.85        (camelCase is discouraged in standard Python)
# 2nd_attempt = 5          (SyntaxError: cannot start with number)
# class = "Computer Sci"   (SyntaxError: 'class' is a reserved keyword)
```

---

## 3. The 4 Fundamental Primitive Data Types

Python classifies data into types. The 4 fundamental primitives are:

| Data Type | Python Class | Description | Real-World Examples |
| :--- | :--- | :--- | :--- |
| **Integer** | `int` | Whole numbers (positive, negative, zero) with arbitrary precision. | `150`, `-45`, `0`, `1000000` |
| **Float** | `float` | Real numbers containing decimal points (IEEE 754 standard). | `19.99`, `-0.005`, `3.14159`, `2.0` |
| **String** | `str` | Ordered sequence of Unicode text characters enclosed in quotes. | `"Seattle"`, `'Order-9821'`, `""` |
| **Boolean** | `bool` | Logical truth values (`True` or `False`). Subtype of integer (`1` or `0`). | `True`, `False` |

### Inspecting Types with `type()`
```python
order_id = 90412
unit_price = 129.95
product_title = "Mechanical Keyboard"
in_stock = True

print(type(order_id))       # <class 'int'>
print(type(unit_price))     # <class 'float'>
print(type(product_title))  # <class 'str'>
print(type(in_stock))       # <class 'bool'>
```

---

## 4. Modern String Formatting (f-strings)

Introduced in Python 3.6, **f-strings** (formatted string literals) provide a concise, readable, and highly efficient way to embed variables and expressions directly inside strings.

Prefix your string literal with `f` or `F`, and place variables or expressions inside curly braces `{}`:

```python
customer = "Marcus Aurelius"
items_ordered = 3
unit_cost = 45.50

# 1. Direct variable interpolation:
print(f"Customer {customer} ordered {items_ordered} items.")

# 2. In-line mathematical expressions:
print(f"Subtotal: ${items_ordered * unit_cost}")

# 3. Formatting floating-point decimal precision (:.2f means 2 decimal places):
raw_tax = 136.50 * 0.0825  # 11.26125
print(f"Tax: ${raw_tax:.2f}")  # Output: Tax: $11.26

# 4. Thousands separator with comma (:,):
annual_revenue = 1582900.5
print(f"Revenue: ${annual_revenue:,.2f}")  # Output: Revenue: $1,582,900.50

# 5. Fixed-width padding and alignment:
# :<15 (left-align in 15 spaces), :>10 (right-align in 10 spaces)
print(f"{'Product':<20} | {'Price':>8}")
print(f"{'Ergonomic Mouse':<20} | {'$49.99':>8}")
print(f"{'USB-C Hub':<20} | {'$19.50':>8}")
```

---

## 5. Common Pitfalls to Avoid

1. **Treating numbers as strings**:
   ```python
   price1 = "50"
   price2 = "20"
   print(price1 + price2)  # Output: "5020" (String concatenation, NOT addition!)
   ```
2. **Accidentally overwriting built-in functions**:
   ```python
   # DO NOT DO THIS:
   # print = "Hello"
   # print("Test")  # ❌ TypeError: 'str' object is not callable
   ```
3. **Mismatched quotes**:
   Always close strings with the same quote type used to open them (`"..."` or `'...'`).

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_01_Variables_And_Data_Types.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_01_Variables_And_Data_Types.py):

```python
course_code = "CS-101"
course_title = "Introduction to Computer Science"
student_count = 128
tuition_per_student = 1450.00
is_active_term = True

gross_tuition = student_count * tuition_per_student

print(f"Course: {course_code} - {course_title}")
print(f"Enrollment: {student_count} students | Active: {is_active_term}")
print(f"Total Tuition Collected: ${gross_tuition:,.2f}")
```

---

## 📝 Quick Exercise: Point of Sale (POS) Retail Receipt Generator

### 🏢 Real-Life Scenario
You are developing the terminal checkout billing module for a modern retail electronics store. When a customer purchases units of a product, the register calculates line item totals, applies a loyalty member discount, adds shipping costs, and prints an itemized customer receipt.

### 📋 Requirements
1. Declare the following variables with appropriate types:
   - `customer_name` $\rightarrow$ `"Eleanor Vance"` (`str`)
   - `item_name` $\rightarrow$ `"Noise-Cancelling Headphones"` (`str`)
   - `unit_price` $\rightarrow$ `149.95` (`float`)
   - `quantity` $\rightarrow$ `2` (`int`)
   - `is_loyalty_member` $\rightarrow$ `True` (`bool`)
   - `member_discount` $\rightarrow$ `25.00` (`float`)
   - `shipping_fee` $\rightarrow$ `8.50` (`float`)
2. Compute:
   - `subtotal`: `unit_price * quantity`
   - `final_total`: `subtotal - member_discount + shipping_fee`
3. Using only **f-strings** and **`print()`**, output an itemized invoice formatted exactly as shown below, with all monetary values formatted to 2 decimal places (`:.2f`).

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lesson 1 (variables, primitive types, basic math operators, f-strings, and `print()`). Do **not** use `input()`, `if` statements, functions, loops, or collections.

### 🎯 Expected Output
```text
==================================================
              APEX ELECTRONICS POS                
==================================================
Customer:       Eleanor Vance
Loyalty Member: True
--------------------------------------------------
Item:           Noise-Cancelling Headphones
Quantity:       2
Unit Price:     $149.95
Subtotal:       $299.90
Member Disc:   -$25.00
Shipping Fee:   $8.50
--------------------------------------------------
FINAL TOTAL:    $283.40
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Customer & Product Variables
customer_name = "Eleanor Vance"
item_name = "Noise-Cancelling Headphones"
unit_price = 149.95
quantity = 2
is_loyalty_member = True
member_discount = 25.00
shipping_fee = 8.50

# 2. Arithmetic Calculations
subtotal = unit_price * quantity
final_total = subtotal - member_discount + shipping_fee

# 3. Formatted POS Receipt Output
print("==================================================")
print("              APEX ELECTRONICS POS                ")
print("==================================================")
print(f"Customer:       {customer_name}")
print(f"Loyalty Member: {is_loyalty_member}")
print("--------------------------------------------------")
print(f"Item:           {item_name}")
print(f"Quantity:       {quantity}")
print(f"Unit Price:     ${unit_price:.2f}")
print(f"Subtotal:       ${subtotal:.2f}")
print(f"Member Disc:   -${member_discount:.2f}")
print(f"Shipping Fee:   ${shipping_fee:.2f}")
print("--------------------------------------------------")
print(f"FINAL TOTAL:    ${final_total:.2f}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **Which of the following is an illegal variable name in Python?**
   - A) `user_total_2`
   - B) `_system_cache`
   - C) `2nd_user_id`
   - D) `totalAccountBalance`

2. **What is the resulting data type of `x = 100 / 4` in Python 3?**
   - A) `int` (`25`)
   - B) `float` (`25.0`)
   - C) `str` (`"25"`)
   - D) `bool` (`True`)

3. **What is the output of `f"{1250000:,.2f}"`?**
   - A) `"1250000.00"`
   - B) `"1,250,000.0"`
   - C) `"1,250,000.00"`
   - D) `SyntaxError`

<details>
<summary><b>View Answers</b></summary>
1: C (Variables cannot start with numeric digits)<br>
2: B (The single '/' true division operator always returns a float in Python)<br>
3: C (The ',.2f' format specifier adds thousands comma separators and rounds to 2 decimal places)
</details>
