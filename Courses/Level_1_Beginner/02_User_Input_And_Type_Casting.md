# Lesson 2: Dynamic User Input, Type Casting & String Sanitization

In real-world software engineering, applications rarely run on hardcoded static values. Applications interact with human users, external APIs, configuration files, and terminal arguments. In this lesson, you will master receiving interactive input from users, converting data types safely (type casting), and sanitizing text data.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Capture interactive terminal input using the built-in `input()` function.
2. Understand that `input()` **unconditionally returns a string (`str`)**.
3. Safely cast raw strings into `int`, `float`, `str`, and `bool`.
4. Recognize and prevent common conversion pitfalls (such as `ValueError` on bad numbers and `bool("False") == True`).
5. Clean and sanitize user input using `.strip()`, `.lower()`, `.upper()`, and `.title()`.
6. Chain string methods together cleanly.

---

## 1. Capturing User Input with `input()`

The `input()` function prompts the user in the console, halts execution until the user presses `[Enter]`, and returns everything typed as a `str`:

```python
user_name = input("Enter your full name: ")
print(f"Welcome to the portal, {user_name}!")
print(f"Data type of user_name is: {type(user_name)}")  # Always <class 'str'>
```

> [!WARNING]
> **The `input()` String Trap**:
> Even if a user enters `42`, Python captures `"42"` (a string). If you perform addition without casting, Python concatenates strings instead of adding numbers:
> ```python
> a = input("Enter number 1: ") # User enters 10
> b = input("Enter number 2: ") # User enters 20
> print(a + b)                  # Output: "1020" (String concatenation, not 30!)
> ```

---

## 2. Type Casting (Explicit Type Conversion)

To perform mathematical calculations or logical operations on user input, you must convert the string into the appropriate numeric or boolean type.

```python
# Converting to Integer:
user_age_str = input("Enter your age: ")
user_age = int(user_age_str)
next_year_age = user_age + 1
print(f"Next year you will be {next_year_age} years old.")

# Inline casting directly at input time:
hourly_wage = float(input("Enter hourly wage ($): "))
hours_worked = float(input("Enter hours worked this week: "))
gross_pay = hourly_wage * hours_worked
print(f"Gross Pay: ${gross_pay:,.2f}")
```

### Type Conversion Functions Overview

| Function | Converts Input To | Valid Inputs | Behavior on Invalid Input |
| :--- | :--- | :--- | :--- |
| `int(x)` | Integer | `"42"`, `3.99` (truncates to 3), `True` (1) | Raises `ValueError` on `"42.5"` or `"abc"` |
| `float(x)` | Float | `"3.14"`, `"42"`, `10` (10.0) | Raises `ValueError` on non-numeric strings |
| `str(x)` | String | Any Python object | Always succeeds (`str(100)` $\rightarrow$ `"100"`) |
| `bool(x)` | Boolean | Any Python object | Empty objects $\rightarrow$ `False`, Non-empty $\rightarrow$ `True` |

---

## 3. The Boolean Casting Truthiness Trap

A frequent bug for beginners is trying to cast `"False"` to a boolean using `bool("False")`.

In Python, `bool()` evaluates **truthiness**:
- Any non-empty string evaluates to `True` (including `"False"`, `"0"`, and `"   "`).
- Only the empty string `""` evaluates to `False`.

```python
# ❌ INCORRECT:
is_subscribed = bool(input("Subscribe? (True/False): ")) # Typing "False" produces True!

# ✅ CORRECT: Compare against expected strings:
raw_answer = input("Subscribe? (yes/no): ").strip().lower()
is_subscribed = raw_answer == "yes"
```

---

## 4. String Sanitization & Method Chaining

Users frequently include accidental leading/trailing spaces or unpredictable capitalization. Python provides string methods to sanitize raw inputs:

