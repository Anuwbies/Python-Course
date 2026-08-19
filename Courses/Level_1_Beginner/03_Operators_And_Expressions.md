# Lesson 3: Operators & Arithmetic Expressions

Operators are special symbols and keywords in Python that carry out mathematical computations, logical evaluations, and value assignments. In this lesson, you will master arithmetic operators, augmented assignments, comparison checks, and boolean logic.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Master all 7 arithmetic operators (`+`, `-`, `*`, `/`, `//`, `%`, `**`) and their behavioral nuances.
2. Apply floor division (`//`) and modulus (`%`) to solve real-world partitioning and time decomposition problems.
3. Understand Operator Precedence (PEMDAS/BODMAS) and express complex mathematical equations cleanly.
4. Use shorthand augmented assignment operators (`+=`, `-=`, `*=`, etc.) for in-place updates.
5. Formulate comparison expressions (`==`, `!=`, `<`, `>`, `<=`, `>=`).
6. Construct compound boolean logic using `and`, `or`, and `not`, including **Short-Circuit Evaluation**.

---

## 1. The 7 Arithmetic Operators

| Operator | Operation | Syntax | Example | Result | Type Returned |
| :---: | :--- | :--- | :--- | :--- | :--- |
| `+` | Addition | `a + b` | `15 + 4` | `19` | `int` or `float` |
| `-` | Subtraction | `a - b` | `15 - 4` | `11` | `int` or `float` |
| `*` | Multiplication | `a * b` | `15 * 4` | `60` | `int` or `float` |
| `/` | **True Division** | `a / b` | `15 / 4` | `3.75` | **Always `float`** |
| `//` | **Floor Division** | `a // b` | `15 // 4` | `3` | `int` (rounds down) |
| `%` | **Modulus (Remainder)** | `a % b` | `15 % 4` | `3` | `int` or `float` |
| `**` | **Exponentiation (Power)**| `a ** b` | `2 ** 4` | `16` ($2^4$) | `int` or `float` |

### 💡 Why `//` and `%` are Fundamental in Computer Science
Floor division (`//`) discards the fractional part and rounds down to the nearest integer. Modulus (`%`) returns the remainder left over after integer division.

#### 1. Time Unit Decomposition:
```python
total_seconds = 3725  # 1 hour, 2 minutes, 5 seconds

hours = total_seconds // 3600         # 1 hr
remaining_seconds = total_seconds % 3600  # 125 sec

minutes = remaining_seconds // 60     # 2 min
seconds = remaining_seconds % 60      # 5 sec

print(f"{hours}h {minutes}m {seconds}s")  # Output: 1h 2m 5s
```

#### 2. Even vs. Odd Testing:
```python
number = 48
is_even = (number % 2 == 0)  # True
is_odd = (number % 2 != 0)   # False
```

#### 3. Circular Cycling / Wrapping (Round-Robin):
```python
# If you have 4 worker servers (IDs 0, 1, 2, 3):
request_number = 14
assigned_worker = request_number % 4  # 2 (Wraps around cleanly)
```

---

## 2. Operator Precedence (PEMDAS / BODMAS)

When multiple operators appear in a single expression, Python evaluates them in order of priority:

1. **Parentheses** `()`: Highest precedence (overrides everything).
2. **Exponentiation** `**`: Evaluated right-to-left.
3. **Multiplication, Division, Floor Div, Modulus** `*`, `/`, `//`, `%`: Evaluated left-to-right.
4. **Addition and Subtraction** `+`, `-`: Evaluated left-to-right.

```python
# Without parentheses:
result1 = 5 + 3 * 2 ** 3   # 2**3=8 -> 3*8=24 -> 5+24 = 29

# With parentheses:
result2 = (5 + 3) * (2 ** 3)  # 8 * 8 = 64
```

> [!TIP]
> Always use parentheses when writing compound formulas. It eliminates ambiguity and makes your code self-documenting for team members.

---

## 3. Augmented Assignment Operators

Instead of retyping a variable name to update its value (`counter = counter + 1`), Python provides augmented assignment operators:

```python
balance = 1000.00
balance += 250.00   # balance = balance + 250.00 (now 1250.00)
balance -= 50.00    # balance = balance - 50.00  (now 1200.00)
balance *= 1.05     # balance = balance * 1.05   (now 1260.00, 5% interest)
balance /= 2        # balance = balance / 2      (now 630.00)
balance //= 10      # balance = balance // 10    (now 63.0)
balance %= 20       # balance = balance % 20     (now 3.0)
```

---

## 4. Comparison Operators

Comparison operators evaluate relationships between values and return a `bool` (`True` or `False`):

| Operator | Description | Example | Result |
| :---: | :--- | :--- | :---: |
| `==` | Equal to | `10 == 10.0` | `True` |
| `!=` | Not equal to | `10 != 5` | `True` |
| `>` | Greater than | `25 > 30` | `False` |
| `<` | Less than | `15 < 20` | `True` |
| `>=` | Greater than or equal to | `50 >= 50` | `True` |
| `<=` | Less than or equal to | `40 <= 39` | `False` |

> [!CAUTION]
> **Single `=` vs Double `==`**:
> - `=` is an **assignment** statement (`x = 10` puts `10` into `x`).
> - `==` is an **equality check** (`x == 10` returns `True` if `x` equals `10`).

---

## 5. Logical Operators & Short-Circuit Evaluation

Logical operators combine multiple boolean expressions:

- **`and`**: Returns `True` only if **both** operands are `True`.
- **`or`**: Returns `True` if **at least one** operand is `True`.
- **`not`**: Inverts the boolean truth value.

```python
credit_score = 720
annual_income = 65000.00
has_bankruptcies = False

# Both conditions must be met:
is_eligible = (credit_score >= 700) and (annual_income >= 50000.00)  # True

# Clean inversion:
is_creditworthy = is_eligible and (not has_bankruptcies)             # True
```

### ⚡ Short-Circuit Evaluation
Python evaluates logical expressions from left to right and stops as soon as the outcome is guaranteed:
- In `A and B`: If `A` is `False`, Python immediately returns `False` without checking `B`.
- In `A or B`: If `A` is `True`, Python immediately returns `True` without checking `B`.

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_03_Operators_And_Expressions.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_03_Operators_And_Expressions.py):

```python
# Cash Register Coin Breakdown
total_cents = int(input("Enter total change in cents (e.g. 287): "))

quarters = total_cents // 25
rem_after_quarters = total_cents % 25

dimes = rem_after_quarters // 10
rem_after_dimes = rem_after_quarters % 10

nickels = rem_after_dimes // 5
pennies = rem_after_dimes % 5

print(f"Optimal coin change for {total_cents}¢:")
print(f"Quarters (25¢): {quarters} | Dimes (10¢): {dimes} | Nickels (5¢): {nickels} | Pennies (1¢): {pennies}")
```

---

## 📝 Quick Exercise: Server Cluster Telemetry & Task Distribution

### 🏢 Real-Life Scenario
You are building an automated telemetry diagnostic script for a cloud operations center. The tool reads the total accumulated uptime in seconds for a database server, converts it into standard human units (Days, Hours, Minutes, Seconds), and computes the workload distribution of batch tasks across a worker node cluster.

### 📋 Requirements
1. Prompt and capture inputs:
   - `total_uptime_seconds`: Prompt with `"Enter server uptime in seconds: "` (`int`, e.g. `372845`).
   - `total_jobs`: Prompt with `"Enter total pending batch jobs: "` (`int`, e.g. `1025`).
   - `worker_nodes`: Prompt with `"Enter active worker server count: "` (`int`, e.g. `8`).
2. Decompose uptime using integer floor division `//` and modulus `%`:
   - 1 Day = `86400` seconds $\rightarrow$ `days = total_uptime_seconds // 86400`, `rem_days = total_uptime_seconds % 86400`
   - 1 Hour = `3600` seconds $\rightarrow$ `hours = rem_days // 3600`, `rem_hours = rem_days % 3600`
   - 1 Minute = `60` seconds $\rightarrow$ `minutes = rem_hours // 60`, `seconds = rem_hours % 60`
3. Compute cluster task distribution:
   - `jobs_per_worker = total_jobs // worker_nodes`
   - `unassigned_overflow = total_jobs % worker_nodes`
