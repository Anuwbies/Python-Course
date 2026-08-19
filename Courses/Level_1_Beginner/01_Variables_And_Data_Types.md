# Lesson 1: Printing, Variables & Primitive Data Types

Welcome to your first Python lesson! In computer science, software development begins with data: how we represent information, store it in memory, transform it, and present it clearly to users.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master terminal output using `print()`, including the `sep` and `end` parameters.
2. Understand computer memory variables, reference assignment, and dynamic typing.
3. Distinguish and use the 4 core primitive data types (`int`, `float`, `str`, `bool`).
4. Inspect data types dynamically using the built-in `type()` function.
5. Format numbers and text cleanly using modern **f-strings** with precision, thousands separators, and alignment specifiers.
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
print("Loading server data", end="...")
print(" [DONE]")                             # Output: Loading server data... [DONE]
```

---

## 2. Variables & The Python Memory Model

A **variable** is a symbolic name that references an object stored in computer memory.

### Static vs. Dynamic Typing
In statically typed languages (like C++ or Java), you must declare the variable type upfront:
```cpp
int userAge = 25; // C++
```

In Python, typing is **dynamic**. Python infers the type automatically at runtime based on the assigned value:
```python
user_age = 25          # Inferred as int
user_age = "Twenty-Five" # Rebound to a str (Dynamic rebinding)
```

```
Variable Name (Tag)         Memory Object
[ user_age ] ------------> ( Integer: 25 )
```

---

## 3. The Four Core Primitive Data Types

Python has four foundational primitive types that represent single values:

| Type | Name | Description | Example Values |
| :--- | :--- | :--- | :--- |
| `int` | Integer | Whole numbers (positive, negative, zero) with arbitrary precision | `42`, `-10`, `0`, `1_000_000` |
| `float` | Floating-point | Real numbers with decimal fractions (IEEE 754 64-bit) | `3.14159`, `-0.005`, `2.0`, `1e-3` |
| `str` | String | Immutable sequences of Unicode characters enclosed in quotes | `"Hello"`, `'Python 3'`, `"123"` |
| `bool` | Boolean | Logical truth values (`True` or `False`) | `True`, `False` |

```python
server_nodes = 16              # int
cpu_utilization = 78.45        # float
cluster_region = "us-east-1"   # str
is_healthy = True              # bool

# Inspecting types at runtime:
print(type(server_nodes))      # <class 'int'>
print(type(cpu_utilization))   # <class 'float'>
print(type(cluster_region))    # <class 'str'>
print(type(is_healthy))        # <class 'bool'>
```

---

## 4. Modern String Interpolation: f-strings

Introduced in Python 3.6, **Formatted String Literals (f-strings)** provide the most readable, performant way to embed expressions inside string literals.

Prefix the string with `f` or `F` and place variables or expressions inside `{}`:

```python
item = "Database Server"
rate_per_hour = 3.456
hours = 24

# Basic interpolation:
print(f"Service: {item} | Cost: ${rate_per_hour * hours}")

# Decimal precision specifier (:.2f formats float to 2 decimal places):
print(f"Daily Cost: ${rate_per_hour * hours:.2f}")  # Output: $82.94

# Thousands comma separator (:, or :,.2f):
annual_budget = 1450000.758
print(f"Budget: ${annual_budget:,.2f}")             # Output: $1,450,000.76

