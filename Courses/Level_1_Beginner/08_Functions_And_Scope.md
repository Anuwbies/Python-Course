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

## 2. Passing Lists & Mutable Objects (Pass-by-Object-Reference)

In Python, arguments are passed using **pass-by-object-reference** (also known as *call-by-sharing*). Understanding how functions handle mutable objects (like `list`, `dict`, `set`) versus immutable objects (like `int`, `float`, `str`, `tuple`) is essential to avoiding critical software bugs.

### 🧠 The Python Object Reference Model

When you pass a variable into a function, Python passes a **reference (pointer) to the existing memory object**, not a disconnected duplicate copy.

```
Caller's Variable [ fruits ] ────┐
                                 ▼
                      [ Memory Object: 0x7FA1B0 ]
                      [ "Apple", "Banana" ]
                                 ▲
Function Parameter [ items ] ────┘
```

#### Mutating in Place vs. Local Reassignment

```python
# --- Scenario A: In-Place Modification (Affects Caller) ---
def mutate_list(items: list[str]) -> None:
    # .append() modifies the existing object at memory address 0x7FA1B0
    items.append("Cherry")

basket = ["Apple", "Banana"]
mutate_list(basket)
print(basket) # Output: ['Apple', 'Banana', 'Cherry'] (Caller's list WAS modified!)


# --- Scenario B: Local Reassignment (Does NOT Affect Caller) ---
def reassign_list(items: list[str]) -> None:
    # '=' creates a BRAND NEW local list at a new address; severs connection!
    items = ["Orange", "Mango"]

basket = ["Apple", "Banana"]
reassign_list(basket)
print(basket) # Output: ['Apple', 'Banana'] (Caller's list is UNTOUCHED!)
```

---

### 🛡️ Pure Functions vs. Side Effects

In professional software engineering, functions should generally avoid unexpected "side effects" (unintentionally mutating data passed from external components).

| Pattern | Definition | Pros & Cons | Example |
| :--- | :--- | :--- | :--- |
| **Pure Function** | Returns a **new** value without modifying input arguments. Given identical inputs, always returns identical outputs. | ✅ Highly testable, predictable, safe in concurrent systems.<br>❌ Small memory overhead for new objects. | `def double_all(nums): return [n*2 for n in nums]` |
| **Impure / In-Place Mutation** | Modifies the input argument directly in memory. | ✅ Zero memory allocation overhead (fast for huge datasets).<br>❌ Can introduce subtle bugs across callers. | `def double_all_inplace(nums): nums[0] *= 2` |

#### Defensive Copying Pattern
If your function must modify a list internally without impacting the caller's original data, make an explicit **defensive copy**:

```python
def remove_outliers_safely(scores: list[float]) -> list[float]:
    """Cleans data by creating an isolated working copy."""
    clean_copy = scores.copy()  # or scores[:] (Shallow copy)
    if clean_copy:
        clean_copy.remove(max(clean_copy))
        clean_copy.remove(min(clean_copy))
    return clean_copy

raw_metrics = [12.0, 95.0, 4.0, 88.0, 52.0]
filtered = remove_outliers_safely(raw_metrics)

print("Original:", raw_metrics) # [12.0, 95.0, 4.0, 88.0, 52.0] (Safely preserved!)
print("Filtered:", filtered)    # [12.0, 88.0, 52.0]
```

#### Safe Guard Clauses for Empty Sequences
Never assume a list contains items. Always write guard clauses to protect against `IndexError` or `ZeroDivisionError`:

```python
def compute_class_average(grades: list[float]) -> float:
    # Guard clause: An empty list [] evaluates to False in boolean context
    if not grades:
        return 0.0
    return round(sum(grades) / len(grades), 2)
```

---

## 3. The Mutable Default Argument Trap

> [!CAUTION]
> **Never use a mutable object (`list`, `dict`, `set`) as a default parameter value!**
> In Python, default parameter expressions are evaluated **once when the function definition is executed at module load time**, NOT on each individual function call.

