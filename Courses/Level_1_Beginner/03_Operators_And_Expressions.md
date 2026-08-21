# Lesson 3: Operators, Boolean Logic & Expressions

Computers fundamentally operate by evaluating expressions—combining values, variables, and operators to yield new data and make decisions. In this lesson, you will master all families of Python operators, logical evaluation strategies, and operator precedence.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master all 7 Arithmetic Operators, distinguishing True Division (`/`) from Floor Division (`//`) and Modulo (`%`).
2. Utilize Augmented Assignment Operators (`+=`, `-=`, `*=`, etc.) for clean state updates.
3. Compare values using the 6 Relational/Comparison Operators (`==`, `!=`, `<`, `>`, `<=`, `>=`).
4. Construct compound boolean decisions using Logical Operators (`and`, `or`, `not`).
5. Understand **Short-Circuit Evaluation** and its practical performance/safety implications.
6. Evaluate expressions reliably following Python's **Operator Precedence (PEMDAS)**.

---

## 1. Arithmetic Operators

Python supports 7 core arithmetic operators:

```python
a = 17
b = 5

# 1. Addition (+) & Subtraction (-)
print(a + b)   # 22
print(a - b)   # 12

# 2. Multiplication (*) & Exponentiation (**)
print(a * b)   # 85
print(b ** 3)  # 5 * 5 * 5 = 125 (5 cubed)

# 3. True Division (/) -> ALWAYS returns a float
print(a / b)   # 3.4

# 4. Floor / Integer Division (//) -> Discards decimal remainder
print(a // b)  # 3

# 5. Modulo (%) -> Returns the remainder after integer division
print(a % b)   # 2 (since 17 = 5 * 3 + 2)
```

### Essential Practical Uses of Modulo (`%`) and Floor Division (`//`):
1. **Even vs. Odd Check**: Any number `n % 2 == 0` is even; `n % 2 != 0` is odd.
2. **Unit Conversions (Hours/Minutes/Seconds or Change Breakdown)**:
   ```python
   total_seconds = 3725
   hours = total_seconds // 3600    # 1 hour
   rem_seconds = total_seconds % 3600
   minutes = rem_seconds // 60      # 2 minutes
   seconds = rem_seconds % 60       # 5 seconds
   print(f"{hours}h {minutes}m {seconds}s") # 1h 2m 5s
   ```

---

## 2. Augmented Assignment Operators

Instead of writing `balance = balance + deposit`, Python provides compact augmented assignment operators:

```python
inventory = 100
inventory += 25   # inventory = inventory + 25 (125)
inventory -= 10   # inventory = inventory - 10 (115)
inventory *= 2    # inventory = inventory * 2  (230)
inventory //= 4   # inventory = inventory // 4 (57)
inventory %= 10   # inventory = inventory % 10 (7)
inventory **= 2   # inventory = inventory ** 2 (49)
```

---

## 3. Comparison (Relational) Operators

Comparison operators evaluate expressions and unconditionally return a boolean (`True` or `False`):

| Operator | Meaning | Example | Result |
| :---: | :--- | :--- | :---: |
| `==` | Equal to | `10 == 10` | `True` |
| `!=` | Not equal to | `10 != 5` | `True` |
| `>` | Strictly greater than | `15 > 20` | `False` |
| `<` | Strictly less than | `8 < 12` | `True` |
| `>=` | Greater than or equal to | `10 >= 10` | `True` |
| `<=` | Less than or equal to | `7 <= 5` | `False` |

---

## 4. Logical Operators & Short-Circuit Evaluation

Logical operators combine multiple boolean expressions:

| Operator | Description | Truth Condition |
| :---: | :--- | :--- |
| `and` | Logical AND | Returns `True` **only if both** operands are `True` |
| `or` | Logical OR | Returns `True` **if at least one** operand is `True` |
| `not` | Logical NOT | Inverts truth value (`not True` $\rightarrow$ `False`) |

```python
user_age = 22
has_license = True
has_dui_record = False

# Eligible to rent vehicle?
is_eligible = (user_age >= 21) and has_license and (not has_dui_record)
print(f"Rental Approved: {is_eligible}") # True
```

