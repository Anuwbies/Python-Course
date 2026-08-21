# Lesson 4: Control Flow: Conditionals, Branching & Decision Logic

Real-world computer programs are not linear scripts; they make intelligent decisions based on runtime state. In this lesson, you will master conditional branching using `if`, `elif`, `else`, ternary conditional expressions, and membership testing.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Direct program execution branches using `if`, `elif`, and `else` blocks.
2. Structure robust nested conditional logic without spaghetti code.
3. Write clean, idiomatic one-line **Ternary Expressions** (`value if condition else fallback`).
4. Perform collection and substring membership testing with `in` and `not in`.
5. Identify and avoid common boolean conditional anti-patterns.

---

## 1. The `if`, `elif`, `else` Architecture

Python uses indentation (standard 4 spaces) to define execution blocks:

```python
credit_score = 720

if credit_score >= 750:
    tier = "Platinum Elite"
    rate_discount = 0.015
elif credit_score >= 680:
    tier = "Prime Gold"
    rate_discount = 0.0075
elif credit_score >= 620:
    tier = "Standard"
    rate_discount = 0.0
else:
    tier = "Subprime"
    rate_discount = -0.02

print(f"Customer Tier: {tier} | Rate Adjustment: {rate_discount * 100:+.2f}%")
```

---

## 2. Nested Conditionals

When a secondary decision depends strictly on a primary condition being met, conditions can be nested:

```python
has_valid_license = True
blood_alcohol_content = 0.00

if has_valid_license:
    if blood_alcohol_content == 0.00:
        print("✅ Cleared to operate commercial heavy transport.")
    else:
        print("❌ Prohibited: Zero-tolerance BAC policy violated.")
else:
    print("❌ Prohibited: Valid operator license required.")
```

---

## 3. Ternary Conditional Operator (Inline `if-else`)

For simple variable assignments based on a condition, Python supports an inline ternary expression:

$$\text{result} = \text{value\_if\_true} \textbf{ if } \text{condition} \textbf{ else } \text{value\_if\_false}$$

```python
account_balance = 450.00
withdrawal = 500.00

# Concise inline assignment:
status_message = "APPROVED" if account_balance >= withdrawal else "DENIED - INSUFFICIENT FUNDS"
print(f"Transaction Status: {status_message}")
```

---

## 4. Membership Testing: `in` and `not in`

The `in` and `not in` operators test whether a substring exists within a string, or an item exists within a collection:

```python
email_address = "admin@datacenter.internal.net"

# Substring containment check:
if "@" in email_address and email_address.endswith(".net"):
    print("Valid internal network address format.")

# Checking against unauthorized domains:
blocked_providers = ("spammail.com", "throwaway.io", "tempinbox.org")
user_domain = "tempinbox.org"

if user_domain in blocked_providers:
    print("❌ Registration blocked: Disposable email provider detected.")
```

---

---

## 5. Structural Pattern Matching (`match` / `case`) (Python 3.10+)

For complex multi-branch routing, Python 3.10 introduced **Structural Pattern Matching** (`match`/`case`), which is far more expressive and safer than traditional `switch/case` in C++ or Java.

```python
http_status_code = 404

match http_status_code:
    case 200 | 201: # OR pattern
        response = "OK / Resource Created"
    case 400:
        response = "Bad Request: Client Error"
    case 401 | 403:
        response = "Unauthorized / Forbidden Access"
    case 404:
        response = "Not Found: Resource does not exist"
    case 500 | 502 | 503:
        response = "Server Gateway Error"
    case _: # Wildcard pattern (default catch-all like 'else')
        response = f"Unknown Status Code: {http_status_code}"

print(f"HTTP Status: {response}")
```

### Pattern Matching with Guard Clauses (`if` inside `case`)
You can attach guards to case blocks to inspect values conditionally:

```python
transaction = {"type": "WITHDRAWAL", "amount": 15000.0, "is_flagged": True}

match transaction:
    case {"type": "WITHDRAWAL", "amount": amt} if amt > 10000.0 or transaction.get("is_flagged"):
        print(f"🚨 FRAUD ALERT: High-value or flagged withdrawal of ${amt:,.2f}")
    case {"type": "WITHDRAWAL", "amount": amt}:
        print(f"Standard withdrawal of ${amt:,.2f} processed.")
    case {"type": "DEPOSIT", "amount": amt}:
        print(f"Deposit of ${amt:,.2f} credited.")
    case _:
        print("Invalid transaction payload format.")
```

---

## 6. Common Boolean Anti-Patterns to Avoid

### ❌ The "Truthiness of Non-Empty Strings" Bug
```python
user_role = "operator"

# ❌ WRONG: "manager" evaluates as a non-empty string which is ALWAYS True!
if user_role == "admin" or "manager":  # Bug: always evaluates to True!
    print("Access granted.")

# ✅ CORRECT:
if user_role == "admin" or user_role == "manager":
    print("Access granted.")

# ✅ EVEN BETTER (using 'in'):
if user_role in ("admin", "manager"):
    print("Access granted.")
```

---

## 7. Chained Comparison Mechanics

Python natively supports **chained comparisons** like in mathematical algebra:

```python
score = 85

# In Python, this is evaluated as: (70 <= score) and (score <= 90)
# WITHOUT evaluating 'score' multiple times:
if 70 <= score <= 90:
    print("Score is in the B Grade range.")
```

---

## 💻 Code Example & Reference

The following real-life program models an **Automated Mortgage & Commercial Loan Risk Assessment Engine**, utilizing all conditional flow concepts from this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Commercial Mortgage Underwriting Risk Engine
# =====================================================================

print("=" * 65)
print(f"{'🏦 COMMERCIAL MORTGAGE RISK & UNDERWRITING ENGINE':^65}")
print("=" * 65)

# 1. Inputs & Sanitization (Lessons 1 & 2)
applicant_name = input("Enter Primary Borrower Name: ").strip().title()
employment_type = input("Enter Employment (W2 / Self-Employed / Retired): ").strip().upper()
annual_income = float(input("Enter Verified Gross Annual Income ($): "))
monthly_debt = float(input("Enter Total Monthly Debt Obligations ($): "))
requested_loan = float(input("Enter Requested Loan Principal ($): "))
credit_score = int(input("Enter Credit Score (300-850): "))
property_type = input("Property Type (Residential / Commercial / Industrial): ").strip().title()

# 2. Arithmetic & Financial Debt-to-Income (DTI) Ratios (Lessons 1, 2, 3)
monthly_income = annual_income / 12.0
debt_to_income_ratio = (monthly_debt / monthly_income) * 100.0
loan_to_income_ratio = requested_loan / annual_income

# 3. Multi-branch Conditionals & Nested Underwriting Rules (Lesson 4)
APPROVED_PROPERTY_TYPES = ("Residential", "Commercial", "Industrial")

if property_type not in APPROVED_PROPERTY_TYPES:
    decision = "REJECTED"
    underwriting_notes = f"Property type '{property_type}' is outside our charter."
    final_interest_rate = 0.0
else:
    # Credit Score & DTI Verification Matrix
    if credit_score >= 760 and debt_to_income_ratio <= 36.0:
        decision = "APPROVED (TIER 1 PRIME)"
        base_rate = 6.25
        underwriting_notes = "Optimal credit profile; automatic fast-track approval."
    elif credit_score >= 680 and debt_to_income_ratio <= 43.0:
        decision = "APPROVED (TIER 2 STANDARD)"
        base_rate = 6.95
        underwriting_notes = "Acceptable risk profile; standard closing conditions."
    elif credit_score >= 620 and debt_to_income_ratio <= 50.0:
        # Nested employment stability check
        if employment_type in ("W2", "RETIRED"):
            decision = "CONDITIONAL APPROVAL"
            base_rate = 7.85
            underwriting_notes = "Requires 12 months verified cash reserves and manual audit."
        else:
            decision = "REJECTED"
            base_rate = 0.0
            underwriting_notes = "Self-employed applicants with <680 score require DTI under 40%."
    else:
        decision = "REJECTED"
        base_rate = 0.0
        underwriting_notes = "Credit score below underwriting threshold or excessive DTI."

    # Ternary rate adjustment based on property class
    rate_adjustment = 0.50 if property_type == "Commercial" else (0.75 if property_type == "Industrial" else 0.00)
    final_interest_rate = base_rate + rate_adjustment if decision.startswith("APPROV") or decision.startswith("COND") else 0.0