```python
# ❌ DANGEROUS ANTI-PATTERN: All callers share the exact SAME list object in memory!
def add_user_bad(username: str, user_list: list = []):
    user_list.append(username)
    return user_list

print(add_user_bad("Alice")) # ['Alice']
print(add_user_bad("Bob"))   # ['Alice', 'Bob'] (Accidentally shared across independent callers!)
print(add_user_bad("Charlie")) # ['Alice', 'Bob', 'Charlie']

# ✅ INDUSTRY-STANDARD PATTERN: Use None as default and instantiate internally:
def add_user_good(username: str, user_list: list = None) -> list:
    if user_list is None:
        user_list = [] # Fresh list created every call
    user_list.append(username)
    return user_list

print(add_user_good("Alice")) # ['Alice']
print(add_user_good("Bob"))   # ['Bob'] (Isolated clean instance!)
```

---

## 4. Flexible Arguments: `*args` and `**kwargs`

Python provides special syntax to accept variable numbers of arguments:

- **`*args`**: Packs arbitrary extra **positional arguments** into a **`tuple`**.
- **`**kwargs`**: Packs arbitrary extra **keyword arguments** into a **`dict`**.

```python
def configure_cluster_node(node_id: str, *ip_aliases: str, **system_flags: any) -> None:
    """Configures a server node with arbitrary IP aliases and runtime flags."""
    print(f"Configuring Node [{node_id}] (Type of args: {type(ip_aliases).__name__})")
    for ip in ip_aliases:
        print(f"  - Binding Alias IP: {ip}")
        
    print(f"Flags Applied (Type of kwargs: {type(system_flags).__name__}):")
    for key, value in system_flags.items():
        print(f"  - {key} = {value}")

# Invoking with mixed positional, variable positional, and variable keyword arguments:
configure_cluster_node(
    "NODE-US-EAST-01",
    "10.0.0.15", "10.0.0.16", "172.16.4.1",     # *args (packed into a tuple)
    region="us-east-1", ssl_enabled=True, timeout=30 # **kwargs (packed into a dict)
)
```

### Argument Unpacking in Function Calls
You can also use `*` and `**` in reverse to **unpack** collections into function arguments:

```python
def calculate_box_volume(length: float, width: float, height: float) -> float:
    return length * width * height

# Unpacking a list/tuple with *
dimensions = [10.0, 5.0, 2.0]
print(calculate_box_volume(*dimensions)) # 100.0 (Unpacks elements into positional args)

# Unpacking a dict with **
box_dict = {"length": 12.0, "width": 4.0, "height": 3.0}
print(calculate_box_volume(**box_dict))   # 144.0 (Unpacks keys as keyword args)
```

---

## 5. Variable Scope & The LEGB Rule

Scope determines where a variable can be read or modified in a Python script. Python resolves identifiers using the **LEGB hierarchy**:

```
┌────────────────────────────────────────────────────────┐
│ 1. Local (L)        Inside currently running function  │
│    ▲                                                   │
│ 2. Enclosing (E)    Inside nested/outer functions      │
│    ▲                                                   │
│ 3. Global (G)       Top level of module/file           │
│    ▲                                                   │
│ 4. Built-in (B)     Python built-ins (len, sum, range) │
└────────────────────────────────────────────────────────┘
```

```python
# Built-in scope: 'len', 'print', 'max' live in Python builtins
global_threshold = 100 # Global Scope

def outer_controller():
    controller_id = "CTRL-A" # Enclosing Scope for inner_worker()
    
    def inner_worker():
        task_id = "TSK-001" # Local Scope
        # Can read Local (task_id), Enclosing (controller_id), Global (global_threshold), Built-in (len)
        print(f"[{controller_id}] Running {task_id} under limit {global_threshold}")
    
    inner_worker()

outer_controller()
```

### Modifying Scopes: `global` vs. `nonlocal`