```python
# 1. Stripping unwanted whitespace:
raw_email = "   engineer@enterprise.io   \n"
clean_email = raw_email.strip() # "engineer@enterprise.io"

# 2. Case normalization:
city_input = "  sAn fRaNcIsCo  "
print(city_input.strip().title()) # "San Francisco"
print(city_input.strip().upper()) # "SAN FRANCISCO"
print(city_input.strip().lower()) # "san francisco"

# 3. Method Chaining:
command = input("Enter action (START / STOP): ").strip().upper()
```

---

## 💻 Code Example & Reference

The following real-life program models an **Aviation Cargo Manifest & Fuel Calculation System**, using all concepts from this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Aviation Flight Dispatcher & Cargo Intake Engine
# =====================================================================

print("=" * 65)
print(f"{'✈️  AEROSPACE FLIGHT DISPATCH & FUEL CALCULATOR':^65}")
print("=" * 65)

# 1. Interactive Inputs with Sanitization & Chaining
flight_code = input("Enter Flight Code (e.g. ua-892): ").strip().upper()
destination_city = input("Enter Destination City: ").strip().title()
aircraft_tail_no = input("Enter Aircraft Tail ID: ").strip().upper()

# 2. Numeric Type Casting
distance_nautical_miles = float(input("Enter route distance (Nautical Miles): "))
passenger_count = int(input("Enter total checked-in passengers: "))
average_passenger_weight_kg = 82.5 # standard aviation assumption
cargo_freight_kg = float(input("Enter additional freight cargo weight (kg): "))

# 3. Boolean Evaluation via String Comparison
is_international_str = input("Is this an international flight? (yes/no): ").strip().lower()
is_international = is_international_str in ("yes", "y", "true")

# 4. Systems Arithmetic Calculations
total_passenger_mass_kg = passenger_count * average_passenger_weight_kg
total_payload_kg = total_passenger_mass_kg + cargo_freight_kg

# Fuel burn: ~4.2 kg per nautical mile + reserve buffer
fuel_rate_per_nm = 4.2
contingency_multiplier = 1.15 if is_international else 1.05
required_fuel_kg = distance_nautical_miles * fuel_rate_per_nm * contingency_multiplier

# 5. Formatted Manifest Display
print("\n" + "=" * 65)
print(f"{'OFFICIAL FLIGHT DISPATCH MANIFEST':^65}")
print("=" * 65)
print(f"{'Flight Number:':<30} {flight_code}")
print(f"{'Destination:':<30} {destination_city}")
print(f"{'Aircraft Tail:':<30} {aircraft_tail_no}")
print(f"{'International Clearance:':<30} {str(is_international)}")
print("-" * 65)
print(f"{'Flight Distance:':<30} {distance_nautical_miles:,.1f} NM")
print(f"{'Passenger Count:':<30} {passenger_count} souls")
print(f"{'Total Passenger Mass:':<30} {total_passenger_mass_kg:,.2f} kg")
print(f"{'Cargo Freight Mass:':<30} {cargo_freight_kg:,.2f} kg")
print(f"{'Total Payload Mass:':<30} {total_payload_kg:,.2f} kg")
print("-" * 65)
print(f"{'REQUIRED FUEL (WITH RESERVES):':<30} {required_fuel_kg:,.2f} kg")
print("=" * 65)
```

### 🔍 Code Explanation:
- **`input()` & Sanitization**: `input()` captures raw terminal entries, chained with `.strip().upper()` or `.strip().title()` to ensure data integrity regardless of how the operator typed it.
- **Explicit Type Casting**: `float()` and `int()` convert numeric text strings to arithmetic-compatible values for distance, passengers, and cargo weights.
- **Safe Boolean Evaluation**: Rather than using `bool(input())`, we compare `.strip().lower()` against acceptable affirmative terms (`"yes"`, `"y"`, `"true"`).
- **Formatted Presentation**: We generate a clear flight manifest with alignment specifiers and thousands separators (`:,.2f`).

---

## 📝 Quick Exercise: Freelance Billing & Invoice Calculator

### 🏢 Real-Life Scenario
You are building an automated invoicing utility for freelance software consultants. The program prompts the consultant for client details, hourly billing rate, billable project hours, and any software/cloud infrastructure expenses incurred. It then calculates the labor subtotal, total invoice amount, estimated income tax withholding, and expected net earnings.

### 📋 Requirements
1. Prompt for and sanitize the following inputs:
   - `client_name`: Prompt with `"Enter client business name: "` and format with `.strip().title()`.
   - `project_title`: Prompt with `"Enter project title: "` and format with `.strip()`.
2. Prompt and cast numerical inputs:
   - `hourly_rate`: Prompt with `"Enter hourly billing rate ($): "` and cast to `float`.
   - `hours_worked`: Prompt with `"Enter total billable hours: "` and cast to `float`.
   - `expenses`: Prompt with `"Enter cloud/hardware expenses incurred ($): "` and cast to `float`.
3. Perform the following financial calculations:
   - `labor_cost = hourly_rate * hours_worked`
   - `invoice_total = labor_cost + expenses`
   - `tax_withholding = invoice_total * 0.22` (estimated 22% tax reserve)
   - `net_earnings = invoice_total - tax_withholding`
4. Using **f-strings**, output a clean, formatted billing summary with all monetary amounts formatted to 2 decimal places with comma grouping (`:,.2f`).

> [!IMPORTANT]
> **Cumulative Constraint**: Use concepts covered in **Lessons 1 and 2** (variables, primitives, `input()`, `int()`, `float()`, `str()`, string sanitization methods, arithmetic, f-strings, and `print()`).

### 🎯 Expected Output
*(Assuming the user inputs: Client: `   quantum leap technologies   `, Project: `Cloud API Migration`, Rate: `85.00`, Hours: `32.5`, Expenses: `120.50`)*

```text
Enter client business name:    quantum leap technologies   
Enter project title: Cloud API Migration
Enter hourly billing rate ($): 85.00
Enter total billable hours: 32.5
Enter cloud/hardware expenses incurred ($): 120.50

