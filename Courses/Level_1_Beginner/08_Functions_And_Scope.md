# Lesson 8: Functions, Scope & Modular Program Design

In professional software development, writing long, monolithic scripts creates code that is difficult to read, debug, test, and reuse. **Functions** are the fundamental building block of modular engineering—they encapsulate specific tasks into reusable, parameterized units. In this lesson, you will master function definitions, argument modes (`*args`, `**kwargs`), return values, and variable scope (the LEGB rule).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Define and call functions using `def`, parameters, and `return` statements.
2. Apply modern Python **Type Annotations** (`param: type -> return_type`) and Google-style **Docstrings**.
3. Utilize Default Parameters and avoid the infamous **Mutable Default Argument Trap**.
4. Pass arbitrary arguments using `*args` (positional) and `**kwargs` (keyword).
5. Understand the **LEGB Scope Rule** (Local, Enclosing, Global, Built-in) and the `global` keyword.
6. Write pure, testable functions following Single Responsibility principles.

---

## 1. Defining Functions & Return Values

A function is declared using the `def` keyword, followed by parameter names and an indented body:

```python
def calculate_tax(subtotal: float, tax_rate: float = 0.08) -> float:
    """Calculates tax on a given subtotal.
    
    Args:
        subtotal (float): The base cost before tax.
        tax_rate (float): The fractional tax rate (default is 8%).
        
    Returns:
        float: The calculated tax amount rounded to 2 decimal places.
    """
    return round(subtotal * tax_rate, 2)

# Calling with positional and default arguments:
print(calculate_tax(100.0))          # 8.0 (uses default 0.08)
print(calculate_tax(100.0, 0.15))    # 15.0 (overrides default)
```

---

## 2. The Mutable Default Argument Trap

> [!CAUTION]
> **Never use a mutable object (`list`, `dict`, `set`) as a default parameter value!**
> In Python, default parameter objects are evaluated **once when the function is defined**, not every time it is called.

```python
# ❌ INCORRECT: All callers share the SAME list in memory!
def add_user_bad(username: str, user_list: list = []):
    user_list.append(username)
    return user_list

print(add_user_bad("Alice")) # ['Alice']
print(add_user_bad("Bob"))   # ['Alice', 'Bob'] (Accidentally shared state!)

# ✅ CORRECT: Use None as default and initialize inside:
def add_user_good(username: str, user_list: list = None):
    if user_list is None:
        user_list = []
    user_list.append(username)
    return user_list

print(add_user_good("Alice")) # ['Alice']
print(add_user_good("Bob"))   # ['Bob'] (Isolated clean lists!)
```

---

## 3. Flexible Arguments: `*args` and `**kwargs`

- **`*args`**: Captures any number of positional arguments into a `tuple`.
- **`**kwargs`**: Captures any number of named/keyword arguments into a `dict`.

```python
def log_telemetry_event(event_name: str, *tags: str, **metadata: any) -> None:
    print(f"EVENT: {event_name}")
    print(f"  Tags: {tags}")
    print(f"  Metadata Attributes:")
    for key, value in metadata.items():
        print(f"    - {key}: {value}")

# Invoking with arbitrary arguments:
log_telemetry_event(
    "USER_LOGIN", 
    "security", "audit", "prod-auth", # *args
    ip="192.168.1.10", region="us-west", latency_ms=42.5 # **kwargs
)
```

---

## 4. Variable Scope & The LEGB Rule

Python searches for variable names in four cascading scopes (**LEGB**):

1. **L**ocal: Inside the currently executing function.
2. **E**nclosing: Inside any enclosing/nested outer functions.
3. **G**lobal: At the top level of the current module file.
4. **B**uilt-in: Python's built-in namespace (`print`, `len`, `int`, `range`).