By default, assigning a variable inside a function creates a **new local variable** that shadows (hides) variables in outer scopes.

```python
counter = 0

def increment_bad():
    # counter = counter + 1 # ❌ UnboundLocalError: local variable referenced before assignment
    pass

def increment_global():
    global counter # Explicitly allows modifying the module-level variable
    counter += 1

increment_global()
print("Global Counter:", counter) # 1
```

> [!TIP]
> **Production Best Practice**: Minimize or avoid using the `global` keyword in production systems. Global mutable state introduces hidden coupling and makes unit testing difficult. Prefer passing arguments and returning new values explicitly.

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

## 📝 10-Tier Progressive Mastery Challenges

To build true mastery from basic function design to multi-stage modular system architecture, work through these 10 progressive challenges:

---

### 🟢 Tier 1: Fundamentals (Exercises 1–3)

#### 🔹 Exercise 1: Temperature Unit Converter (Pure Return)
* **Goal**: Write a function `celsius_to_fahrenheit(celsius: float) -> float`.
* **Formula**: `(celsius * 9/5) + 32`.
* **Requirement**: Return the result rounded to 2 decimal places (do not print inside the function).
* **Test**: `celsius_to_fahrenheit(25.0)` $\rightarrow$ `77.0`

#### 🔹 Exercise 2: Bill Splitter with Default Tip (Default Arguments)
* **Goal**: Write a function `split_bill(total_amount: float, num_people: int, tip_percentage: float = 0.15) -> float`.
* **Calculation**: Add the tip to `total_amount`, then divide evenly among `num_people`.
* **Requirement**: Return the per-person amount rounded to 2 decimal places.
* **Test**:
  - `split_bill(100.0, 4)` $\rightarrow$ `28.75` (uses default 15% tip)
  - `split_bill(100.0, 4, tip_percentage=0.20)` $\rightarrow$ `30.0`

#### 🔹 Exercise 3: Security Password Policy Validator (Boolean Logic & Early Returns)
* **Goal**: Write a function `is_strong_password(password: str) -> bool`.
* **Rules**: Must be at least 8 characters long, contain at least one uppercase letter, at least one lowercase letter, and at least one digit.
* **Requirement**: Use early returns (`return False` immediately when a rule fails, otherwise `return True`).
* **Test**:
  - `is_strong_password("Pass1234")` $\rightarrow$ `True`
  - `is_strong_password("weakpass")` $\rightarrow$ `False`

---

### 🟡 Tier 2: Intermediate Data Processing (Exercises 4–6)

#### 🔹 Exercise 4: Dataset Summary Statistics (Multiple Return Values)
* **Goal**: Write a function `calculate_statistics(numbers: list[float]) -> tuple[float, float, float]`.
* **Requirement**: Return `(minimum, maximum, average)` from the list. If the list is empty, return `(0.0, 0.0, 0.0)`.
* **Test**:
  - `low, high, avg = calculate_statistics([10.0, 20.0, 30.0, 40.0])`
  - `print(low, high, avg)` $\rightarrow$ `10.0, 40.0, 25.0`

#### 🔹 Exercise 5: Clean Task Manager (Avoiding Mutable Default Trap)
* **Goal**: Write a function `add_task(task_name: str, priority: str = "Normal", task_list: list = None) -> list`.
* **Trap to Avoid**: Do **NOT** use `task_list: list = []` in the header. Use `None` as default and initialize a fresh list inside if omitted.
* **Requirement**: Append a dictionary `{"task": task_name, "priority": priority}` to the list and return it.
* **Test**:
  - `list_a = add_task("Buy groceries")`
  - `list_b = add_task("Fix bug", priority="High")`
  - Ensure `list_a` and `list_b` are separate lists and do not share items!

#### 🔹 Exercise 6: Text Sanitizer & Word Counter (Docstrings & Modular Helpers)
* **Goal**: Write two functions:
  1. `clean_text(raw_text: str) -> str`: Converts to lowercase and removes punctuation (`.`, `,`, `!`, `?`).
  2. `word_frequency(text: str) -> dict[str, int]`: Uses `clean_text` internally, splits into words, and returns a tally dictionary.