# 4. Formatted Underwriting Report Output (Lesson 1)
print("\n" + "=" * 65)
print(f"{'MORTGAGE UNDERWRITING DECISION':^65}")
print("=" * 65)
print(f"{'Borrower Name:':<30} {applicant_name}")
print(f"{'Employment / Property:':<30} {employment_type} | {property_type}")
print(f"{'Debt-to-Income (DTI):':<30} {debt_to_income_ratio:.2f}%")
print(f"{'Credit Score:':<30} {credit_score} pts")
print("-" * 65)
print(f"{'FINAL DECISION:':<30} {decision}")
print(f"{'Assigned Interest Rate:':<30} {f'{final_interest_rate:.2f}%' if final_interest_rate > 0 else 'N/A'}")
print(f"{'Underwriting Notes:':<30} {underwriting_notes}")
print("=" * 65)
```

### 🔍 Code Explanation:
- **Membership Validation**: `property_type not in APPROVED_PROPERTY_TYPES` verifies inputs immediately before evaluating downstream numbers.
- **Hierarchical `if-elif-else`**: Branches evaluate risk bands from highest credit / lowest debt to higher risk thresholds.
- **Nested Decisions**: Within the borderline credit band (`620-679`), an inner branch checks `employment_type` stability.
- **Ternary Operator**: Computes commercial asset surcharges in a concise inline expression.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master branching logic, nested decisions, ternary operators, string membership checks, and structural pattern matching:

---

### 🟢 Tier 1: Basic Conditionals & Ternary Expressions (Exercises 1–3)

#### 🔹 Exercise 1: Traffic Signal Controller
* **Goal**: Given `signal_color = "red"`.
* **Requirement**: Print `"STOP"` if red, `"CAUTION"` if yellow, `"GO"` if green, or `"SIGNAL MALFUNCTION"` otherwise.

#### 🔹 Exercise 2: Inline Ternary Discount Applier
* **Goal**: Given `is_member = True` and `price = 100.0`.
* **Requirement**: Use a one-line ternary expression to compute `final_price = price * 0.90 if is_member else price`. Print `f"Final Price: ${final_price:.2f}"`.

#### 🔹 Exercise 3: Pass/Fail Grade Boundary
* **Goal**: Prompt for test score (0-100).
* **Requirement**: If `score >= 60`, print `"PASSED"`, otherwise `"FAILED"`.

---

### 🟡 Tier 2: Multi-Branch & String Containment (Exercises 4–6)

#### 🔹 Exercise 4: Academic Letter Grade Classifier
* **Goal**: Given numeric grade `score` (0–100).
* **Scale**: `90-100` $\rightarrow$ `"A"`, `80-89` $\rightarrow$ `"B"`, `70-79` $\rightarrow$ `"C"`, `60-69` $\rightarrow$ `"D"`, `<60` $\rightarrow$ `"F"`.
* **Requirement**: Use chained comparisons (`90 <= score <= 100`) in an `if-elif-else` block.

#### 🔹 Exercise 5: Malicious URL Protocol & Domain Inspector
* **Goal**: Prompt for a URL string.
* **Requirement**: Check if it starts with `"https://"` and does NOT contain `"phishing"` or `"tracker"`. Print safety verdict.

#### 🔹 Exercise 6: Leap Year Evaluator
* **Goal**: Prompt for a year integer (e.g. `2024`).
* **Rule**: A year is a leap year if `(year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)`.
* **Requirement**: Print whether the year is a leap year.

---

### 🟠 Tier 3: Nested Decisions & Pattern Matching (Exercises 7–9)

#### 🔹 Exercise 7: ATM Cash Withdrawal Processor
* **Goal**: Given `balance = 500.0`, `daily_limit = 300.0`.
* **Input**: Prompt for `withdraw_amount`.
* **Rules**: Check if `withdraw_amount % 20 == 0` (only $20 bills). Then check `withdraw_amount <= daily_limit`. Then check `withdraw_amount <= balance`. Provide precise rejection reasons for each failure point.

#### 🔹 Exercise 8: Structural `match/case` REST API Router
* **Goal**: Given `method = "POST"` and `endpoint = "/api/v1/users"`.
* **Requirement**: Use `match (method, endpoint):` to handle `("GET", "/api/v1/users")`, `("POST", "/api/v1/users")`, and wildcard `_`.

#### 🔹 Exercise 9: Server Health Tier Classifier with Guards
* **Goal**: Given a dictionary `telemetry = {"cpu": 95, "mem": 88, "disk": 70}`.
* **Requirement**: Use `match/case` with guard clauses to classify `CRITICAL` (any metric > 90), `WARNING` (any metric > 75), or `HEALTHY`.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Hospital Emergency Triage Badge Classifier
* **Goal**: Take patient vitals ($SpO_2$, HR, Pain scale, Symptoms), classify ESI severity Level 1 to 4, and compute estimated wait times.

---

## 📝 Quick Exercise: Hospital Emergency Department Triage Classifier

### 🏢 Real-Life Scenario
You are building the patient intake triage sorting system for a busy metropolitan emergency department. When a patient arrives, the triage nurse inputs vital statistics (heart rate, blood oxygen saturation $SpO_2$, pain scale, and chief complaint keywords). The system determines the Emergency Severity Index (ESI Level 1 to 4) and routes the patient to Resuscitation, Trauma, Urgent Care, or General Waiting.

### 📋 Requirements
1. Capture and sanitize patient intake data:
   - `patient_name`: Formatted with `.strip().title()`
   - `patient_age`: Cast to `int`
   - `heart_rate_bpm`: Cast to `int`
   - `spo2_percentage`: Cast to `float` (Blood oxygen percentage, e.g. `91.5`)
   - `pain_level`: Cast to `int` (scale 1-10)
   - `symptoms`: Formatted with `.strip().lower()`
2. Triage Classification Rules (Hierarchical Conditionals):
   - **Level 1 (CRITICAL - RESUSCITATION)**: If `spo2_percentage < 88.0` OR `heart_rate_bpm > 140` OR (`"unresponsive"` in `symptoms` or `"cardiac"` in `symptoms`).
   - **Level 2 (EMERGENT - TRAUMA BAY)**: Else if `spo2_percentage <= 92.0` OR `heart_rate_bpm >= 120` OR (`"chest pain"` in `symptoms` or `"stroke"` in `symptoms`).
   - **Level 3 (URGENT - ACUTE CARE)**: Else if `pain_level >= 7` OR `patient_age >= 75`.
   - **Level 4 (STANDARD - GENERAL CLINIC)**: All other stable cases.
3. Compute estimated triage wait time using a ternary expression:
   - `0 minutes` if Level 1 or Level 2, else `15 minutes` if Level 3, else `60 minutes`.
4. Output the official triage intake badge.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1, 2, 3, and 4** (variables, types, input sanitization, casting, arithmetic, compound boolean logic, `in` membership, `if-elif-else`, ternary, and f-string formatting).

### 🎯 Expected Output
*(Assuming the user inputs: Name: `  sarah connor  `, Age: `45`, Heart Rate: `125`, SpO2: `94.0`, Pain: `8`, Symptoms: `severe chest pain after exercise`)*

```text
Enter Patient Name:   sarah connor  
Enter Patient Age: 45
Enter Resting Heart Rate (BPM): 125
Enter Blood Oxygen SpO2 (%): 94.0
Enter Pain Scale (1-10): 8
Enter Chief Symptoms: severe chest pain after exercise

