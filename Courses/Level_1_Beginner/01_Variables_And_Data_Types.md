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

## 2. Variables & The Python Memory Model (CPython Internals)

A **variable** in Python is not a physical storage box holding data; it is an **object reference (a pointer / name tag)** bound to an object stored in heap memory.

```
Variable Name (Tag in Namespace)              Heap Object in Memory
[ user_age ] ─────────────────────────► [ Type: int | RefCount: 1 | Value: 25 ]
                                        [ Memory Address: 0x7FFF98A201 ]
```

### 🔍 Object Identity and the `id()` Function
Every object created in Python is assigned a unique integer identifier representing its memory address. You can inspect this using `id()`:

```python
x = 1000
y = 1000
print(f"Memory address of x: {id(x)}")
print(f"Memory address of y: {id(y)}")
print(f"Do x and y share the exact same memory object? {id(x) == id(y)}") # True or False depending on optimization
```

### ⚡ CPython Optimization: Small Integer Caching (-5 to 256)
CPython pre-allocates and caches an internal array of integer objects in the range **`-5` to `256`** at startup. Any variable assigned a number in this range automatically points to the exact same pre-allocated singleton in memory!

```python
a = 42
b = 42
print(id(a) == id(b)) # ALWAYS True! Both point to Python's cached singleton for 42.

c = 10000
d = 10000
print(id(c) == id(d)) # False (in standard REPL; numbers > 256 allocate distinct objects)
```

### ⚠️ Floating-Point Precision & IEEE 754 Representation
Python floats are stored as 64-bit binary floating-point numbers following the **IEEE 754 standard**. Because computers represent fractions in binary (base-2), certain decimal fractions cannot be represented exactly:

```python
print(0.1 + 0.2)          # Output: 0.30000000000000004
print(0.1 + 0.2 == 0.3)   # Output: False!
```
> [!TIP]
> **Pro-Tip**: When comparing floats in professional engineering, use `round(a + b, 10) == round(c, 10)` or `math.isclose(a + b, 0.3)` rather than strict `==` equality.

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

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to build complete confidence with printing, variables, primitive types, arithmetic, and formatted string output:

---

### 🟢 Tier 1: Printing & Basic Variables (Exercises 1–3)

#### 🔹 Exercise 1: Server Banner Formatter
* **Goal**: Declare variables `host = "web-node-01"`, `port = 8080`, and `status = "ONLINE"`.
* **Requirement**: Print a single line using `sep=" | "` that outputs `web-node-01 | 8080 | ONLINE`.

#### 🔹 Exercise 2: Continuous Loading Indicator
* **Goal**: Use two `print()` statements where the first prints `"Connecting to database"` with `end="..."` and the second prints `" [OK]"`.

#### 🔹 Exercise 3: Type Introspection Dashboard
* **Goal**: Declare one variable of each primitive type (`int`, `float`, `str`, `bool`).
* **Requirement**: Print the value and its `type()` on separate lines.

---

### 🟡 Tier 2: Arithmetic & Formatting (Exercises 4–6)

#### 🔹 Exercise 4: Precision Financial Rounding
* **Goal**: Given `cost = 45.892` and `tax = 3.671`, calculate `total = cost + tax`.
* **Requirement**: Print `total` formatted to 2 decimal places using an f-string (`:.2f`).

#### 🔹 Exercise 5: Thousands Separator Metric
* **Goal**: Given `annual_requests = 1450289450`, print `"Total Ingested: 1,450,289,450 requests"` using `:,\`.

#### 🔹 Exercise 6: Multi-Column Aligned Table
* **Goal**: Given 3 items with prices, print a formatted 3-column table (`Item Name`, `Qty`, `Price`) using `<` left, `^` center, and `>` right column alignment specifiers.

---

### 🟠 Tier 3: Memory & Multi-Step Math (Exercises 7–9)

#### 🔹 Exercise 7: Object Identity Inspector
* **Goal**: Create two variables `n1 = 200` and `n2 = 200`. Print their memory addresses using `id()`.
* **Requirement**: Verify if their IDs are identical (`id(n1) == id(n2)`).

#### 🔹 Exercise 8: Temperature Converter Script
* **Goal**: Given `temp_c = 37.5`, calculate `temp_f = (temp_c * 9/5) + 32` and `temp_k = temp_c + 273.15`.
* **Requirement**: Print a clean 3-line summary formatted to 1 decimal place.

#### 🔹 Exercise 9: Payroll Gross-to-Net Calculator
* **Goal**: Given `hourly_rate = 35.50`, `hours = 80.0`, `tax_rate = 0.18`, and `health_deduction = 120.00`.
* **Calculation**:
  - `gross = hourly_rate * hours`
  - `tax_amount = gross * tax_rate`
  - `net_pay = gross - tax_amount - health_deduction`
* **Requirement**: Print an itemized payroll statement.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Point of Sale (POS) Itemized Checkout Receipt
* **Goal**: Combine all concepts (variables, types, arithmetic, alignment, formatting) to print an itemized retail receipt.

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
<summary><b>🔍 View Exercise Solutions (POS & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: POS Retail Receipt
# =====================================================================
customer_name = "Eleanor Vance"
item_name = "Noise-Cancelling Headphones"
unit_price = 149.95
quantity = 2
is_loyalty_member = True
member_discount = 25.00
shipping_fee = 8.50

subtotal = unit_price * quantity
final_total = subtotal - member_discount + shipping_fee

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

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
host, port, status = "web-node-01", 8080, "ONLINE"
print(host, port, status, sep=" | ")

# Ex 2:
print("Connecting to database", end="...")
print(" [OK]")

# Ex 3:
age, pi, name, active = 25, 3.1415, "Alice", True
print(f"{age}: {type(age)}", f"{pi}: {type(pi)}", f"{name}: {type(name)}", f"{active}: {type(active)}", sep="\n")

# Ex 4:
cost, tax = 45.892, 3.671
total = cost + tax
print(f"Total: ${total:.2f}")

# Ex 5:
annual_requests = 1450289450
print(f"Total Ingested: {annual_requests:,} requests")

# Ex 6:
print(f"{'Item Name':<15} | {'Qty':^5} | {'Price':>8}")
print("-" * 34)
print(f"{'Mouse':<15} | {2:^5} | {f'${25.00:.2f}':>8}")

# Ex 7:
n1, n2 = 200, 200
print(f"ID n1: {id(n1)}, ID n2: {id(n2)}, Same Object: {id(n1) == id(n2)}")

# Ex 8:
temp_c = 37.5
temp_f = (temp_c * 9/5) + 32
temp_k = temp_c + 273.15
print(f"Celsius: {temp_c:.1f}°C\nFahrenheit: {temp_f:.1f}°F\nKelvin: {temp_k:.1f}K")

# Ex 9:
hourly_rate, hours, tax_rate, health_deduction = 35.50, 80.0, 0.18, 120.00
gross = hourly_rate * hours
tax_amount = gross * tax_rate
net_pay = gross - tax_amount - health_deduction
print(f"Gross: ${gross:.2f} | Tax: ${tax_amount:.2f} | Net: ${net_pay:.2f}")
```
</details>