# Column alignment specifiers (< left align, > right align, ^ center align):
print(f"{'Service':<20} | {'Status':^10} | {'Rate':>8}")
print("-" * 44)
print(f"{'Cloud DB':<20} | {'ONLINE':^10} | {'$3.45':>8}")
print(f"{'Redis Cache':<20} | {'ONLINE':^10} | {'$1.20':>8}")
```

---

## 5. Python Naming Conventions (PEP 8)

Follow the official Python Style Guide (**PEP 8**):
1. **Variables & Functions**: Use `snake_case` (lowercase letters with underscores):
   - `total_price`, `max_retry_count`, `is_authenticated`
2. **Constants**: Use `UPPER_CASE_WITH_UNDERSCORES`:
   - `MAX_CONNECTIONS = 100`, `TAX_RATE = 0.08`
3. **Keywords to Avoid**: Never use reserved keywords (`if`, `class`, `def`, `for`, `print`, `type`) as variable names.

---

## 💻 Code Example & Reference

The following real-life program models a **Cloud Infrastructure Billing & Server Telemetry Monitor**, combining all the concepts taught in this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Cloud Infrastructure Telemetry & Invoice Reporter
# =====================================================================

# 1. Variable Declarations & Primitive Data Types
service_id = "AWS-EC2-CLUSTER-09"         # str
allocated_cores = 64                      # int
hourly_node_rate = 0.3875                 # float (precise computing cost)
uptime_hours = 720.0                      # float (monthly continuous hours)
is_high_availability = True               # bool (redundancy status)

# 2. Inspecting Types with type()
print("--- [System Type Introspection] ---")
print("service_id type:      ", type(service_id), sep="\t")
print("allocated_cores type: ", type(allocated_cores), sep="\t")
print("hourly_node_rate type:", type(hourly_node_rate), sep="\t")
print("is_ha status type:    ", type(is_high_availability), sep="\t")
print()

# 3. Arithmetic Computations
base_compute_cost = allocated_cores * hourly_node_rate * uptime_hours
redundancy_fee = 150.00 if is_high_availability else 0.00
gross_invoice_amount = base_compute_cost + redundancy_fee

# 4. Formatted Terminal Output with sep, end, and alignment f-strings
print("Initializing Cluster Telemetry", end="...")
print(" [SUCCESS]\n")

print("=" * 60)
print(f"{'CLOUD TELEMETRY & BILLING REPORT':^60}")
print("=" * 60)
print(f"{'Metric / Property':<35} | {'Value':>20}")
print("-" * 60)
print(f"{'Service Identifier':<35} | {service_id:>20}")
print(f"{'Allocated CPU Cores':<35} | {allocated_cores:>20}")
print(f"{'Hourly Core Cost Rate':<35} | {f'${hourly_node_rate:.4f}':>20}")
print(f"{'Monthly Active Uptime (Hrs)':<35} | {f'{uptime_hours:.1f}':>20}")
print(f"{'High Availability Enabled':<35} | {str(is_high_availability):>20}")
print("-" * 60)
print(f"{'Base Compute Subtotal':<35} | {f'${base_compute_cost:,.2f}':>20}")
print(f"{'Redundancy Surcharge':<35} | {f'${redundancy_fee:,.2f}':>20}")
print("=" * 60)
print(f"{'TOTAL INVOICE AMOUNT':<35} | {f'${gross_invoice_amount:,.2f}':>20}")
print("=" * 60)
```

### 🔍 Code Explanation:
- **Variables & Types**: Variables are initialized with descriptive `snake_case` names across all 4 primitive types (`str`, `int`, `float`, `bool`).
- **`type()` & `sep`**: We display the type of each variable, utilizing `sep="\t"` to create clean tab stops.
- **`end="..."`**: We print an initialization message without an immediate newline, completing it with `[SUCCESS]`.
- **f-string Alignment**: We construct an aligned terminal table using `{text:<35}` (left-aligned 35 characters), `{text:^60}` (centered 60 characters), and `{value:>20}` (right-aligned 20 characters).
- **Number Formatting**: Currency totals are formatted using `:,.2f` to guarantee two decimal places and commas for thousands.

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
3. Using only **f-strings** and **`print()`**, output an itemized invoice formatted exactly as shown in the expected output, with all monetary values formatted to 2 decimal places (`:.2f`).

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

**Explanation of the Solution:**
- We store all transaction facts in typed variables conforming to PEP 8 snake_case.
- We multiply `unit_price` by `quantity` to get `subtotal`, and adjust for discounts and shipping to compute `final_total`.
- We use f-strings with `:.2f` float precision format specifiers to display values to standard financial precision.
</details>