* **Test**: `word_frequency("Hello, world! Hello Python?")` $\rightarrow$ `{"hello": 2, "world": 1, "python": 1}`

---

### 🟠 Tier 3: Advanced Function Signatures (Exercises 7–9)

#### 🔹 Exercise 7: Math Vector Aggregator (`*args`)
* **Goal**: Write a function `custom_aggregate(operation: str, *values: float) -> float`.
* **Operations supported**:
  - `"sum"`: Returns the sum of all numbers.
  - `"product"`: Returns the product (multiplication) of all numbers.
  - `"mean"`: Returns the average.
  - Any other operation: Return `0.0`.
* **Requirement**: If no numbers are passed in `*values`, return `0.0`.
* **Test**:
  - `custom_aggregate("sum", 2, 4, 6)` $\rightarrow$ `12.0`
  - `custom_aggregate("product", 2, 3, 4)` $\rightarrow$ `24.0`

#### 🔹 Exercise 8: User Profile Generator (`**kwargs`)
* **Goal**: Write a function `build_user_profile(username: str, email: str, **attributes) -> dict`.
* **Requirement**: Construct a dictionary containing `"username"`, `"email"`, and merge all arbitrary attributes passed in `**attributes`. Also add a key `"is_active": True` by default if not explicitly provided in `**attributes`.
* **Test**:
  - `build_user_profile("alice", "alice@example.com", role="Admin", department="Security")`
  - Output: `{"username": "alice", "email": "alice@example.com", "is_active": True, "role": "Admin", "department": "Security"}`

#### 🔹 Exercise 9: Universal Structured Logger (`*args` + `**kwargs` + Scope)
* **Goal**: Write a function `log_event(level: str, message: str, *tags: str, **context) -> str`.
* **Format**: Return a single formatted string:
  `"[{LEVEL}] {message} | Tags: <comma_separated_tags> | Context: <key=value, key=value>"`
  - If no tags are provided, show `"Tags: None"`.
  - If no context is provided, show `"Context: None"`.
* **Test**:
  `log_event("WARNING", "High CPU load", "infra", "compute", host="srv-01", cpu_pct=92.5)`
  - Output: `"[WARNING] High CPU load | Tags: infra, compute | Context: host=srv-01, cpu_pct=92.5"`

---

### 🟣 Tier 4: Senior Architecture & Pipeline (Exercise 10)

#### 🔹 Exercise 10: E-Commerce Checkout Pipeline (Modular System Design)
Build a complete modular checkout processing system using 4 coordinated functions:

1. **`calculate_subtotal(cart: list[dict]) -> float`**:
   - Each item in `cart` is `{"name": str, "price": float, "qty": int}`. Returns total pre-tax price.
2. **`apply_coupon(subtotal: float, coupon_code: str = None) -> float`**:
   - `"SAVE10"`: 10% discount.
   - `"SAVE20"`: 20% discount.
   - `"FLAT50"`: $50 off (minimum subtotal must be $\ge \$100$, cannot make subtotal negative).
   - If coupon is invalid or `None`, return `subtotal` unchanged.
3. **`calculate_shipping(subtotal: float, is_express: bool = False, is_international: bool = False) -> float`**:
   - Base shipping: `$10.00` (Free if `subtotal >= 100.0`).
   - Add `$15.00` if `is_express`.
   - Add `$25.00` if `is_international`.