4. Formulate boolean health checks using comparison and logical operators:
   - `meets_sla`: Uptime is greater than or equal to 1 day (`days >= 1`).
   - `is_perfectly_balanced`: Unassigned overflow equals zero (`unassigned_overflow == 0`).
   - `is_overloaded`: `jobs_per_worker > 100` or `unassigned_overflow >= 5`.
   - `is_cluster_healthy`: Meets SLA and is not overloaded (`meets_sla and (not is_overloaded)`).
5. Output the structured telemetry report.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1, 2, and 3 (variables, primitives, `input()`, `int()`, `float()`, arithmetic operators, comparison operators, logical operators, f-strings, and `print()`). Do **not** use `if` statements, loops, or functions.

### 🎯 Sample Interactive Run
```text
Enter server uptime in seconds: 372845
Enter total pending batch jobs: 1025
Enter active worker server count: 8

==================================================
        CLOUD CLUSTER TELEMETRY REPORT            
==================================================
Uptime Breakdown: 4d 7h 34m 5s (Total: 372845s)
--------------------------------------------------
WORKLOAD DISTRIBUTION:
Total Batch Jobs:    1025
Active Worker Nodes: 8
Jobs Per Node:       128
Unassigned Backlog:  1
--------------------------------------------------
DIAGNOSTIC HEALTH CHECKS:
Meets 24h SLA:       True
Perfect Load Split:  False
Cluster Overloaded:  True
Cluster Healthy:     False
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Capture inputs
total_uptime_seconds = int(input("Enter server uptime in seconds: "))
total_jobs = int(input("Enter total pending batch jobs: "))
worker_nodes = int(input("Enter active worker server count: "))

# 2. Decompose uptime
days = total_uptime_seconds // 86400
rem_days = total_uptime_seconds % 86400

hours = rem_days // 3600
rem_hours = rem_days % 3600

minutes = rem_hours // 60
seconds = rem_hours % 60

# 3. Workload distribution
jobs_per_worker = total_jobs // worker_nodes
unassigned_overflow = total_jobs % worker_nodes

# 4. Diagnostic boolean evaluations
meets_sla = days >= 1
is_perfectly_balanced = unassigned_overflow == 0
is_overloaded = (jobs_per_worker > 100) or (unassigned_overflow >= 5)
is_cluster_healthy = meets_sla and (not is_overloaded)

# 5. Formatted telemetry output
print("\n==================================================")
print("        CLOUD CLUSTER TELEMETRY REPORT            ")
print("==================================================")
print(f"Uptime Breakdown: {days}d {hours}h {minutes}m {seconds}s (Total: {total_uptime_seconds}s)")
print("--------------------------------------------------")
print("WORKLOAD DISTRIBUTION:")
print(f"Total Batch Jobs:    {total_jobs}")
print(f"Active Worker Nodes: {worker_nodes}")
print(f"Jobs Per Node:       {jobs_per_worker}")
print(f"Unassigned Backlog:  {unassigned_overflow}")
print("--------------------------------------------------")
print("DIAGNOSTIC HEALTH CHECKS:")
print(f"Meets 24h SLA:       {meets_sla}")
print(f"Perfect Load Split:  {is_perfectly_balanced}")
print(f"Cluster Overloaded:  {is_overloaded}")
print(f"Cluster Healthy:     {is_cluster_healthy}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the result of `19 // 4` and `19 % 4`?**
   - A) `4.75` and `3`
   - B) `4` and `3`
   - C) `5` and `-1`
   - D) `4` and `0.75`

2. **What does `False or not False and True` evaluate to?**
   - A) `False`
   - B) `True`
   - C) `None`
   - D) `SyntaxError`

3. **In the expression `score > 90 and verify_user()`, if `score` is 75, does Python execute `verify_user()`?**
   - A) Yes, Python always evaluates both sides.
   - B) No, because of short-circuit evaluation on `and` when the left operand is `False`.
   - C) It raises a `RuntimeError`.
   - D) It depends on whether `verify_user` is imported.

<details>
<summary><b>View Answers</b></summary>
1: B (19 // 4 is 4, 19 % 4 leaves remainder 3)<br>
2: B ('not False' is True -> 'True and True' is True -> 'False or True' is True)<br>
3: B (Short-circuiting terminates the evaluation immediately when the first condition in an 'and' check is False)
</details>