==================================================
           FREELANCE INVOICE SUMMARY              
==================================================
Client:        Quantum Leap Technologies
Project:       Cloud API Migration
--------------------------------------------------
Hours Logged:  32.50 hrs @ $85.00/hr
Labor Cost:    $2,762.50
Expenses:      $120.50
--------------------------------------------------
INVOICE TOTAL: $2,883.00
Est. Tax (22%):$634.26
NET EARNINGS:  $2,248.74
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Capture and sanitize text inputs (Lesson 1 & 2)
client_name = input("Enter client business name: ").strip().title()
project_title = input("Enter project title: ").strip()

# 2. Capture and cast numeric inputs (Lesson 2)
hourly_rate = float(input("Enter hourly billing rate ($): "))
hours_worked = float(input("Enter total billable hours: "))
expenses = float(input("Enter cloud/hardware expenses incurred ($): "))

# 3. Perform calculations (Lesson 1 & 2)
labor_cost = hourly_rate * hours_worked
invoice_total = labor_cost + expenses
tax_withholding = invoice_total * 0.22
net_earnings = invoice_total - tax_withholding

# 4. Formatted invoice display (Lesson 1 f-strings)
print("\n==================================================")
print("           FREELANCE INVOICE SUMMARY              ")
print("==================================================")
print(f"Client:        {client_name}")
print(f"Project:       {project_title}")
print("--------------------------------------------------")
print(f"Hours Logged:  {hours_worked:.2f} hrs @ ${hourly_rate:.2f}/hr")
print(f"Labor Cost:    ${labor_cost:,.2f}")
print(f"Expenses:      ${expenses:,.2f}")
print("--------------------------------------------------")
print(f"INVOICE TOTAL: ${invoice_total:,.2f}")
print(f"Est. Tax (22%):${tax_withholding:,.2f}")
print(f"NET EARNINGS:  ${net_earnings:,.2f}")
print("==================================================")
```

**Explanation of the Solution:**
- Input strings are sanitized at capture time using `.strip()` and `.title()`.
- Floating-point casting enables math calculations on user-provided financial rates.
- `f"{val:,.2f}"` produces professional dollar-and-cent formatting.
</details>