```python
system_mode = "PRODUCTION" # Global variable

def execute_operation():
    local_worker_id = "WRK-99" # Local variable
    print(f"Executing in {system_mode} by {local_worker_id}")

execute_operation()
# print(local_worker_id) # ❌ NameError: 'local_worker_id' is not accessible in global scope!
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Financial Loan Amortization & Multi-Option Mortgage Engine**, combining all function design and scope mechanics taught in this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Multi-Product Mortgage & Amortization Engine
# =====================================================================

GLOBAL_BANK_CHARTER = "Apex Federal Financial Services" # Global constant

def calculate_monthly_payment(
    principal: float, 
    annual_interest_rate: float, 
    term_years: int = 30
) -> float:
    """Calculates fixed monthly loan payment using standard amortization formula.
    
    Formula: M = P * [ r(1+r)^n ] / [ (1+r)^n - 1 ]
    """
    if annual_interest_rate <= 0:
        return principal / (term_years * 12)
        
    monthly_rate = (annual_interest_rate / 100.0) / 12.0
    total_payments = term_years * 12
    
    factor = (1.0 + monthly_rate) ** total_payments
    monthly_payment = principal * (monthly_rate * factor) / (factor - 1.0)
    return round(monthly_payment, 2)

def generate_loan_summary(
    borrower_name: str,
    principal: float,
    rate: float,
    term_years: int = 30,
    *insurance_riders: str,
    **fee_overrides: float
) -> dict:
    """Generates complete underwriting summary including fees and insurance."""
    base_monthly = calculate_monthly_payment(principal, rate, term_years)
    total_repayment = base_monthly * term_years * 12
    total_interest = total_repayment - principal
    
    # Calculate variable fee overrides (*kwargs)
    origination_fee = fee_overrides.get("origination_fee", principal * 0.01)
    appraisal_fee = fee_overrides.get("appraisal_fee", 550.00)
    closing_costs = origination_fee + appraisal_fee + sum(fee_overrides.values()) - (origination_fee + appraisal_fee if "origination_fee" in fee_overrides or "appraisal_fee" in fee_overrides else 0)
    
    return {
        "institution": GLOBAL_BANK_CHARTER,
        "borrower": borrower_name,
        "principal": principal,
        "annual_rate": rate,
        "term_years": term_years,
        "monthly_principal_interest": base_monthly,
        "total_interest_lifetime": total_interest,
        "total_closing_costs": closing_costs,
        "riders": insurance_riders,
    }

def print_loan_schedule(loan_details: dict) -> None:
    """Formats and prints the financial loan disclosures."""
    print("\n" + "=" * 65)
    print(f"{loan_details['institution']:^65}")
    print(f"{'MORTGAGE LOAN DISCLOSURE SCHEDULE':^65}")
    print("=" * 65)
    print(f"{'Borrower Name:':<32} {loan_details['borrower']}")
    print(f"{'Loan Principal:':<32} ${loan_details['principal']:,.2f}")
    print(f"{'Annual Interest Rate:':<32} {loan_details['annual_rate']:.2f}%")
    print(f"{'Loan Duration:':<32} {loan_details['term_years']} Years ({loan_details['term_years'] * 12} Months)")
    print("-" * 65)
    print(f"{'MONTHLY PRINCIPAL & INTEREST:':<32} ${loan_details['monthly_principal_interest']:,.2f}")
    print(f"{'Total Interest Over Life of Loan:':<32} ${loan_details['total_interest_lifetime']:,.2f}")
    print(f"{'Total Estimated Closing Costs:':<32} ${loan_details['total_closing_costs']:,.2f}")
    print("-" * 65)
    print(f"Attached Policy Riders ({len(loan_details['riders'])}):")
    for rider in loan_details['riders']:
        print(f"  ✓ {rider}")
    print("=" * 65)

# Executing loan calculations
applicant_loan = generate_loan_summary(
    "Eleanor Vance",
    450_000.00,
    6.75,
    30,
    "Flood Hazard Protection", "Title Loss Indemnity", "Mortgage Default Insurance", # *args
    origination_fee=3500.00, appraisal_fee=600.00, title_search=350.00 # **kwargs
)

print_loan_schedule(applicant_loan)
```

### 🔍 Code Explanation:
- **Modular Functions**: Calculations are broken down into discrete single-responsibility functions (`calculate_monthly_payment`, `generate_loan_summary`, `print_loan_schedule`).
- **Type Hints & Docstrings**: Every parameter and return value is typed and documented with formal docstrings.
- **Default Parameters**: `term_years: int = 30` provides an intuitive default while permitting custom terms (e.g. 15 years).
- **`*args` & `**kwargs`**: `*insurance_riders` gathers variable policy add-ons; `**fee_overrides` collects arbitrary closing fees.

---

## 📝 Quick Exercise: Cloud VM Instance Pricing & Quota Management Utility

### 🏢 Real-Life Scenario
You are developing the backend resource provisioning and cost estimation utility for a cloud infrastructure provider (such as AWS EC2 or Google Cloud Compute). The utility provides modular functions to estimate instance running costs, check resource quotas against team limits, and format resource provisioning invoices.

### 📋 Requirements
1. **Define `calculate_instance_cost` function**:
   - Signature: `def calculate_instance_cost(instance_type: str, hours: float, is_spot_instance: bool = False) -> float`
   - Hourly baseline rates dictionary:
     `RATES = {"t3.micro": 0.0104, "t3.medium": 0.0416, "c5.xlarge": 0.1700, "r5.2xlarge": 0.5040}`
   - Look up the rate (default to `0.05` if unknown).
   - If `is_spot_instance` is `True`, apply a `70%` discount (`rate * 0.30`).
   - Return total cost rounded to 4 decimal places.
2. **Define `verify_quota_limits` function**:
   - Signature: `def verify_quota_limits(requested_cores: int, requested_ram_gb: float, max_cores: int = 64, max_ram_gb: float = 256.0) -> tuple[bool, str]`
   - If `requested_cores > max_cores`: Return `False, f"Exceeded CPU quota limit of {max_cores} cores"`.
   - If `requested_ram_gb > max_ram_gb`: Return `False, f"Exceeded RAM quota limit of {max_ram_gb} GB"`.
   - Otherwise: Return `True, "Within assigned resource quota"`.
