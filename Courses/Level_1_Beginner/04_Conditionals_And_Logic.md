# Lesson 4: Conditional Statements (`if`, `elif`, `else`)

Software becomes intelligent when it can make decisions. Conditional statements allow your program to evaluate dynamic data at runtime and execute specific branches of code depending on whether conditions are `True` or `False`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand control flow, execution branching, and Python's indentation rules.
2. Construct single-branch (`if`), two-branch (`if...else`), and multi-branch (`if...elif...else`) logic trees.
3. Master Python's concise **chained comparisons** (`650 <= score < 750`).
4. Implement nested conditionals and understand how to flatten them cleanly.
5. Write one-line **ternary conditional expressions**.
6. Use string membership operators (`in` and `not in`).
7. Identify and avoid common logical anti-patterns.

---

## 1. Python Block Structure & Indentation Rules

Unlike languages like C, Java, or JavaScript that use curly braces `{ ... }` to denote code blocks, **Python uses indentation (strictly 4 spaces)**.

```python
account_balance = 450.00
withdrawal_amount = 100.00

if withdrawal_amount <= account_balance:
    # Everything indented 4 spaces belongs to the 'if' block:
    print("Withdrawal approved!")
    account_balance -= withdrawal_amount
    print(f"Remaining Balance: ${account_balance:.2f}")

# Unindented code runs unconditionally after the block finishes:
print("Thank you for using Apex Banking.")
```

> [!CAUTION]
> **Indentation Rules**:
> - Always use 4 spaces per indentation level. Never mix tabs and spaces.
> - An `if` statement line **must** end with a colon (`:`).
> - An `if` block cannot be empty. If you need a temporary placeholder, use the `pass` keyword:
>   ```python
>   if is_maintenance_mode:
>       pass  # TODO: implement maintenance handling
>   ```

---

## 2. Multi-Way Branching: `if` - `elif` - `else`

- **`if`**: Evaluates the primary condition first.
- **`elif`** (*else-if*): Evaluated only if all preceding conditions were `False`. You can chain as many `elif` blocks as needed.
- **`else`**: The fallback catch-all block executed if **none** of the conditions evaluated to `True`.

```python
http_status_code = 404

if http_status_code == 200:
    status_category = "Success: OK"
elif http_status_code == 301:
    status_category = "Redirect: Moved Permanently"
elif http_status_code == 400:
    status_category = "Client Error: Bad Request"
elif http_status_code == 404:
    status_category = "Client Error: Resource Not Found"
elif http_status_code == 500:
    status_category = "Server Error: Internal Server Crash"
else:
    status_category = f"Unknown Status Code ({http_status_code})"

print(f"Response: {status_category}")
```

> [!NOTE]
> Python tests conditions sequentially from top to bottom. The moment **one** condition matches, its block runs, and Python immediately skips the rest of the `if-elif-else` construct.

---

## 3. Chained Comparisons & Nested Conditions

Python allows intuitive mathematical range checks without needing verbose `and` statements:

```python
applicant_age = 28

# Standard syntax in older languages:
# if applicant_age >= 18 and applicant_age <= 65:

# Pythonic Chained Comparison:
if 18 <= applicant_age <= 65:
    print("Applicant meets prime working-age eligibility criteria.")
```

### Nested Conditionals
You can nest conditional blocks inside other conditional blocks:

```python
has_valid_id = True
has_boarding_pass = True
is_security_cleared = False

if has_valid_id:
    if has_boarding_pass:
        if is_security_cleared:
            print("Passenger cleared for aircraft boarding. ✈️")
        else:
            print("❌ Access Denied: Security screening pending.")
    else:
        print("❌ Access Denied: Missing boarding pass.")
else:
    print("❌ Access Denied: Missing valid government ID.")
```

---

## 4. Ternary Conditional Expressions (One-Liners)

For simple value assignments based on a single condition, Python provides an elegant inline syntax:
`value_if_true if condition else value_if_false`

```python
cart_subtotal = 85.00
# Free shipping if cart is $50 or more, otherwise $7.95
shipping_fee = 0.0 if cart_subtotal >= 50.00 else 7.95

print(f"Shipping Fee: ${shipping_fee:.2f}")
```

---

## 5. String Membership Testing: `in` and `not in`

The `in` operator checks if a substring is contained within a string:

```python
email = input("Enter email address: ").strip().lower()

if "@" in email and "." in email:
    if "admin" in email:
        print("Administrative account detected.")
    else:
        print("Standard user account detected.")
else:
    print("❌ Invalid email format: missing '@' or '.' domain.")
```

---

## 6. Common Anti-Patterns to Avoid

### The "Truthy String" Bug:
```python
user_role = "editor"

# ❌ WRONG: "manager" is a non-empty string, which is ALWAYS True!
# if user_role == "admin" or "manager":  # Always evaluates to True!

# ✅ CORRECT:
if user_role == "admin" or user_role == "manager":
    print("Access granted to elevated panel.")
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_04_Conditionals_And_Logic.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_04_Conditionals_And_Logic.py):

```python
# Movie Ticket Dynamic Pricing Engine
customer_age = int(input("Enter customer age: "))
is_matinee = input("Is this a matinee screening? (yes/no): ").strip().lower() == "yes"

if customer_age < 5:
    base_price = 0.00
elif 5 <= customer_age <= 12:
    base_price = 8.50
elif 13 <= customer_age <= 64:
    base_price = 14.00
else:
    base_price = 10.00

# Apply $3 discount for matinee screenings on paid tickets:
if is_matinee and base_price > 0:
    final_price = base_price - 3.00
else:
    final_price = base_price

print(f"Ticket Price: ${final_price:.2f}")
```

---

## 📝 Quick Exercise: Commercial Loan & Credit Underwriting System

### 🏢 Real-Life Scenario
You are developing the core automated risk assessment engine for a commercial business lending fintech platform. The system evaluates loan applications based on business registration status, years of operation, credit score, annual revenue, and Debt-to-Income (DTI) ratio.

### 📋 Requirements
1. Capture and sanitize inputs:
   - `business_name`: Prompt with `"Enter business name: "`, format with `.strip().title()`.
   - `business_status`: Prompt with `"Enter entity status (active/pending/suspended): "`, format with `.strip().lower()`.
   - `years_in_business`: Prompt with `"Enter years in operation: "`, cast to `float`.
   - `credit_score`: Prompt with `"Enter principal credit score (300-850): "`, cast to `int`.
   - `annual_revenue`: Prompt with `"Enter annual revenue ($): "`, cast to `float`.
   - `monthly_debt`: Prompt with `"Enter total monthly debt payments ($): "`, cast to `float`.
2. Compute financial metrics:
   - `monthly_revenue = annual_revenue / 12.0`
   - `dti_ratio = (monthly_debt / monthly_revenue) * 100.0`
3. Multi-branch underwriting logic:
   - **Check 1**: If `business_status != "active"`:
     - `decision = "REJECTED: Business entity status is not active."`
     - `interest_rate = 0.0`
     - `max_credit_line = 0.0`
   - **Check 2**: Else if `years_in_business < 1.0`:
     - `decision = "REJECTED: Minimum 1.0 year of operational history required."`
     - `interest_rate = 0.0`
     - `max_credit_line = 0.0`
   - **Check 3 (Tier 1 Prime)**: Else if `credit_score >= 740` and `dti_ratio <= 30.0`:
     - `decision = "APPROVED: Tier 1 Prime Business Line of Credit"`
     - `interest_rate = 5.25`
     - `max_credit_line = annual_revenue * 0.25`
   - **Check 4 (Tier 2 Standard)**: Else if `650 <= credit_score < 740` and `dti_ratio <= 45.0`:
     - `decision = "APPROVED: Tier 2 Standard Commercial Facility"`
     - `interest_rate = 8.50`
     - `max_credit_line = annual_revenue * 0.15`
   - **Check 5 (High Risk)**: Else if `credit_score < 600` or `dti_ratio > 50.0`:
     - `decision = "REJECTED: Subprime credit score or excessive debt burden."`
     - `interest_rate = 0.0`
     - `max_credit_line = 0.0`
   - **Check 6 (Fallback)**: Else:
     - `decision = "MANUAL REVIEW: Application flagged for Senior Committee review."`
     - `interest_rate = 11.00`
     - `max_credit_line = annual_revenue * 0.08`
4. Output the structured underwriting report.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 through 4 (variables, primitives, `input()`, `int()`, `float()`, string methods, arithmetic, comparison, logical `and`/`or`/`not`, `if`/`elif`/`else`, nested conditionals, f-strings, and `print()`). Do **not** use loops, lists, or functions.

### 🎯 Sample Interactive Run
```text
Enter business name:   apex logistics llc   
Enter entity status (active/pending/suspended): active
Enter years in operation: 3.5
Enter principal credit score (300-850): 760
Enter annual revenue ($): 480000.00
Enter total monthly debt payments ($): 6000.00