### ⚡ Short-Circuit Evaluation
Python stops evaluating a compound expression as soon as the outcome is guaranteed:
- In `A and B`: If `A` is `False`, Python immediately returns `False` without evaluating `B`.
- In `A or B`: If `A` is `True`, Python immediately returns `True` without evaluating `B`.

This prevents errors, such as avoiding division by zero:
```python
total_count = 0
total_sum = 100
# Safe because total_count != 0 short-circuits before the division executes:
if total_count != 0 and (total_sum / total_count > 50):
    print("Above threshold")
```

---

## 5. Object Identity (`is`) vs. Value Equality (`==`)

A critical distinction in Python is the difference between comparing **values** versus comparing **memory identities**:

- **`==` (Value Equality)**: Calls the `__eq__()` method to check if two objects contain equivalent data/values.
- **`is` (Identity Comparison)**: Checks if two variables point to the **exact same memory address** (`id(a) == id(b)`).

```python
list_a = [1, 2, 3]
list_b = [1, 2, 3]
list_c = list_a

print(list_a == list_b) # True  (They have identical contents)
print(list_a is list_b) # False (They are distinct objects in heap memory!)
print(list_a is list_c) # True  (list_c references the exact same list)
```

> [!IMPORTANT]
> **Always compare with `None` using `is`**:
> Use `if val is None:` or `if val is not None:` instead of `== None`. `None` is a singleton in Python, and `is` is faster and cannot be overridden.

---

## 6. Bitwise Operators & Flag Masking

Bitwise operators manipulate individual binary bits of integer numbers:

| Operator | Name | Operation | Example (`a=5` (0101₂), `b=3` (0011₂)) | Result |
| :---: | :--- | :--- | :--- | :--- |
| `&` | Bitwise AND | Bit is `1` if both bits are `1` | `5 & 3` (0101 & 0011) | `1` (0001₂) |
| `\|` | Bitwise OR | Bit is `1` if either bit is `1` | `5 \| 3` (0101 \| 0011) | `7` (0111₂) |
| `^` | Bitwise XOR | Bit is `1` if bits are different | `5 ^ 3` (0101 ^ 0011) | `6` (0110₂) |
| `~` | Bitwise NOT | Inverts all bits (`-x - 1`) | `~5` | `-6` |
| `<<` | Left Shift | Shifts bits left (multiplies by $2^n$) | `5 << 1` | `10` (1010₂) |
| `>>` | Right Shift | Shifts bits right (floor divides by $2^n$) | `5 >> 1` | `2` (0010₂) |

```python
# System Permission Bitmasking Example:
READ_PERMISSION = 0b001   # 1
WRITE_PERMISSION = 0b010  # 2
EXEC_PERMISSION = 0b100   # 4

# Combine permissions using Bitwise OR:
user_perms = READ_PERMISSION | EXEC_PERMISSION # 0b101 (5)

# Check permission using Bitwise AND:
has_write = (user_perms & WRITE_PERMISSION) != 0 # False
has_read = (user_perms & READ_PERMISSION) != 0   # True
```

---

## 7. The Walrus Operator (`:=`) (Assignment Expressions)

Introduced in Python 3.8, the **walrus operator (`:=`)** allows you to assign values to variables *within* an expression.

```python
# Standard two-step approach:
val = input("Enter command: ").strip()
if len(val) > 0:
    print(f"Executing: {val}")

# Walrus assignment expression:
if (cmd := input("Enter command: ").strip()):
    print(f"Executing: {cmd} (Length: {len(cmd)})")
```

---

## 8. Operator Precedence (Order of Operations)

When multiple operators appear in a single expression, Python evaluates them in strict precedence:

1. **Parentheses**: `( )`
2. **Exponentiation**: `**`
3. **Bitwise NOT, Unary Signs**: `~x`, `+x`, `-x`
4. **Multiplication, Division, Floor Div, Modulo**: `*`, `/`, `//`, `%`
5. **Addition, Subtraction**: `+`, `-`
6. **Bitwise Shifts**: `<<`, `>>`
7. **Bitwise AND**: `&`
8. **Bitwise XOR, OR**: `^`, `|`
9. **Comparisons & Identity/Membership**: `==`, `!=`, `<`, `>`, `<=`, `>=`, `is`, `is not`, `in`, `not in`
10. **Logical NOT**: `not`
11. **Logical AND**: `and`
12. **Logical OR**: `or`
13. **Walrus Operator / Assignment**: `:=`, `=`

