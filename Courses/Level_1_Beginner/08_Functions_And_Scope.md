# Lesson 8: Functions & Scope

Functions are the primary building block of structured, modular programming. They encapsulate logic into reusable, testable, and named subroutines, allowing software engineers to adhere to the **DRY principle** (*Don't Repeat Yourself*).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Define custom functions with `def`, pass parameters, and return calculated values.
2. Clearly distinguish between **returning data** (`return`) and **printing output** (`print()`).
3. Master positional parameters, keyword arguments, and default parameter values.
4. Avoid the critical **Mutable Default Argument Trap** (`def f(x=[])`).
5. Accept arbitrary arguments using `*args` (tuples) and `**kwargs` (dictionaries).
6. Understand variable scoping and the **LEGB rule** (Local, Enclosing, Global, Built-in).
7. Document functions with **PEP 257 Docstrings** and Python **Type Annotations**.

---

## 1. Defining Functions & The `return` Statement

A function is defined using the `def` keyword followed by the function name, parentheses `()`, and a colon `:`.

```python
# Function definition with type hints and docstring:
def calculate_cylinder_volume(radius: float, height: float) -> float:
    """Calculates the volume of a 3D cylinder given radius and height."""
    pi = 3.14159265
    volume = pi * (radius ** 2) * height
    return volume  # Passes the computed result back to the caller

# Calling the function and storing the result:
tank_volume = calculate_cylinder_volume(4.0, 12.5)
print(f"Cylinder Volume: {tank_volume:,.2f} cubic meters")
```

### ⚠️ `return` vs. `print()`
- `print()` displays text on the terminal screen. It cannot be used in downstream mathematical calculations.
- `return` sends a value back to the line of code that called the function.
- If a function finishes without an explicit `return` statement, it automatically returns `None`.

---

## 2. Positional, Keyword, & Default Arguments

```python
def compute_order_total(subtotal: float, tax_rate: float = 0.08, discount: float = 0.0) -> float:
    """Computes total cost with optional default tax and discount."""
    taxable_amount = subtotal - discount
    total = taxable_amount * (1.0 + tax_rate)
    return round(total, 2)

# 1. Using positional arguments:
order1 = compute_order_total(100.0)  # Uses default tax_rate=0.08, discount=0.0 -> 108.0

# 2. Overriding defaults with positional values:
order2 = compute_order_total(100.0, 0.10, 15.0)

# 3. Using explicit keyword arguments (order does not matter!):
order3 = compute_order_total(subtotal=250.0, discount=50.0, tax_rate=0.05)
```

> [!CAUTION]
> **Syntax Rule**: In a function signature, non-default parameters **must always precede** default parameters (`def func(a, b=10):` is valid; `def func(a=10, b):` is a `SyntaxError`).

---

## 3. The Mutable Default Argument Trap

In Python, default arguments are evaluated **once** when the function is defined, not every time it is called. Never use a mutable object (like a `list` or `dict`) as a default value:

```python
# ❌ DANGEROUS: The list persists across multiple calls!
# def append_log(entry: str, log_list: list = []):
#     log_list.append(entry)
#     return log_list

# ✅ PYTHONIC BEST PRACTICE: Use None as default sentinel
def append_log(entry: str, log_list: list = None) -> list:
    if log_list is None:
        log_list = []
    log_list.append(entry)
    return log_list
```

---

## 4. Flexible Arguments: `*args` and `**kwargs`

- **`*args`**: Captures any number of positional arguments into an immutable **tuple**.
- **`**kwargs`**: Captures any number of keyword arguments into a **dictionary**.

```python
# 1. *args Example: Multi-number statistical aggregator
def compute_average(*scores: float) -> float:
    if not scores:
        return 0.0
    return sum(scores) / len(scores)

print(compute_average(85, 90, 78, 92, 100))  # 89.0

# 2. **kwargs Example: Dynamic configuration builder
def configure_server(hostname: str, ip_address: str, **settings) -> dict:
    config = {
        "hostname": hostname,
        "ip_address": ip_address,
        "metadata": settings  # captured as a dictionary
    }
    return config

server = configure_server("prod-db-1", "10.0.0.1", port=5432, ssl=True, timeout_sec=30)
print(server)
```

---

## 5. Variable Scope & The LEGB Rule

Scope determines where a variable can be seen and accessed in your code. Python resolves names in the **LEGB** order:

1. **L - Local**: Variables defined inside the current function.
2. **E - Enclosing**: Variables in outer enclosing functions (closures).
3. **G - Global**: Variables defined at the top level of the script.
4. **B - Built-in**: Python's pre-loaded names (`print`, `len`, `sum`, `range`).

```python
app_environment = "PRODUCTION"  # Global scope

def process_transaction(amount: float):
    fee_rate = 0.025            # Local scope (only exists inside process_transaction)
    total_fee = amount * fee_rate
    print(f"[{app_environment}] Fee: ${total_fee:.2f}")

process_transaction(500.0)
# print(fee_rate)  # ❌ NameError: name 'fee_rate' is not defined (outside local scope)
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_08_Functions_And_Scope.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_08_Functions_And_Scope.py):

```python
# Financial Loan Monthly Payment Estimator
def calculate_monthly_mortgage(principal: float, annual_rate_pct: float, years: int) -> float:
    """Calculates fixed monthly payment using standard amortization formula."""
    monthly_rate = (annual_rate_pct / 100.0) / 12.0
    total_payments = years * 12
    
    if monthly_rate == 0:
        return principal / total_payments
        
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** total_payments) / (((1 + monthly_rate) ** total_payments) - 1)
    return round(monthly_payment, 2)