==================================================
           EMERGENCY TRIAGE INTAKE PASS           
==================================================
Patient:       Sarah Connor (Age: 45)
Vitals:        HR: 125 BPM | SpO2: 94.0% | Pain: 8/10
Symptoms:      severe chest pain after exercise
--------------------------------------------------
TRIAGE LEVEL:  LEVEL 2 - EMERGENT
ASSIGNED WARD: TRAUMA BAY / RAPID ACUTE
EST. WAIT TIME:0 mins (IMMEDIATE DOCTOR EVALUATION)
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Hospital & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Emergency Triage Intake Pass
# =====================================================================
patient_name = input("Enter Patient Name: ").strip().title()
patient_age = int(input("Enter Patient Age: "))
heart_rate_bpm = int(input("Enter Resting Heart Rate (BPM): "))
spo2_percentage = float(input("Enter Blood Oxygen SpO2 (%): "))
pain_level = int(input("Enter Pain Scale (1-10): "))
symptoms = input("Enter Chief Symptoms: ").strip().lower()

if (spo2_percentage < 88.0) or (heart_rate_bpm > 140) or ("unresponsive" in symptoms or "cardiac" in symptoms):
    triage_level = "LEVEL 1 - CRITICAL"
    assigned_ward = "RESUSCITATION UNIT"
    est_wait = "0 mins (IMMEDIATE RESUSCITATION)"