4. **`process_order(customer_name: str, cart: list[dict], coupon: str = None, **shipping_options) -> dict`**:
   - Calls the 3 functions above, calculates tax (8% on discounted subtotal), and returns an order summary dictionary containing:
     - `customer`: `customer_name`
     - `subtotal`: float
     - `discounted_subtotal`: float
     - `shipping_cost`: float
     - `tax`: float
     - `total`: float (discounted subtotal + shipping + tax, rounded to 2 decimals)

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
<summary><b>🔍 View Exercise Solutions (VM Utility & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Cloud VM Fleet Estimator
# =====================================================================
def calculate_instance_cost(instance_type: str, hours: float, is_spot_instance: bool = False) -> float:
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

# =====================================================================
# SOLUTION: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
def celsius_to_fahrenheit(celsius: float) -> float:
    return round((celsius * 9/5) + 32, 2)

# Ex 2:
def split_bill(total_amount: float, num_people: int, tip_percentage: float = 0.15) -> float:
    total = total_amount * (1 + tip_percentage)
    return round(total / num_people, 2)

# Ex 3:
def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True

# Ex 4:
def calculate_statistics(numbers: list[float]) -> tuple[float, float, float]:
    if not numbers:
        return (0.0, 0.0, 0.0)
    return (min(numbers), max(numbers), sum(numbers) / len(numbers))

# Ex 5:
def add_task(task_name: str, priority: str = "Normal", task_list: list = None) -> list:
    if task_list is None:
        task_list = []
    task_list.append({"task": task_name, "priority": priority})
    return task_list

# Ex 6:
def clean_text(raw_text: str) -> str:
    cleaned = raw_text.lower()
    for char in [".", ",", "!", "?"]:
        cleaned = cleaned.replace(char, "")
    return cleaned

def word_frequency(text: str) -> dict[str, int]:
    cleaned = clean_text(text)
    words = cleaned.split()
    tally = {}
    for w in words:
        tally[w] = tally.get(w, 0) + 1
    return tally

# Ex 7:
def custom_aggregate(operation: str, *values: float) -> float:
    if not values:
        return 0.0
    if operation == "sum":
        return float(sum(values))
    elif operation == "product":
        prod = 1.0
        for v in values:
            prod *= v
        return float(prod)
    elif operation == "mean":
        return float(sum(values) / len(values))
    return 0.0

# Ex 8:
def build_user_profile(username: str, email: str, **attributes) -> dict:
    profile = {
        "username": username,
        "email": email,
        "is_active": attributes.pop("is_active", True)
    }
    profile.update(attributes)
    return profile

# Ex 9:
def log_event(level: str, message: str, *tags: str, **context) -> str:
    tag_str = ", ".join(tags) if tags else "None"
    ctx_str = ", ".join(f"{k}={v}" for k, v in context.items()) if context else "None"
    return f"[{level}] {message} | Tags: {tag_str} | Context: {ctx_str}"

# Ex 10:
def calculate_subtotal(cart: list[dict]) -> float:
    return sum(item["price"] * item["qty"] for item in cart)

def apply_coupon(subtotal: float, coupon_code: str = None) -> float:
    if not coupon_code:
        return subtotal
    if coupon_code == "SAVE10":
        return subtotal * 0.90
    elif coupon_code == "SAVE20":
        return subtotal * 0.80
    elif coupon_code == "FLAT50" and subtotal >= 100.0:
        return max(0.0, subtotal - 50.0)
    return subtotal

def calculate_shipping(subtotal: float, is_express: bool = False, is_international: bool = False) -> float:
    shipping = 0.0 if subtotal >= 100.0 else 10.00
    if is_express:
        shipping += 15.00
    if is_international:
        shipping += 25.00
    return shipping

def process_order(customer_name: str, cart: list[dict], coupon: str = None, **shipping_options) -> dict:
    subtotal = calculate_subtotal(cart)
    discounted = apply_coupon(subtotal, coupon)
    shipping = calculate_shipping(discounted, **shipping_options)
    tax = discounted * 0.08
    total = round(discounted + shipping + tax, 2)
    return {
        "customer": customer_name,
        "subtotal": round(subtotal, 2),
        "discounted_subtotal": round(discounted, 2),
        "shipping_cost": round(shipping, 2),
        "tax": round(tax, 2),
        "total": total
    }
```
</details>
