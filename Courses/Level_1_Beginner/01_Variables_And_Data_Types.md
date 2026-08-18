# Lesson 1: Printing, Variables & Primitive Data Types

Welcome to your first Python lesson! In computer science, everything starts with data and how we display, store, and manipulate it.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand how to output information to the terminal using `print()`.
2. Know the 4 fundamental primitive data types in Python.
3. Understand variable assignment and Python's dynamic typing.
4. Format strings cleanly using modern **f-strings**.

---

## 1. Outputting Data with `print()`

The `print()` function takes text, numbers, or variables and prints them to the standard output (your console/terminal).

```python
# Printing simple strings:
print("Hello, World!")
print('Single quotes work just fine too!')

# Printing multiple items separated by commas (Python automatically inserts a space):
print("My name is", "Alex", "and I am", 19, "years old.")

# Escape sequences:
print("Line 1\nLine 2")    # \n creates a newline
print("Column 1\tColumn 2") # \t inserts a tab
```

---

## 2. Variables & Dynamic Typing

A **variable** is a named location in memory that stores a value.

Unlike static languages (such as C++, Java, or C#) where you must declare the type (`int x = 5;`), **Python is dynamically typed**: Python infers the type of variable at runtime based on what value you assign to it.

```python
# Variable assignment: name = value
user_name = "Jordan"   # Python knows this is a str (string)
score = 95             # Python knows this is an int (integer)
```

### Variable Naming Rules & Conventions:
- Must start with a letter (`a-z`, `A-Z`) or an underscore (`_`).
- Cannot start with a number (e.g. `2nd_user` is **invalid**).
- Can only contain alphanumeric characters and underscores (`a-z`, `A-Z`, `0-9`, `_`).
- Case-sensitive: `Age`, `age`, and `AGE` are 3 distinct variables.
- **Python Convention**: Use `snake_case` for variable names (all lowercase with underscores between words).

---

## 3. The 4 Fundamental Primitive Data Types

| Type | Type Name | Description | Examples |
| :--- | :--- | :--- | :--- |
| **Integer** | `int` | Whole numbers (positive, negative, or zero) | `42`, `-7`, `0`, `1000000` |
| **Float** | `float` | Real numbers containing a decimal point | `3.14159`, `-0.5`, `2.0` |
| **String** | `str` | Ordered sequence of characters / text | `"Python"`, `'CS101'`, `""` |
| **Boolean** | `bool` | Logical truth values (Only two possible values) | `True`, `False` |

```python
# Demonstrating types
age = 20                 # int
gpa = 3.85               # float
major = "Computer Sci"   # str
is_graduated = False     # bool

# Checking the type using the built-in type() function:
print(type(age))          # <class 'int'>
print(type(gpa))          # <class 'float'>
print(type(major))        # <class 'str'>
print(type(is_graduated)) # <class 'bool'>
```

---

## 4. Modern String Formatting (f-strings)

Introduced in Python 3.6, **f-strings** (formatted string literals) are the fastest, cleanest, and most readable way to format strings.

Prefix your string with `f` (or `F`), and insert variables or expressions inside curly braces `{}`:

```python
student_name = "Maria"
current_year = 1
average_grade = 92.485

# Basic f-string
message = f"Student {student_name} is in year {current_year}."
print(message)

# Expressions inside f-strings:
print(f"In two years, {student_name} will be in year {current_year + 2}.")

# Decimal precision formatting:
# :.2f means format as float rounded to 2 decimal places
print(f"Grade: {average_grade:.2f}%")  # Output: Grade: 92.49%
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_1.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Lessons/Lesson_1.py):

```python
course_name = "CS101"
student_count = 120
pass_rate = 94.5

print(f"Welcome to {course_name}! There are {student_count} students enrolled with a {pass_rate}% pass rate.")
```

---

## 📝 Quick Exercise

**Prompt**:
1. Create a variable `item_name` set to `"Laptop"`.
2. Create a variable `item_price` set to `999.99`.
3. Create a variable `in_stock` set to `True`.
4. Create a variable `quantity` set to `3`.
5. Use an f-string to print:
   `"Item: Laptop | Price: $999.99 | In Stock: True | Total Value: $2999.97"`

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
item_name = "Laptop"
item_price = 999.99
in_stock = True
quantity = 3

total_value = item_price * quantity

print(f"Item: {item_name} | Price: ${item_price:.2f} | In Stock: {in_stock} | Total Value: ${total_value:.2f}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **Which of the following variable names is illegal in Python?**
   - A) `student_score`
   - B) `_max_value`
   - C) `1st_place`
   - D) `totalScore2`

2. **What is the data type of `x = "False"`?**
   - A) `bool`
   - B) `str`
   - C) `int`
   - D) `None`

3. **What is the printed result of `f"{2 + 3 * 2}"`?**
   - A) `"10"`
   - B) `"8"`
   - C) `"2 + 3 * 2"`
   - D) `Error`

<details>
<summary><b>View Answers</b></summary>
1: C (Variables cannot start with a number)<br>
2: B (Quotes indicate a string literal)<br>
3: B (Standard order of operations: 3*2 = 6, 6+2 = 8)
</details>