---

## 💻 Code Example & Reference

The following real-life program models an **Automated Warehouse Palletizing & Shipping Tier Engine**, utilizing all operators and evaluation concepts taught in this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Automated Warehouse Pallet & Freight Tier Engine
# =====================================================================

print("=" * 65)
print(f"{'📦 LOGISTICS PALLETIZING & FREIGHT VALIDATION ENGINE':^65}")
print("=" * 65)

# 1. Capture and cast order specifications (Lessons 1 & 2)
sku_code = input("Enter Product SKU: ").strip().upper()
unit_weight_kg = float(input("Enter unit item weight (kg): "))
total_ordered_units = int(input("Enter total units ordered: "))
is_fragile_str = input("Is the shipment marked fragile? (yes/no): ").strip().lower()
is_fragile = is_fragile_str in ("yes", "y", "true")

# 2. Arithmetic & Division Mechanics (Lesson 3)
UNITS_PER_PALLET = 48
full_pallets = total_ordered_units // UNITS_PER_PALLET
loose_boxes = total_ordered_units % UNITS_PER_PALLET
has_loose_boxes = loose_boxes != 0

total_gross_weight_kg = total_ordered_units * unit_weight_kg
pallet_tare_weight_kg = (full_pallets + (1 if has_loose_boxes else 0)) * 22.5
total_shipment_weight = total_gross_weight_kg + pallet_tare_weight_kg

# 3. Augmented State Tracking (Lesson 3)
estimated_handling_cost = 50.00
estimated_handling_cost += full_pallets * 15.00
if has_loose_boxes:
    estimated_handling_cost += loose_boxes * 1.50
if is_fragile:
    estimated_handling_cost *= 1.20 # 20% delicate handling fee

# 4. Complex Logical Expressions with Short-Circuiting (Lesson 3)
MAX_STANDARD_WEIGHT_KG = 2500.0
is_heavy_freight = total_shipment_weight > 1000.0
requires_special_carrier = (total_shipment_weight >= MAX_STANDARD_WEIGHT_KG) or (is_fragile and is_heavy_freight)
qualifies_for_direct_dispatch = (full_pallets >= 2) and (not requires_special_carrier) and (total_ordered_units % 2 == 0)

# 5. Formatted Operational Summary (Lessons 1 & 2)
print("\n" + "=" * 65)
print(f"{'WAREHOUSE DISPATCH MANIFEST':^65}")
print("=" * 65)
print(f"{'Product SKU:':<32} {sku_code}")
print(f"{'Total Ordered Units:':<32} {total_ordered_units:,} units")
print(f"{'Full Pallet Stacks (48/plt):':<32} {full_pallets} full pallets")
print(f"{'Loose Package Count:':<32} {loose_boxes} loose boxes")
print(f"{'Total Cargo Weight:':<32} {total_shipment_weight:,.2f} kg")
print("-" * 65)
print(f"{'Special Carrier Required:':<32} {str(requires_special_carrier)}")
print(f"{'Direct Dispatch Clearance:':<32} {str(qualifies_for_direct_dispatch)}")
print("-" * 65)
print(f"{'TOTAL HANDLING & FREIGHT FEE:':<32} ${estimated_handling_cost:,.2f}")
print("=" * 65)
```

### 🔍 Code Explanation:
- **Floor Division & Modulo**: `total_ordered_units // 48` calculates complete pallets; `total_ordered_units % 48` calculates remaining unstacked boxes.
- **Augmented Assignments**: `+=` and `*=` update the handling charge progressively based on pallet counts and fragility status.
- **Relational & Boolean Logic**: Relational comparisons (`>=`, `!=`, `>`) combined with logical operators (`and`, `or`, `not`) determine dispatch routing rules.
- **Short-Circuit Safety**: Boolean checks verify freight limits and conditions without unnecessary sub-evaluations.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master arithmetic, boolean expressions, short-circuit evaluation, identity vs equality, bitwise logic, and the walrus operator:

---

### 🟢 Tier 1: Arithmetic & Augmented Assignment (Exercises 1–3)

#### 🔹 Exercise 1: Even/Odd Modulo Detector
* **Goal**: Prompt the user for an integer number.
* **Requirement**: Use `% 2` to evaluate if the number is even (`is_even = (num % 2 == 0)`). Print `f"Is Even: {is_even}"`.