loan_amount = 350000.00
interest_rate = 6.5
loan_term = 30

payment = calculate_monthly_mortgage(loan_amount, interest_rate, loan_term)
print(f"30-Year Mortgage (${loan_amount:,.2f} @ {interest_rate}%): ${payment:,.2f}/month")
```

---

## 📝 Quick Exercise: Modular Enterprise Payroll & Deductions Suite

### 🏢 Real-Life Scenario
You are developing the compensation calculation engine for an enterprise Human Resources Management System (HRMS). The system requires a modular suite of functions to calculate employee gross pay (including 1.5x overtime compensation for hours exceeding 40.0), calculate mandatory and elective payroll deductions (income tax, retirement 401k contributions, health insurance), and package an itemized payslip dictionary.

### 📋 Requirements
1. Define function `calculate_gross_pay(hours_worked: float, hourly_rate: float, overtime_multiplier: float = 1.5) -> float`:
   - Standard hours are capped at 40.0.
   - If `hours_worked <= 40.0`: `gross = hours_worked * hourly_rate`.
   - Else: regular 40 hours at base rate + `(hours_worked - 40.0) * (hourly_rate * overtime_multiplier)`.
   - Returns gross pay rounded to 2 decimal places.
2. Define function `calculate_deductions(gross_pay: float, tax_rate: float = 0.18, retirement_rate: float = 0.05, health_insurance: float = 45.00) -> dict`:
   - Computes:
     - `income_tax = round(gross_pay * tax_rate, 2)`
     - `retirement_401k = round(gross_pay * retirement_rate, 2)`
     - `health_fee = round(health_insurance, 2)`
     - `total_deductions = round(income_tax + retirement_401k + health_fee, 2)`
     - `net_pay = round(gross_pay - total_deductions, 2)`
   - Returns a dictionary containing all 5 deduction metrics.
3. Define master function `generate_payslip(employee_name: str, employee_id: str, hours_worked: float, hourly_rate: float, **deduction_options) -> dict`:
   - Calls `calculate_gross_pay(hours_worked, hourly_rate)`.
   - Passes `gross_pay` and unpacks `**deduction_options` into `calculate_deductions(gross_pay, **deduction_options)`.
   - Returns a consolidated dictionary:
     ```python
     {
         "employee_name": employee_name,
         "employee_id": employee_id,
         "hours_worked": hours_worked,
         "hourly_rate": hourly_rate,
         "gross_pay": gross_pay,
         "deductions": deductions_dict,
         "net_pay": deductions_dict["net_pay"]
     }
     ```
4. Test the suite with employee `"Marcus Vance"` (ID: `"EMP-4081"`), logging `46.5` hours at `$45.00/hr`, with a custom 6% retirement contribution (`retirement_rate=0.06`), and output the itemized payslip.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 through 8 (variables, primitives, `input()`, numbers, strings, conditionals, loops, lists, tuples, dictionaries, sets, `def` functions, default parameters, `*args`, `**kwargs`, docstrings, type annotations, f-strings, and `print()`). Do **not** use file operations, `try/except`, or classes.

### 🎯 Expected Output
```text
==================================================
              APEX HR ENTERPRISE PAYSLIP          