==================================================
        COMMERCIAL LOAN UNDERWRITING REPORT       
==================================================
Applicant:        Apex Logistics Llc
Entity Status:    active | Experience: 3.5 yrs
Credit Score:     760
Annual Revenue:   $480,000.00 (Monthly: $40,000.00)
Monthly Debt:     $6,000.00
Calculated DTI:   15.00%
--------------------------------------------------
DECISION:         APPROVED: Tier 1 Prime Business Line of Credit
Interest Rate:    5.25%
Max Credit Line:  $120,000.00
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Capture and sanitize applicant inputs
business_name = input("Enter business name: ").strip().title()
business_status = input("Enter entity status (active/pending/suspended): ").strip().lower()
years_in_business = float(input("Enter years in operation: "))
credit_score = int(input("Enter principal credit score (300-850): "))
annual_revenue = float(input("Enter annual revenue ($): "))
monthly_debt = float(input("Enter total monthly debt payments ($): "))

# 2. Compute financial ratios
monthly_revenue = annual_revenue / 12.0
dti_ratio = (monthly_debt / monthly_revenue) * 100.0

# 3. Multi-branch underwriting logic
if business_status != "active":
    decision = "REJECTED: Business entity status is not active."
    interest_rate = 0.0
    max_credit_line = 0.0
elif years_in_business < 1.0:
    decision = "REJECTED: Minimum 1.0 year of operational history required."
    interest_rate = 0.0
    max_credit_line = 0.0
elif credit_score >= 740 and dti_ratio <= 30.0:
    decision = "APPROVED: Tier 1 Prime Business Line of Credit"
    interest_rate = 5.25
    max_credit_line = annual_revenue * 0.25
elif 650 <= credit_score < 740 and dti_ratio <= 45.0:
    decision = "APPROVED: Tier 2 Standard Commercial Facility"
    interest_rate = 8.50
    max_credit_line = annual_revenue * 0.15
elif credit_score < 600 or dti_ratio > 50.0:
    decision = "REJECTED: Subprime credit score or excessive debt burden."
    interest_rate = 0.0
    max_credit_line = 0.0
else:
    decision = "MANUAL REVIEW: Application flagged for Senior Committee review."
    interest_rate = 11.00
    max_credit_line = annual_revenue * 0.08

# 4. Formatted underwriting report
print("\n==================================================")
print("        COMMERCIAL LOAN UNDERWRITING REPORT       ")
print("==================================================")
print(f"Applicant:        {business_name}")
print(f"Entity Status:    {business_status} | Experience: {years_in_business:.1f} yrs")
print(f"Credit Score:     {credit_score}")
print(f"Annual Revenue:   ${annual_revenue:,.2f} (Monthly: ${monthly_revenue:,.2f})")
print(f"Monthly Debt:     ${monthly_debt:,.2f}")
print(f"Calculated DTI:   {dti_ratio:.2f}%")
print("--------------------------------------------------")
print(f"DECISION:         {decision}")
print(f"Interest Rate:    {interest_rate:.2f}%")
print(f"Max Credit Line:  ${max_credit_line:,.2f}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is printed by the following code?**
   ```python
   score = 85
   if score >= 90:
       print("A")
   elif score >= 80:
       print("B")
   elif score >= 70:
       print("C")
   else:
       print("D")
   ```
   - A) `B` and `C`
   - B) `B`
   - C) `A`
   - D) `C`

2. **What does the expression `"python" in "Intro to Python Programming".lower()` evaluate to?**
   - A) `False`
   - B) `True`
   - C) `TypeError`
   - D) `None`

3. **Why is `if role == "guest" or "trial":` a bug in Python?**
   - A) `"trial"` is evaluated as a standalone boolean and is always truthy.
   - B) Python does not allow the `or` keyword inside `if` statements.
   - C) Strings cannot be compared with `==`.
   - D) It produces a `SyntaxError`.

<details>
<summary><b>View Answers</b></summary>
1: B (Execution stops immediately after the first matching branch: score >= 80)<br>
2: B (After lowercasing, "python" is indeed a substring)<br>
3: A (Non-empty string "trial" is always True, causing the condition to always succeed)
</details>