#### 🔹 Exercise 2: Time Duration Decomposer
* **Goal**: Given `total_seconds = 7384`.
* **Calculation**: Use `//` and `%` to calculate hours, minutes, and remaining seconds.
* **Requirement**: Print in `Xh Ym Zs` format.

#### 🔹 Exercise 3: Augmented Score Tracker
* **Goal**: Initialize `score = 100`.
* **Operations**: Add 25, multiply by 2, subtract 50, and floor divide by 4 using augmented operators (`+=`, `*=`, `-=`, `//=`). Print final score.

---

### 🟡 Tier 2: Relational Logic & Short-Circuiting (Exercises 4–6)

#### 🔹 Exercise 4: Loan Pre-Qualification Decision
* **Goal**: Given `credit_score = 720`, `income = 65000.0`, `has_bankruptcies = False`.
* **Rule**: Pre-approved if `credit_score >= 680` AND `income >= 50000` AND `not has_bankruptcies`.
* **Requirement**: Print boolean result.

#### 🔹 Exercise 5: Short-Circuit Safe Division Guard
* **Goal**: Given `count = 0` and `total = 500`.
* **Requirement**: Write a single boolean expression `is_valid_avg = (count > 0) and ((total / count) >= 50)`. Verify it evaluates to `False` without crashing with `ZeroDivisionError`.

#### 🔹 Exercise 6: Chained Comparison Range Checker
* **Goal**: Prompt for temperature reading in Celsius.
* **Requirement**: Check if temperature is within operating range using chained comparison `18.0 <= temp <= 27.5`.

---

### 🟠 Tier 3: Memory Identity & Bitwise Operations (Exercises 7–9)

#### 🔹 Exercise 7: Object Identity vs Equality Tester
* **Goal**: Create two identical lists `list1 = [10, 20]` and `list2 = [10, 20]`.
* **Requirement**: Print results of `list1 == list2` and `list1 is list2`. Rebind `list3 = list1` and test `list1 is list3`.

#### 🔹 Exercise 8: Bitwise Permission Flag System
* **Goal**: Define bitmask constants `ADMIN = 4`, `EDITOR = 2`, `VIEWER = 1`.
* **Requirement**: Create a user with `user_role = EDITOR | VIEWER` (bitwise OR). Check if user has `ADMIN` permission using bitwise AND (`&`).

#### 🔹 Exercise 9: Interactive Walrus Loop Validator
* **Goal**: Prompt the user for input and simultaneously assign and check length using `:=`:
  `if (msg := input("Enter message: ").strip()): print(f"Received: {msg}")`.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Cash Drawer Optimal Change Dispenser
* **Goal**: Prompt for `total_due` and `cash_paid`. Perform exact integer cent conversion and decompose change into minimal bills, quarters, dimes, nickels, and pennies.

---

## 📝 Quick Exercise: Point of Sale Coin Change Breakdown & Discount Matrix

### 🏢 Real-Life Scenario
You are developing the cashier change calculator and cash drawer dispenser for a physical retail store. When a customer pays cash for an invoice, the system computes the exact change due and breaks down the change into the minimum number of physical currency denominations (Dollars, Quarters, Dimes, Nickels, Pennies) using floor division and modulo arithmetic.

### 📋 Requirements
1. Capture and sanitize inputs:
   - `cashier_name`: Sanitized with `.strip().title()`
   - `total_due`: Total amount owed in dollars (e.g. `17.38`), cast to `float`
   - `cash_paid`: Cash handed by customer (e.g. `20.00`), cast to `float`
2. Perform arithmetic and denomination breakdown:
   - Calculate `change_due_dollars = cash_paid - total_due`.
   - Convert `change_due_cents = round(change_due_dollars * 100)` to work cleanly in integers without float rounding errors.
   - Compute exact counts:
     - `dollars = change_due_cents // 100`
     - `rem_cents_1 = change_due_cents % 100`
     - `quarters = rem_cents_1 // 25`
     - `rem_cents_2 = rem_cents_1 % 25`
     - `dimes = rem_cents_2 // 10`
     - `rem_cents_3 = rem_cents_2 % 10`
     - `nickels = rem_cents_3 // 5`
     - `pennies = rem_cents_3 % 5`