==================================================
Employee:         Marcus Vance (ID: EMP-4081)
Hours Logged:     46.50 hrs (40.00 reg + 6.50 OT)
Hourly Base Rate: $45.00/hr
--------------------------------------------------
GROSS COMPENSATION: $2,238.75
--------------------------------------------------
PAYROLL DEDUCTIONS:
- Income Tax (18%):  $  402.98
- 401(k) Plan (6%):  $  134.32
- Health Insurance:  $   45.00
- Total Deductions:  $  582.30
--------------------------------------------------
NET TAKE-HOME PAY:  $1,656.45
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def calculate_gross_pay(hours_worked: float, hourly_rate: float, overtime_multiplier: float = 1.5) -> float:
    """Calculates total gross pay with 1.5x overtime for hours exceeding 40.0."""
    if hours_worked <= 40.0:
        gross = hours_worked * hourly_rate
    else:
        regular_pay = 40.0 * hourly_rate
        overtime_hours = hours_worked - 40.0
        overtime_pay = overtime_hours * (hourly_rate * overtime_multiplier)
        gross = regular_pay + overtime_pay
    return round(gross, 2)


def calculate_deductions(gross_pay: float, tax_rate: float = 0.18, retirement_rate: float = 0.05, health_insurance: float = 45.00) -> dict:
    """Calculates itemized payroll deductions and net take-home earnings."""
    income_tax = round(gross_pay * tax_rate, 2)
    retirement_401k = round(gross_pay * retirement_rate, 2)
    health_fee = round(health_insurance, 2)
    total_deductions = round(income_tax + retirement_401k + health_fee, 2)
    net_pay = round(gross_pay - total_deductions, 2)
    
    return {
        "income_tax": income_tax,
        "retirement_401k": retirement_401k,
        "health_insurance": health_fee,
        "total_deductions": total_deductions,
        "net_pay": net_pay
    }


def generate_payslip(employee_name: str, employee_id: str, hours_worked: float, hourly_rate: float, **deduction_options) -> dict:
    """Generates a complete consolidated employee payslip record."""
    gross_pay = calculate_gross_pay(hours_worked, hourly_rate)
    deductions = calculate_deductions(gross_pay, **deduction_options)
    
    return {
        "employee_name": employee_name,
        "employee_id": employee_id,
        "hours_worked": hours_worked,
        "hourly_rate": hourly_rate,
        "gross_pay": gross_pay,
        "deductions": deductions,
        "net_pay": deductions["net_pay"]
    }


# Test Execution
payslip = generate_payslip(
    employee_name="Marcus Vance",
    employee_id="EMP-4081",
    hours_worked=46.5,
    hourly_rate=45.00,
    retirement_rate=0.06
)

reg_hours = min(payslip["hours_worked"], 40.0)
ot_hours = max(payslip["hours_worked"] - 40.0, 0.0)
d = payslip["deductions"]

print("==================================================")
print("              APEX HR ENTERPRISE PAYSLIP          ")
print("==================================================")
print(f"Employee:         {payslip['employee_name']} (ID: {payslip['employee_id']})")
print(f"Hours Logged:     {payslip['hours_worked']:.2f} hrs ({reg_hours:.2f} reg + {ot_hours:.2f} OT)")
print(f"Hourly Base Rate: ${payslip['hourly_rate']:.2f}/hr")
print("--------------------------------------------------")
print(f"GROSS COMPENSATION: ${payslip['gross_pay']:,.2f}")
print("--------------------------------------------------")
print("PAYROLL DEDUCTIONS:")
print(f"- Income Tax (18%):  ${d['income_tax']:>8.2f}")
print(f"- 401(k) Plan (6%):  ${d['retirement_401k']:>8.2f}")
print(f"- Health Insurance:  ${d['health_insurance']:>8.2f}")
print(f"- Total Deductions:  ${d['total_deductions']:>8.2f}")
print("--------------------------------------------------")
print(f"NET TAKE-HOME PAY:  ${payslip['net_pay']:,.2f}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is returned by a Python function that executes without reaching a `return` statement?**
   - A) `0`
   - B) `False`
   - C) `None`
   - D) `""`

2. **Why is `def register_user(username, roles=[]):` dangerous in Python?**
   - A) The `roles` list is evaluated only once and shared across all future function invocations.
   - B) Lists cannot be passed into functions.
   - C) It produces an immediate `SyntaxError`.
   - D) The list is converted into a tuple.

3. **In the function signature `def audit(event, *flags, **metadata):`, what type does `flags` have inside the function?**
   - A) `list`
   - B) `tuple`
   - C) `dict`
   - D) `set`

<details>
<summary><b>View Answers</b></summary>
1: C (Python functions default to returning the singleton None object)<br>
2: A (Default parameter expressions are bound at definition time, making mutable defaults shared state)<br>
3: B (*args and *flags capture variable positional arguments as an immutable tuple)
</details>