3. **Define `generate_fleet_report` function**:
   - Accepts `team_name: str`, `*instance_list: tuple`, and `**config_flags: any`.
   - Calculates the fleet total cost and quota status.
4. Execute the functions with sample cloud deployment data and output the formatted report.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1 through 8** (variables, types, arithmetic, compound conditionals, loops, lists, tuples, dicts, functions, default args, `*args`, `**kwargs`, type hints, and f-strings).

### 🎯 Expected Output
```text
==================================================
       CLOUD FLEET PROVISIONING ESTIMATOR         
==================================================
Team:             Data Science AI Lab
Instances Active: 3 nodes
Total CPU Cores:  24 / 64 cores
Total RAM:        96.0 / 256.0 GB
Quota Clearance:  ✅ Within assigned resource quota
--------------------------------------------------
INSTANCE BREAKDOWN:
  - Node #1 [c5.xlarge]:   720.0 hrs (On-Demand) -> $122.4000
  - Node #2 [c5.xlarge]:   720.0 hrs (Spot 70% off) -> $36.7200
  - Node #3 [r5.2xlarge]:  360.0 hrs (On-Demand) -> $181.4400
--------------------------------------------------
TOTAL ESTIMATED FLEET COST: $340.56
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Modular Functions (Lessons 1-8)
def calculate_instance_cost(instance_type: str, hours: float, is_spot_instance: bool = False) -> float:
    """Calculates VM run cost based on instance type and spot pricing."""
    rates = {
        "t3.micro": 0.0104,
        "t3.medium": 0.0416,
        "c5.xlarge": 0.1700,
        "r5.2xlarge": 0.5040
    }
    hourly_rate = rates.get(instance_type, 0.05)
    if is_spot_instance:
        hourly_rate *= 0.30 # 70% discount
    return round(hourly_rate * hours, 4)

def verify_quota_limits(
    requested_cores: int, 
    requested_ram_gb: float, 
    max_cores: int = 64, 
    max_ram_gb: float = 256.0
) -> tuple[bool, str]:
    """Verifies that requested computing capacity is within organizational limits."""
    if requested_cores > max_cores:
        return False, f"Exceeded CPU quota limit of {max_cores} cores"
    if requested_ram_gb > max_ram_gb:
        return False, f"Exceeded RAM quota limit of {max_ram_gb} GB"
    return True, "Within assigned resource quota"

def generate_fleet_report(
    team_name: str,
    instances: list[dict],
    max_cores: int = 64,
    max_ram_gb: float = 256.0
) -> None:
    """Aggregates and displays cloud fleet deployment telemetry."""
    total_cores = sum(inst["cores"] for inst in instances)
    total_ram = sum(inst["ram_gb"] for inst in instances)
    
    is_ok, quota_msg = verify_quota_limits(total_cores, total_ram, max_cores, max_ram_gb)
    quota_status_tag = f"✅ {quota_msg}" if is_ok else f"❌ {quota_msg}"
    
    total_cost = 0.0

    print("==================================================")
    print("       CLOUD FLEET PROVISIONING ESTIMATOR         ")
    print("==================================================")
    print(f"Team:             {team_name}")
    print(f"Instances Active: {len(instances)} nodes")
    print(f"Total CPU Cores:  {total_cores} / {max_cores} cores")
    print(f"Total RAM:        {total_ram:.1f} / {max_ram_gb:.1f} GB")
    print(f"Quota Clearance:  {quota_status_tag}")
    print("--------------------------------------------------")
    print("INSTANCE BREAKDOWN:")

    for idx, inst in enumerate(instances, start=1):
        cost = calculate_instance_cost(inst["type"], inst["hours"], inst["spot"])
        total_cost += cost
        mode = "Spot 70% off" if inst["spot"] else "On-Demand"
        print(f"  - Node #{idx} [{inst['type']}]:   {inst['hours']:.1f} hrs ({mode}) -> ${cost:.4f}")

    print("--------------------------------------------------")
    print(f"TOTAL ESTIMATED FLEET COST: ${total_cost:,.2f}")
    print("==================================================")

# 2. Execution Run
fleet = [
    {"type": "c5.xlarge", "cores": 4, "ram_gb": 16.0, "hours": 720.0, "spot": False},
    {"type": "c5.xlarge", "cores": 4, "ram_gb": 16.0, "hours": 720.0, "spot": True},
    {"type": "r5.2xlarge", "cores": 16, "ram_gb": 64.0, "hours": 360.0, "spot": False},
]

generate_fleet_report("Data Science AI Lab", fleet)
```

**Explanation of the Solution:**
- `calculate_instance_cost` encapsulates pricing tables and spot discounts into a pure, testable function.
- `verify_quota_limits` checks multi-dimensional hardware limits using default threshold values.
- `generate_fleet_report` orchestrates dictionary aggregation, function calls, and formatted reporting.
</details>