3. Boolean Logic:
   - Check if exact payment was made (`change_due_cents == 0`).
   - Check if coin change is required (`change_due_cents % 100 != 0`).
4. Output the receipt using formatted f-strings.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1, 2, and 3** (primitives, casting, string sanitization, arithmetic operators `//`, `%`, comparison `==`, `!=`, and f-strings).

### 🎯 Expected Output
*(Assuming the user inputs: Cashier: `  marcus vance  `, Total Due: `17.37`, Cash Paid: `20.00`)*

```text
Enter Cashier Name:   marcus vance  
Enter Total Due ($): 17.37
Enter Cash Handed ($): 20.00

==================================================
              CASH DRAWER DISPENSER               
==================================================
Cashier:          Marcus Vance
Total Amount Due: $17.37
Cash Received:    $20.00
--------------------------------------------------
TOTAL CHANGE DUE: $2.63 (263 cents)
Coin Change Needed: True
==================================================
OPTIMAL CHANGE DENOMINATIONS:
  $1.00 Dollar Bills: 2
  $0.25 Quarters:     2
  $0.10 Dimes:        1
  $0.05 Nickels:      0
  $0.01 Pennies:      3
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Cash Drawer & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Cash Drawer Dispenser
# =====================================================================
cashier_name = input("Enter Cashier Name: ").strip().title()
total_due = float(input("Enter Total Due ($): "))
cash_paid = float(input("Enter Cash Handed ($): "))

change_due_dollars = cash_paid - total_due
change_due_cents = int(round(change_due_dollars * 100))

dollars = change_due_cents // 100
rem_cents_1 = change_due_cents % 100

quarters = rem_cents_1 // 25
rem_cents_2 = rem_cents_1 % 25

dimes = rem_cents_2 // 10
rem_cents_3 = rem_cents_2 % 10

nickels = rem_cents_3 // 5
pennies = rem_cents_3 % 5

needs_coin_change = (change_due_cents % 100) != 0

print("\n==================================================")
print("              CASH DRAWER DISPENSER               ")
print("==================================================")
print(f"Cashier:          {cashier_name}")
print(f"Total Amount Due: ${total_due:.2f}")
print(f"Cash Received:    ${cash_paid:.2f}")
print("--------------------------------------------------")
print(f"TOTAL CHANGE DUE: ${change_due_dollars:.2f} ({change_due_cents} cents)")
print(f"Coin Change Needed: {needs_coin_change}")
print("==================================================")
print("OPTIMAL CHANGE DENOMINATIONS:")
print(f"  $1.00 Dollar Bills: {dollars}")
print(f"  $0.25 Quarters:     {quarters}")
print(f"  $0.10 Dimes:        {dimes}")
print(f"  $0.05 Nickels:      {nickels}")
print(f"  $0.01 Pennies:      {pennies}")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
num = int(input("Enter integer: "))
print(f"Is Even: {num % 2 == 0}")

# Ex 2:
total_s = 7384
h = total_s // 3600
m = (total_s % 3600) // 60
s = total_s % 60
print(f"{h}h {m}m {s}s")

# Ex 3:
score = 100
score += 25
score *= 2
score -= 50
score //= 4
print(f"Final Score: {score}")

# Ex 4:
credit_score, income, has_bankruptcies = 720, 65000.0, False
approved = (credit_score >= 680) and (income >= 50000) and (not has_bankruptcies)
print(f"Approved: {approved}")

# Ex 5:
count, total = 0, 500
is_valid_avg = (count > 0) and ((total / count) >= 50)
print(f"Valid Average: {is_valid_avg}")

# Ex 6:
temp = float(input("Temperature (°C): "))
print(f"In Normal Range: {18.0 <= temp <= 27.5}")

# Ex 7:
l1, l2 = [10, 20], [10, 20]
l3 = l1
print(f"Equal Value: {l1 == l2}, Identical Object: {l1 is l2}, Aliased Object: {l1 is l3}")

# Ex 8:
ADMIN, EDITOR, VIEWER = 4, 2, 1
user_perms = EDITOR | VIEWER
has_admin = (user_perms & ADMIN) != 0
print(f"User Permissions: {bin(user_perms)}, Has Admin: {has_admin}")

# Ex 9:
if (msg := input("Enter status code: ").strip()):
    print(f"Captured: {msg}")
```
</details>