elif (spo2_percentage <= 92.0) or (heart_rate_bpm >= 120) or ("chest pain" in symptoms or "stroke" in symptoms):
    triage_level = "LEVEL 2 - EMERGENT"
    assigned_ward = "TRAUMA BAY / RAPID ACUTE"
    est_wait = "0 mins (IMMEDIATE DOCTOR EVALUATION)"
elif (pain_level >= 7) or (patient_age >= 75):
    triage_level = "LEVEL 3 - URGENT"
    assigned_ward = "ACUTE FAST TRACK"
    est_wait = "15 mins"
else:
    triage_level = "LEVEL 4 - STANDARD"
    assigned_ward = "GENERAL CLINIC WAITING"
    est_wait = "60 mins"

print("\n==================================================")
print("           EMERGENCY TRIAGE INTAKE PASS           ")
print("==================================================")
print(f"Patient:       {patient_name} (Age: {patient_age})")
print(f"Vitals:        HR: {heart_rate_bpm} BPM | SpO2: {spo2_percentage:.1f}% | Pain: {pain_level}/10")
print(f"Symptoms:      {symptoms}")
print("--------------------------------------------------")
print(f"TRIAGE LEVEL:  {triage_level}")
print(f"ASSIGNED WARD: {assigned_ward}")
print(f"EST. WAIT TIME:{est_wait}")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
color = "red"
if color == "red": print("STOP")
elif color == "yellow": print("CAUTION")
elif color == "green": print("GO")
else: print("SIGNAL MALFUNCTION")

# Ex 2:
is_member, price = True, 100.0
final_p = price * 0.90 if is_member else price
print(f"Final Price: ${final_p:.2f}")

# Ex 3:
score = int(input("Score: "))
print("PASSED" if score >= 60 else "FAILED")

# Ex 4:
s = 85
if 90 <= s <= 100: grade = "A"
elif 80 <= s < 90: grade = "B"
elif 70 <= s < 80: grade = "C"
elif 60 <= s < 70: grade = "D"
else: grade = "F"
print(f"Grade: {grade}")

# Ex 5:
url = input("URL: ").strip().lower()
is_safe = url.startswith("https://") and ("phishing" not in url) and ("tracker" not in url)
print(f"Safe: {is_safe}")

# Ex 6:
year = int(input("Year: "))
is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
print(f"Leap Year: {is_leap}")

# Ex 7:
bal, limit, amt = 500.0, 300.0, float(input("Withdrawal: "))
if amt % 20 != 0: print("Must be multiples of $20")
elif amt > limit: print("Exceeds daily limit")
elif amt > bal: print("Insufficient funds")
else: print(f"Dispensing ${amt:.2f}")

# Ex 8:
method, ep = "POST", "/api/v1/users"
match (method, ep):
    case ("GET", "/api/v1/users"): print("List users")
    case ("POST", "/api/v1/users"): print("Create user")
    case _: print("404 Route Not Found")

# Ex 9:
t = {"cpu": 95, "mem": 88, "disk": 70}
match t:
    case _ if any(v > 90 for v in t.values()): print("CRITICAL")
    case _ if any(v > 75 for v in t.values()): print("WARNING")
    case _: print("HEALTHY")
```
</details>
