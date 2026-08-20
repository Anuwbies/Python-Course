# 🟢 Level 1: Beginner Python — 20 Comprehensive Capstone Projects

Welcome to the **Level 1 Beginner Capstone Collection**! This document contains 20 production-inspired capstone projects designed to test and solidify foundational computer science concepts: variables, type casting, operators, conditionals, loops, sequences (lists, tuples), dictionaries, sets, functions, file I/O, error handling, and Object-Oriented Programming (OOP).

Every solution includes **detailed, step-by-step explanatory comments directly inside the code** to guide your learning.

---

## 📑 Table of Contents
1. [Retail Point-of-Sale (POS) Cash Register & Receipt Engine](#1-retail-point-of-sale-pos-cash-register--receipt-engine)
2. [Hotel Room Reservation & Automated Billing Dispatcher](#2-hotel-room-reservation--automated-billing-dispatcher)
3. [Banking Account Ledger CLI with File Persistence & PIN Security](#3-banking-account-ledger-cli-with-file-persistence--pin-security)
4. [Hospital Patient Medical Intake & Triage Assessment Engine](#4-hospital-patient-medical-intake--triage-assessment-engine)
5. [Student Academic Gradebook & GPA Transcript Generator](#5-student-academic-gradebook--gpa-transcript-generator)
6. [E-Commerce Inventory Reordering & Stock Alert Monitor](#6-e-commerce-inventory-reordering--stock-alert-monitor)
7. [Aviation Flight Manifest & Baggage Fee Dispatcher](#7-aviation-flight-manifest--baggage-fee-dispatcher)
8. [Personal Expense Tracker & Monthly Budget Forecaster](#8-personal-expense-tracker--monthly-budget-forecaster)
9. [Library Book Borrowing & Overdue Fine Calculation System](#9-library-book-borrowing--overdue-fine-calculation-system)
10. [Gym Membership & Access Control Card Verification System](#10-gym-membership--access-control-card-verification-system)
11. [Restaurant Table Reservation & Kitchen Order Queue](#11-restaurant-table-reservation--kitchen-order-queue)
12. [Payroll Salary & Tax Withholding Calculator](#12-payroll-salary--tax-withholding-calculator)
13. [Car Rental Fleet Reservation & Mileage Fee Engine](#13-car-rental-fleet-reservation--mileage-fee-engine)
14. [Real Estate Property Listing & Mortgage Filter Engine](#14-real-estate-property-listing--mortgage-filter-engine)
15. [Warehouse Logistics Pallet Inventory & Space Allocator](#15-warehouse-logistics-pallet-inventory--space-allocator)
16. [Cinema Ticket Seat Booking & Dynamic Pricing System](#16-cinema-ticket-seat-booking--dynamic-pricing-system)
17. [Coffee Shop Drink Customizer & Loyalty Points Ledger](#17-coffee-shop-drink-customizer--loyalty-points-ledger)
18. [Emergency Hotline Dispatch & Incident Priority Logger](#18-emergency-hotline-dispatch--incident-priority-logger)
19. [Electric Vehicle (EV) Charging Station Billing & KWh Meter](#19-electric-vehicle-ev-charging-station-billing--kwh-meter)
20. [Password Policy Compliance & Credential Vault Manager](#20-password-policy-compliance--credential-vault-manager)

---

## 1. Retail Point-of-Sale (POS) Cash Register & Receipt Engine

### 🏢 Real-Life Scenario
A retail boutique needs an automated checkout register. The system records scanned item SKUs, computes subtotal and tax, applies membership discounts, accepts payments, and outputs a formatted physical receipt.

### 📋 Requirements
1. Store catalog in a dictionary: `CATALOG = {"SKU1": ("Item Name", unit_price), ...}`.
2. Accept a list of purchased SKUs and quantities.
3. Apply an 8.5% sales tax. If the customer is a VIP member, deduct 10% from the subtotal.
4. Calculate change for cash payment.

### 🎯 Expected Output
```text
==================================================
           APEX RETAIL BOUTIQUE REGISTER          
==================================================
Item Name                 Qty    Unit Price     Total
--------------------------------------------------
Classic Denim Jacket        1       $89.99     $89.99
Organic Cotton T-Shirt      2       $24.50     $49.00
Leather Card Wallet         1       $35.00     $35.00
--------------------------------------------------
Subtotal:                                     $173.99
VIP Member Discount (10%):                    -$17.40
Taxable Amount:                               $156.59
Sales Tax (8.5%):                              $13.31
TOTAL DUE:                                    $169.90
--------------------------------------------------
Cash Tendered:                                $200.00
Change Due:                                    $30.10
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 1: Retail Point-of-Sale (POS) Cash Register Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. CATALOG DICTIONARY: Maps unique SKU keys to a tuple (item_name, unit_price).
#    This provides O(1) constant-time lookup performance during checkout scanning.
# 2. CART PROCESSING: Iterates over scanned (sku, quantity) pairs, computes line totals,
#    and aggregates them into the running subtotal.
# 3. TAX & DISCOUNT LOGIC: VIP members receive a 10% discount off the subtotal.
#    Sales tax (8.5%) is calculated strictly on the net taxable amount (subtotal - discount),
#    ensuring customers do not pay tax on discounted savings.
# 4. CASH TENDER & CHANGE: Computes the remaining balance (cash_paid - total).
# 5. STRING FORMATTING: Uses f-string column width specifiers (<25, >8.2f) to produce
#    a clean, professional monospace printed receipt.
# =====================================================================

# Step 1: Centralized Product Catalog
CATALOG = {
    "SKU-01": ("Classic Denim Jacket", 89.99),
    "SKU-02": ("Organic Cotton T-Shirt", 24.50),
    "SKU-03": ("Leather Card Wallet", 35.00),
}

def process_pos_transaction(cart: list[tuple[str, int]], is_vip: bool, cash_paid: float) -> None:
    """Processes customer checkout, calculates taxes and discounts, and prints a formatted receipt."""
    subtotal = 0.0
    line_items = []

    # Step 2: Iterate through cart items and compute line totals
    for sku, qty in cart:
        name, price = CATALOG[sku]
        line_total = price * qty
        subtotal += line_total
        # Store unpacked line item for formatted printing
        line_items.append((name, qty, price, line_total))

    # Step 3: Compute VIP Member Discount (10% if VIP, else $0.00)
    discount = (subtotal * 0.10) if is_vip else 0.0
    taxable_amount = subtotal - discount

    # Step 4: Apply 8.5% municipal sales tax on the post-discount taxable amount
    sales_tax = taxable_amount * 0.085
    total_due = taxable_amount + sales_tax

    # Step 5: Compute change owed back to the customer
    change_due = cash_paid - total_due

    # Step 6: Format and display the terminal receipt
    print("==================================================")
    print("           APEX RETAIL BOUTIQUE REGISTER          ")
    print("==================================================")
    print(f"{'Item Name':<25} {'Qty':>3} {'Unit Price':>13} {'Total':>9}")
    print("-" * 50)
    for name, qty, price, l_tot in line_items:
        print(f"{name:<25} {qty:>3} {f'${price:.2f}':>13} {f'${l_tot:.2f}':>9}")
    print("-" * 50)
    print(f"{'Subtotal:':<40} ${subtotal:>8.2f}")
    if is_vip:
        print(f"{'VIP Member Discount (10%):':<40} -${discount:>7.2f}")
        print(f"{'Taxable Amount:':<40} ${taxable_amount:>8.2f}")
    print(f"{'Sales Tax (8.5%):':<40} ${sales_tax:>8.2f}")
    print(f"{'TOTAL DUE:':<40} ${total_due:>8.2f}")
    print("-" * 50)
    print(f"{'Cash Tendered:':<40} ${cash_paid:>8.2f}")
    print(f"{'Change Due:':<40} ${change_due:>8.2f}")
    print("==================================================")

# Execute Simulation: VIP customer buying 1 jacket, 2 t-shirts, 1 wallet, paying $200.00 cash
customer_cart = [("SKU-01", 1), ("SKU-02", 2), ("SKU-03", 1)]
process_pos_transaction(customer_cart, is_vip=True, cash_paid=200.00)
```
</details>

---

## 2. Hotel Room Reservation & Automated Billing Dispatcher

### 🏢 Real-Life Scenario
A resort hotel manages guest reservations across room categories (Standard, Deluxe, Penthouse) with weekend pricing surcharges and resort amenity fees.

### 📋 Requirements
1. Define room rates: `Standard = $120/night`, `Deluxe = $220/night`, `Penthouse = $550/night`.
2. Weekend nights (Friday/Saturday) carry a 20% surcharge on room rate.
3. Daily resort fee: $25.00/night flat.
4. Calculate stay totals and display billing statement.

### 🎯 Expected Output
```text
==================================================
        GRAND HORIZON RESORT & SPA INVOICE        
==================================================
Guest Name:       Elena Rostova
Room Type:        Deluxe ($220.00/night base)
Duration:         4 Nights (2 Weekday, 2 Weekend)
--------------------------------------------------
Weekday Room Charges:                          $440.00
Weekend Surcharge Charges (20%):               $528.00
Resort & Amenity Fees ($25/night):             $100.00
Tourism City Tax (6%):                          $64.08
--------------------------------------------------
TOTAL CHARGES DUE:                           $1,132.08
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 2: Hotel Room Reservation & Billing Dispatcher
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. PRICING CONFIGURATION: Centralized dictionary storing base room tariffs.
# 2. DYNAMIC SURCHARGE MATH: Weekend nights are charged at 1.20x base tariff (20% premium).
# 3. AMENITY CALCULATIONS: Daily resort fee ($25/night) applies across all nights.
# 4. TAXATION: 6% Tourism municipal tax applies to the cumulative subtotal.
# =====================================================================

# Step 1: Base Tier Tariffs
RATES = {"Standard": 120.0, "Deluxe": 220.0, "Penthouse": 550.0}

def generate_hotel_bill(guest: str, room_type: str, weekday_nights: int, weekend_nights: int) -> None:
    """Calculates tiered hotel reservation costs with weekend surcharges and tourism taxes."""
    # Step 2: Retrieve base rate for chosen room category
    base_rate = RATES[room_type]

    # Step 3: Compute segmented stay charges
    weekday_cost = weekday_nights * base_rate
    weekend_cost = weekend_nights * (base_rate * 1.20) # 20% weekend demand surcharge
    total_nights = weekday_nights + weekend_nights
    resort_fee = total_nights * 25.0 # $25.00/night amenity charge
    
    # Step 4: Calculate subtotal and municipal tourism tax (6%)
    subtotal = weekday_cost + weekend_cost + resort_fee
    tax = subtotal * 0.06
    grand_total = subtotal + tax

    # Step 5: Format and render the guest folio invoice
    print("==================================================")
    print("        GRAND HORIZON RESORT & SPA INVOICE        ")
    print("==================================================")
    print(f"Guest Name:       {guest}")
    print(f"Room Type:        {room_type} (${base_rate:.2f}/night base)")
    print(f"Duration:         {total_nights} Nights ({weekday_nights} Weekday, {weekend_nights} Weekend)")
    print("-" * 50)
    print(f"{'Weekday Room Charges:':<40} ${weekday_cost:>8.2f}")
    print(f"{'Weekend Surcharge Charges (20%):':<40} ${weekend_cost:>8.2f}")
    print(f"{'Resort & Amenity Fees ($25/night):':<40} ${resort_fee:>8.2f}")
    print(f"{'Tourism City Tax (6%):':<40} ${tax:>8.2f}")
    print("-" * 50)
    print(f"{'TOTAL CHARGES DUE:':<40} ${grand_total:>8.2f}")
    print("==================================================")

# Execute Simulation
generate_hotel_bill("Elena Rostova", "Deluxe", weekday_nights=2, weekend_nights=2)
```
</details>

---

## 3. Banking Account Ledger CLI with File Persistence & PIN Security

### 🏢 Real-Life Scenario
A community bank requires a command-line account management tool that allows customers to authenticate with a PIN, check balances, deposit, withdraw with overdraft prevention, and save transaction logs to a text file.

### 📋 Requirements
1. Implement a `BankAccount` class with `account_num`, `holder_name`, `pin`, and `balance`.
2. Support `authenticate(entered_pin)`, `deposit(amount)`, and `withdraw(amount)`.
3. Log all transactions into a local log file using Python's `with open()`.

### 🎯 Expected Output
```text
==================================================
           APEX COMMUNITY BANK TERMINAL           
==================================================
[AUTH SUCCESS] Welcome, Marcus Vance!
[DEPOSIT] +$500.00 -> New Balance: $1,500.00
[WITHDRAW] -$200.00 -> New Balance: $1,300.00
[WITHDRAW REJECTED] Overdraft attempt of $2,000.00 blocked.
--------------------------------------------------
TRANSACTION HISTORY PERSISTED TO DISK:
  - Account: ACC-901 | Balance: $1,300.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 3: Bank Account Ledger with File Persistence
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. OOP ENCAPSULATION: Models BankAccount holding private credentials (PIN) and balance state.
# 2. INVARIANT PROTECTION: Withdrawals enforce liquidity checks to prevent overdrafts.
# 3. AUDIT TRAIL LOGGING: Every financial mutation records an entry in self.history.
# 4. CONTEXT-MANAGED FILE PERSISTENCE: with open() writes ledger logs to disk safely.
# =====================================================================

import os

class BankAccount:
    """Encapsulates banking account state, transaction operations, and disk persistence."""

    def __init__(self, account_num: str, holder_name: str, pin: str, initial_balance: float = 0.0):
        self.account_num = account_num
        self.holder_name = holder_name
        self.pin = pin
        self.balance = initial_balance
        self.history = [] # In-memory transaction journal

    def authenticate(self, entered_pin: str) -> bool:
        """Validates customer credentials against the stored PIN."""
        return self.pin == entered_pin

    def deposit(self, amount: float) -> None:
        """Deposits positive funds into the account and journals the operation."""
        if amount > 0:
            self.balance += amount
            self.history.append(f"DEPOSIT: +${amount:.2f}")
            print(f"[DEPOSIT] +${amount:,.2f} -> New Balance: ${self.balance:,.2f}")

    def withdraw(self, amount: float) -> bool:
        """Attempts withdrawal. Blocks operation if requested amount causes an overdraft."""
        if amount <= 0:
            return False
        # Guard clause: Overdraft check
        if amount > self.balance:
            print(f"[WITHDRAW REJECTED] Overdraft attempt of ${amount:,.2f} blocked.")
            return False
        
        self.balance -= amount
        self.history.append(f"WITHDRAW: -${amount:.2f}")
        print(f"[WITHDRAW] -${amount:,.2f} -> New Balance: ${self.balance:,.2f}")
        return True

    def save_ledger_to_disk(self, filename: str) -> None:
        """Persists customer account balance and full transaction history to a file."""
        # Using context manager 'with open' guarantees file descriptor is flushed and closed
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"ACCOUNT:{self.account_num}\nHOLDER:{self.holder_name}\nBALANCE:{self.balance:.2f}\n")
            for entry in self.history:
                f.write(f"{entry}\n")


# Step 5: Execute Banking Simulation
account = BankAccount("ACC-901", "Marcus Vance", "4412", initial_balance=1000.00)

print("==================================================")
print("           APEX COMMUNITY BANK TERMINAL           ")
print("==================================================")

if account.authenticate("4412"):
    print(f"[AUTH SUCCESS] Welcome, {account.holder_name}!")
    account.deposit(500.00)
    account.withdraw(200.00)
    account.withdraw(2000.00) # Blocked overdraft attempt
    
    # Save ledger to disk
    log_filename = "bank_audit.txt"
    account.save_ledger_to_disk(log_filename)
    
    print("--------------------------------------------------")
    print("TRANSACTION HISTORY PERSISTED TO DISK:")
    print(f"  - Account: {account.account_num} | Balance: ${account.balance:,.2f}")
    print("==================================================")
    
    # Cleanup temporary file after test run
    if os.path.exists(log_filename):
        os.remove(log_filename)
```
</details>

---

## 4. Hospital Patient Medical Intake & Triage Assessment Engine

### 🏢 Real-Life Scenario
A hospital emergency room intake desk classifies incoming patients based on vital signs (Heart Rate, Systolic Blood Pressure, Oxygen Saturation) into triage severity categories: Level 1 (Resuscitation), Level 2 (Emergent), Level 3 (Urgent), Level 4 (Non-Urgent).

### 📋 Requirements
1. If $O_2 \text{ Saturation} < 90\%$ or $\text{Systolic BP} > 180$: Level 1 (Resuscitation).
2. If $\text{Heart Rate} > 120$ or $\text{Systolic BP} > 140$: Level 2 (Emergent).
3. If $\text{Heart Rate} > 100$: Level 3 (Urgent).
4. Otherwise: Level 4 (Non-Urgent).

### 🎯 Expected Output
```text
==================================================
        HOSPITAL ER TRIAGE INTAKE SUMMARY         
==================================================
Patient ID:       PAT-108
Name:             Sarah Connor
Heart Rate:       128 bpm
Blood Pressure:   145 mmHg
Oxygen (SpO2):    96%
--------------------------------------------------
ASSIGNED TRIAGE:  🚨 LEVEL 2 (EMERGENT)
Recommended Care: Immediate physician assessment within 15 minutes.
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 4: Hospital Patient Emergency Triage Assessment Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. HIERARCHICAL EMERGENCY DECISION TREE: Evaluates clinical vitals in strictly
#    descending order of severity. Level 1 (life threat) is checked first.
# 2. COMPOUND SHORT-CIRCUIT BOOLEANS: Python's 'or' operator evaluates conditions
#    left-to-right, short-circuiting as soon as a true predicate is encountered.
# 3. CLINICAL ACTION MAPPING: Maps numeric classifications directly to response protocols.
# =====================================================================

def assess_triage(patient_id: str, name: str, hr: int, bp_systolic: int, spo2: int) -> None:
    """Evaluates vital signs against emergency medicine triage protocols."""
    
    # Priority Tier 1: Immediate Resuscitation (Hypoxia or Hypertensive Crisis)
    if spo2 < 90 or bp_systolic > 180:
        level = "🚨 LEVEL 1 (RESUSCITATION)"
        care = "Immediate continuous resuscitation intervention required."
    # Priority Tier 2: Emergent (Severe Tachycardia or Stage 2 Hypertension)
    elif hr > 120 or bp_systolic > 140:
        level = "🚨 LEVEL 2 (EMERGENT)"
        care = "Immediate physician assessment within 15 minutes."
    # Priority Tier 3: Urgent (Moderate Tachycardia)
    elif hr > 100:
        level = "⚠️ LEVEL 3 (URGENT)"
        care = "Clinical assessment within 30 minutes."
    # Priority Tier 4: Stable / Non-Urgent
    else:
        level = "✅ LEVEL 4 (NON-URGENT)"
        care = "Routine outpatient triage queue."

    # Format clinical report
    print("==================================================")
    print("        HOSPITAL ER TRIAGE INTAKE SUMMARY         ")
    print("==================================================")
    print(f"Patient ID:       {patient_id}")
    print(f"Name:             {name}")
    print(f"Heart Rate:       {hr} bpm")
    print(f"Blood Pressure:   {bp_systolic} mmHg")
    print(f"Oxygen (SpO2):    {spo2}%")
    print("-" * 50)
    print(f"ASSIGNED TRIAGE:  {level}")
    print(f"Recommended Care: {care}")
    print("==================================================")

# Execute Clinical Intake Simulation
assess_triage("PAT-108", "Sarah Connor", hr=128, bp_systolic=145, spo2=96)
```
</details>

---

## 5. Student Academic Gradebook & GPA Transcript Generator

### 🏢 Real-Life Scenario
A university registrar department requires a tool that accepts student course grades, calculates weighted grade points ($A=4.0, B=3.0, C=2.0, D=1.0, F=0.0$), computes GPA, and generates academic honors standing.

### 📋 Requirements
1. Dictionary mapping course names to `(credit_hours, letter_grade)`.
2. Compute cumulative GPA = $\frac{\sum(\text{Grade Points} \times \text{Credits})}{\sum \text{Credits}}$.
3. Assign Honors: $\text{GPA} \ge 3.8 \to \text{"Summa Cum Laude"}$, $\ge 3.5 \to \text{"Magna Cum Laude"}$, $\ge 3.0 \to \text{"Dean's List"}$.

### 🎯 Expected Output
```text
==================================================
           OFFICIAL ACADEMIC TRANSCRIPT           
==================================================
Student: David Kim | ID: STU-8821
--------------------------------------------------
Course Code               Credits  Grade  Points  
--------------------------------------------------
CS101: Intro to Python          4      A    16.0  
MATH201: Calculus II            4      B    12.0  
PHYS101: General Physics        4      A    16.0  
ENG102: Tech Writing            3      A    12.0  
--------------------------------------------------
Total Credit Hours: 15
Cumulative GPA:     3.73 / 4.00
Academic Standing:  Dean's List (Honors)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 5: Academic Gradebook & GPA Transcript Generator
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. WEIGHTED GRADE POINT CALCULATION: Maps letter grades to standard 4.0 scale points.
#    Each course earns Quality Points = (Credits * Grade_Points).
# 2. GPA AMORTIZATION FORMULA: Cumulative GPA = Total Quality Points / Total Credits.
# 3. DEFENSIVE CODING: Guards against ZeroDivisionError for empty transcripts.
# 4. ACADEMIC HONORS LADDER: Cascading conditionals assign Latin honors.
# =====================================================================

GRADE_POINTS = {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0.0}

def generate_transcript(student_id: str, name: str, courses: dict[str, tuple[int, str]]) -> None:
    """Generates an official academic transcript with credit-weighted GPA calculation."""
    total_credits = 0
    total_points = 0.0

    print("==================================================")
    print("           OFFICIAL ACADEMIC TRANSCRIPT           ")
    print("==================================================")
    print(f"Student: {name} | ID: {student_id}")
    print("-" * 50)
    print(f"{'Course Code':<25} {'Credits':>7} {'Grade':>6} {'Points':>7}")
    print("-" * 50)

    # Iterate over enrolled courses
    for course, (credits, grade) in courses.items():
        # Compute quality points for this specific course
        pts = GRADE_POINTS.get(grade.upper(), 0.0) * credits
        total_credits += credits
        total_points += pts
        print(f"{course:<25} {credits:>7} {grade:>6} {pts:>7.1f}")

    # Guard against division by zero if student has 0 credits
    gpa = total_points / total_credits if total_credits > 0 else 0.0
    
    # Classify honors standing
    if gpa >= 3.8:
        standing = "Summa Cum Laude (Highest Honors)"
    elif gpa >= 3.5:
        standing = "Magna Cum Laude (High Honors)"
    elif gpa >= 3.0:
        standing = "Dean's List (Honors)"
    else:
        standing = "Good Standing"

    print("-" * 50)
    print(f"Total Credit Hours: {total_credits}")
    print(f"Cumulative GPA:     {gpa:.2f} / 4.00")
    print(f"Academic Standing:  {standing}")
    print("==================================================")

enrolled_courses = {
    "CS101: Intro to Python": (4, "A"),
    "MATH201: Calculus II": (4, "B"),
    "PHYS101: General Physics": (4, "A"),
    "ENG102: Tech Writing": (3, "A")
}
generate_transcript("STU-8821", "David Kim", enrolled_courses)
```
</details>

---

## 6. E-Commerce Inventory Reordering & Stock Alert Monitor

### 🏢 Real-Life Scenario
A fulfillment warehouse monitors SKU inventory levels. When stock falls below safety reorder thresholds, the engine flags items for purchase orders and computes reorder costs.

### 📋 Requirements
1. Dictionary storing inventory: `{"SKU": {"name": str, "stock": int, "reorder_point": int, "unit_cost": float}}`.
2. Identify all items where `stock <= reorder_point`.
3. Calculate quantity needed to restock to maximum capacity (e.g. 100 units) and total purchase order expenditure.

### 🎯 Expected Output
```text
==================================================
       WAREHOUSE INVENTORY REORDER AUDIT          
==================================================
CRITICAL RESTOCK ITEMS NEEDED:
  • [SKU-02] Wireless Ergonomic Mouse: Current Stock 8 <= Reorder Point 15
    -> Order 92 units @ $35.00/ea = $3,220.00
  • [SKU-04] USB-C Dual Hub: Current Stock 5 <= Reorder Point 20
    -> Order 95 units @ $45.00/ea = $4,275.00
--------------------------------------------------
Total Reorder Purchase Budget: $7,495.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 6: Warehouse Inventory Reordering Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. NESTED DICTIONARY SCHEMA: Stores structured SKU attributes (stock, threshold, cost).
# 2. REORDER HEURISTICS: Filters items where current_stock <= reorder_point.
# 3. PROCUREMENT BUDGETING: Computes target replenishment quantity and procurement expenditure.
# =====================================================================

INVENTORY = {
    "SKU-01": {"name": "Mechanical Keyboard", "stock": 45, "reorder_point": 20, "unit_cost": 85.00},
    "SKU-02": {"name": "Wireless Ergonomic Mouse", "stock": 8, "reorder_point": 15, "unit_cost": 35.00},
    "SKU-03": {"name": "4K UltraWide Monitor", "stock": 25, "reorder_point": 10, "unit_cost": 320.00},
    "SKU-04": {"name": "USB-C Dual Hub", "stock": 5, "reorder_point": 20, "unit_cost": 45.00},
}

def audit_reorder_levels(inventory: dict, target_capacity: int = 100) -> None:
    """Scans inventory thresholds, calculates restocking volumes, and outputs purchase orders."""
    print("==================================================")
    print("       WAREHOUSE INVENTORY REORDER AUDIT          ")
    print("==================================================")
    print("CRITICAL RESTOCK ITEMS NEEDED:")
    
    total_budget = 0.0
    for sku, data in inventory.items():
        # Check if stock has breached reorder safety threshold
        if data["stock"] <= data["reorder_point"]:
            needed_quantity = target_capacity - data["stock"]
            reorder_cost = needed_quantity * data["unit_cost"]
            total_budget += reorder_cost
            
            print(f"  • [{sku}] {data['name']}: Current Stock {data['stock']} <= Reorder Point {data['reorder_point']}")
            print(f"    -> Order {needed_quantity} units @ ${data['unit_cost']:.2f}/ea = ${reorder_cost:,.2f}")

    print("-" * 50)
    print(f"Total Reorder Purchase Budget: ${total_budget:,.2f}")
    print("==================================================")

audit_reorder_levels(INVENTORY)
```
</details>

---

## 7. Aviation Flight Manifest & Baggage Fee Dispatcher

### 🏢 Real-Life Scenario
An airline check-in counter calculates baggage fees based on passenger class, bag counts, and weight limits (First bag free for Business/First Class; Economy pays $30 for first bag, $40 for second bag; Overweight $> 50$ lbs incurs $50 penalty).

### 📋 Requirements
1. Passenger class: `"ECONOMY"`, `"BUSINESS"`, `"FIRST"`.
2. Compute baggage fees across a list of bag weights in lbs.

### 🎯 Expected Output
```text
==================================================
        AIRLINE PASSENGER BAGGAGE CHECK-IN        
==================================================
Passenger:   Eleanor Vance
Class:       ECONOMY
Bags Checked:2 pieces
--------------------------------------------------
  - Bag #1: 45.0 lbs -> Standard Fee: $30.00
  - Bag #2: 58.5 lbs -> Standard Fee: $40.00 + Overweight Fee: $50.00 ($90.00)
--------------------------------------------------
TOTAL BAGGAGE CHARGES: $120.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 7: Aviation Flight Baggage Fee Dispatcher
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. TRAVEL CLASS TARIFF RULES:
#    - ECONOMY: $30 for 1st bag, $40 for subsequent bags.
#    - BUSINESS / FIRST: 1st bag free, $35 for subsequent bags.
# 2. OVERWEIGHT CHARGES: Bags exceeding 50.0 lbs incur a flat $50.00 penalty.
# 3. ENUMERATE SEQUENCE PARSING: 1-indexed enumeration determines bag sequence order.
# =====================================================================

def calculate_baggage_fees(passenger: str, travel_class: str, bag_weights: list[float]) -> None:
    """Calculates checked baggage fees based on airline class tiers and weight limits."""
    travel_class = travel_class.upper()
    total_fee = 0.0
    fee_breakdown = []

    for idx, weight in enumerate(bag_weights, start=1):
        fee = 0.0
        details = []

        # Rule 1: Determine base allowance tariff by class
        if travel_class == "ECONOMY":
            base = 30.0 if idx == 1 else 40.0
            fee += base
            details.append(f"Standard Fee: ${base:.2f}")
        elif travel_class in {"BUSINESS", "FIRST"} and idx > 1:
            fee += 35.0
            details.append("Additional Bag Fee: $35.00")
        else:
            details.append("Complimentary Bag ($0.00)")

        # Rule 2: Check for overweight penalty (> 50 lbs)
        if weight > 50.0:
            fee += 50.0
            details.append("Overweight Fee: $50.00")

        total_fee += fee
        fee_breakdown.append((idx, weight, " + ".join(details), fee))

    # Render receipt
    print("==================================================")
    print("        AIRLINE PASSENGER BAGGAGE CHECK-IN        ")
    print("==================================================")
    print(f"Passenger:   {passenger}")
    print(f"Class:       {travel_class}")
    print(f"Bags Checked:{len(bag_weights)} pieces")
    print("-" * 50)
    for idx, wt, desc, f in fee_breakdown:
        print(f"  - Bag #{idx}: {wt:.1f} lbs -> {desc} (${f:.2f})")
    print("-" * 50)
    print(f"TOTAL BAGGAGE CHARGES: ${total_fee:,.2f}")
    print("==================================================")

calculate_baggage_fees("Eleanor Vance", "ECONOMY", [45.0, 58.5])
```
</details>

---

## 8. Personal Expense Tracker & Monthly Budget Forecaster

### 🏢 Real-Life Scenario
A financial planning utility takes user monthly expenses categorized by category (Housing, Food, Utilities, Transport, Entertainment), compares them against a budget, and reports variance.

### 📋 Requirements
1. Accept dictionary of actual expenses vs budget allocation.
2. Calculate total spend, savings rate from net income, and variance per category.

### 🎯 Expected Output
```text
==================================================
           MONTHLY BUDGET VARIANCE AUDIT          
==================================================
Net Monthly Income: $5,000.00
--------------------------------------------------
Category        Budgeted       Actual     Variance
--------------------------------------------------
Housing        $1,800.00    $1,800.00        $0.00
Food             $600.00      $750.00     +$150.00 (Over)
Utilities        $250.00      $220.00      -$30.00 (Under)
Transport        $400.00      $380.00      -$20.00 (Under)
Entertainment    $300.00      $450.00     +$150.00 (Over)
--------------------------------------------------
Total Expenses:   $3,600.00
Net Savings:      $1,400.00 (28.0% Savings Rate)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 8: Monthly Budget Variance & Wealth Accumulation Forecaster
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. DUAL-DICTIONARY RECONCILIATION: Aligns budgeted vs actual expenses by category key.
# 2. VARIANCE ANALYSIS: Computes numerical drift: actual - budgeted.
# 3. SAVINGS METRICS: Computes net savings (income - expenses) and savings percentage.
# =====================================================================

def audit_monthly_budget(net_income: float, budget: dict[str, float], actuals: dict[str, float]) -> None:
    """Performs financial variance analysis across budget categories."""
    total_actual = sum(actuals.values())
    savings = net_income - total_actual
    savings_rate = (savings / net_income * 100.0) if net_income > 0 else 0.0

    print("==================================================")
    print("           MONTHLY BUDGET VARIANCE AUDIT          ")
    print("==================================================")
    print(f"Net Monthly Income: ${net_income:,.2f}")
    print("-" * 50)
    print(f"{'Category':<14} {'Budgeted':>10} {'Actual':>12} {'Variance':>12}")
    print("-" * 50)

    # Reconcile each budgeted category
    for cat, b_val in budget.items():
        a_val = actuals.get(cat, 0.0)
        diff = a_val - b_val
        tag = "(Over)" if diff > 0 else ("(Under)" if diff < 0 else "")
        diff_str = f"+${diff:.2f}" if diff > 0 else (f"-${abs(diff):.2f}" if diff < 0 else "$0.00")
        print(f"{cat:<14} ${b_val:>9,.2f} ${a_val:>10,.2f} {diff_str:>12} {tag}")

    print("-" * 50)
    print(f"Total Expenses:   ${total_actual:>9,.2f}")
    print(f"Net Savings:      ${savings:>9,.2f} ({savings_rate:.1f}% Savings Rate)")
    print("==================================================")

budget_plan = {"Housing": 1800.0, "Food": 600.0, "Utilities": 250.0, "Transport": 400.0, "Entertainment": 300.0}
actual_spend = {"Housing": 1800.0, "Food": 750.0, "Utilities": 220.0, "Transport": 380.0, "Entertainment": 450.0}
audit_monthly_budget(5000.00, budget_plan, actual_spend)
```
</details>

---

## 9. Library Book Borrowing & Overdue Fine Calculation System

### 🏢 Real-Life Scenario
A municipal public library tracks book checkouts, due dates, and calculates overdue fines ($0.25/day for standard books; $1.00/day for high-demand reserve books; max fine $15.00).

### 📋 Requirements
1. Model `BookLoan` entity with `title`, `is_reserve`, and `days_kept`.
2. Compute overdue fines based on days checked out beyond the 14-day loan limit.

### 🎯 Expected Output
```text
==================================================
           MUNICIPAL LIBRARY FINE AUDIT           
==================================================
Patron: Marcus Vance | Card: LIB-4402
--------------------------------------------------
  • 'Python Distilled' (Standard) - 18 days (4 days overdue) -> Fine: $1.00
  • 'AI System Architecture' (Reserve) - 25 days (11 days overdue) -> Fine: $11.00
--------------------------------------------------
Total Outstanding Fines: $12.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 9: Municipal Library Overdue Fine Calculation Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. OOP MODELING: Encapsulates individual book loan parameters.
# 2. BOUNDARY CLAMPING:
#    - max(0, days - 14): Prevents negative overdue days for early returns.
#    - min(15.00, fine): Caps total liability per book to $15.00 maximum.
# =====================================================================

class BookLoan:
    """Represents a borrowed library book and its fine calculation rules."""
    def __init__(self, title: str, is_reserve: bool, days_kept: int):
        self.title = title
        self.is_reserve = is_reserve
        self.days_kept = days_kept

    def calculate_fine(self) -> tuple[int, float]:
        """Calculates overdue days beyond 14-day limit and applies rate caps."""
        # Standard loan period is 14 days
        overdue_days = max(0, self.days_kept - 14)
        
        # Reserve books incur $1.00/day, standard books $0.25/day
        rate = 1.00 if self.is_reserve else 0.25
        
        # Statutory statutory maximum fine cap is $15.00
        fine = min(15.00, overdue_days * rate)
        return overdue_days, fine

def process_patron_fines(patron: str, card_id: str, loans: list[BookLoan]) -> None:
    """Audits multiple patron book loans and aggregates outstanding fines."""
    print("==================================================")
    print("           MUNICIPAL LIBRARY FINE AUDIT           ")
    print("==================================================")
    print(f"Patron: {patron} | Card: {card_id}")
    print("-" * 50)
    
    total_fines = 0.0
    for loan in loans:
        days_late, fine = loan.calculate_fine()
        total_fines += fine
        tag = "Reserve" if loan.is_reserve else "Standard"
        print(f"  • '{loan.title}' ({tag}) - {loan.days_kept} days ({days_late} days overdue) -> Fine: ${fine:.2f}")

    print("-" * 50)
    print(f"Total Outstanding Fines: ${total_fines:.2f}")
    print("==================================================")

patron_loans = [
    BookLoan("Python Distilled", is_reserve=False, days_kept=18),
    BookLoan("AI System Architecture", is_reserve=True, days_kept=25)
]
process_patron_fines("Marcus Vance", "LIB-4402", patron_loans)
```
</details>

---

## 10. Gym Membership & Access Control Card Verification System

### 🏢 Real-Life Scenario
A 24-hour fitness center operates an RFID turnstile gate. The system checks member status (Active, Suspended, Expired) and access tier (Standard = Gym floor only; Premium = Gym + Spa + Pool).

### 📋 Requirements
1. Match member IDs against status and tier dictionaries.
2. Authorize or deny turnstile access based on requested facility zone.

### 🎯 Expected Output
```text
==================================================
        FITNESS ACCESS CONTROL GATE LOG           
==================================================
[ACCESS GRANTED] Elena Rostova (PREMIUM) -> Spa & Sauna Entry Approved.
[ACCESS DENIED]  David Kim (STANDARD) -> Spa & Sauna requires Premium tier!
[ACCESS DENIED]  Sarah Connor (EXPIRED) -> Membership expired! Please renew at reception.
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 10: RFID Facility Access Control Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. GUARD CLAUSES: Early-exit returns validate membership existence, account status,
#    and facility tier permissions hierarchically.
# 2. SET CONTAINMENT: Checks zone categories using O(1) set membership.
# =====================================================================

MEMBERS = {
    "RFID-01": {"name": "Elena Rostova", "tier": "PREMIUM", "status": "ACTIVE"},
    "RFID-02": {"name": "David Kim", "tier": "STANDARD", "status": "ACTIVE"},
    "RFID-03": {"name": "Sarah Connor", "tier": "PREMIUM", "status": "EXPIRED"},
}

def verify_facility_access(rfid: str, zone: str) -> None:
    """Evaluates RFID access credentials against facility zones."""
    member = MEMBERS.get(rfid)
    
    # Guard 1: Unknown card
    if not member:
        print(f"[ACCESS DENIED] Unknown RFID card '{rfid}'.")
        return

    # Guard 2: Inactive or expired account
    if member["status"] != "ACTIVE":
        print(f"[ACCESS DENIED]  {member['name']} ({member['status']}) -> Membership expired! Please renew at reception.")
        return

    # Guard 3: Tier permission mismatch for premium facilities
    if zone.upper() in {"SPA", "SAUNA", "POOL"} and member["tier"] != "PREMIUM":
        print(f"[ACCESS DENIED]  {member['name']} ({member['tier']}) -> Spa & Sauna requires Premium tier!")
        return

    # Access Granted
    print(f"[ACCESS GRANTED] {member['name']} ({member['tier']}) -> Spa & Sauna Entry Approved.")

print("==================================================")
print("        FITNESS ACCESS CONTROL GATE LOG           ")
print("==================================================")
verify_facility_access("RFID-01", "SPA")
verify_facility_access("RFID-02", "SPA")
verify_facility_access("RFID-03", "SPA")
print("==================================================")
```
</details>

---

## 11. Restaurant Table Reservation & Kitchen Order Queue

### 🏢 Real-Life Scenario
A restaurant management system books party reservations, assigns available tables, and tracks ordered kitchen tickets.

### 📋 Requirements
1. Tables: `Table 1 (2 seats)`, `Table 2 (4 seats)`, `Table 3 (6 seats)`.
2. Check capacity before assigning tables; reject if party size exceeds seats.

### 🎯 Expected Output
```text
==================================================
       RESTAURANT TABLE & KITCHEN DISPATCH        
==================================================
✅ Reserved Table 2 (Cap: 4) for Party 'Vance' (3 guests)
❌ Reservation Failed: Party 'Smith' (8 guests) exceeds max table capacity of 6!
--------------------------------------------------
ACTIVE KITCHEN ORDER: Table 2
  - 1x Truffle Pasta ($28.00)
  - 2x Wagyu Burger ($44.00)
Total Bill: $72.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 11: Restaurant Table & Kitchen Order Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. TABLE ALLOCATION HEURISTIC: Scans available tables to find the first unoccupied
#    table that satisfies capacity constraints (party_size <= table_capacity).
# 2. STATE MUTATION: Updates occupancy flags in-place.
# 3. KITCHEN ORDER GENERATOR: Aggregates ordered quantities and unit prices.
# =====================================================================

TABLES = {1: {"cap": 2, "occupied": False}, 2: {"cap": 4, "occupied": False}, 3: {"cap": 6, "occupied": False}}

def reserve_table(party_name: str, guests: int) -> int | None:
    """Finds an unoccupied table matching party size."""
    for t_id, data in TABLES.items():
        if not data["occupied"] and data["cap"] >= guests:
            data["occupied"] = True
            print(f"✅ Reserved Table {t_id} (Cap: {data['cap']}) for Party '{party_name}' ({guests} guests)")
            return t_id
    
    max_cap = max(d["cap"] for d in TABLES.values())
    print(f"❌ Reservation Failed: Party '{party_name}' ({guests} guests) exceeds max table capacity of {max_cap}!")
    return None

print("==================================================")
print("       RESTAURANT TABLE & KITCHEN DISPATCH        ")
print("==================================================")
assigned_table = reserve_table("Vance", 3)
reserve_table("Smith", 8) # Rejection simulation

if assigned_table:
    # Kitchen ticket simulation
    orders = [("Truffle Pasta", 1, 28.00), ("Wagyu Burger", 2, 22.00)]
    tot = sum(qty * price for _, qty, price in orders)
    print("-" * 50)
    print(f"ACTIVE KITCHEN ORDER: Table {assigned_table}")
    for item, qty, price in orders:
        print(f"  - {qty}x {item} (${qty * price:.2f})")
    print(f"Total Bill: ${tot:.2f}")
print("==================================================")
```
</details>

---

## 12. Payroll Salary & Tax Withholding Calculator

### 🏢 Real-Life Scenario
A corporate HR department processes bi-weekly employee payroll, computing gross wages, Federal tax withholding (15%), Social Security (6.2%), and Health Insurance deductions.

### 📋 Requirements
1. Annual salary $\to$ Bi-weekly gross pay ($\text{Salary} / 26$).
2. Compute federal tax, FICA, health insurance, and net deposit.

### 🎯 Expected Output
```text
==================================================
          EMPLOYEE BI-WEEKLY PAY STUB             
==================================================
Employee:        Elena Rostova
Gross Salary:    $120,000.00 / year ($4,615.38 / period)
--------------------------------------------------
DEDUCTIONS:
  - Federal Income Tax (15.0%):                  $692.31
  - Social Security FICA (6.2%):                 $286.15
  - Healthcare Insurance Plan:                   $150.00
--------------------------------------------------
NET DIRECT DEPOSIT:                            $3,486.92
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 12: Corporate Payroll & Statutory Withholding Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. BI-WEEKLY SCHEDULE: Divides annual gross salary by 26 corporate pay periods.
# 2. STATUTORY DEDUCTIONS: Calculates Federal Income Tax (15.0%) and FICA (6.2%).
# 3. NET DIRECT DEPOSIT: Subtracts statutory and healthcare deductions from gross pay.
# =====================================================================

def generate_paystub(name: str, annual_salary: float, health_deduction: float = 150.0) -> None:
    """Computes statutory payroll deductions and outputs an official pay stub."""
    # 26 pay periods per calendar year
    biweekly_gross = annual_salary / 26.0
    
    # Calculate withholdings
    fed_tax = biweekly_gross * 0.15
    fica = biweekly_gross * 0.062
    net_pay = biweekly_gross - (fed_tax + fica + health_deduction)

    print("==================================================")
    print("          EMPLOYEE BI-WEEKLY PAY STUB             ")
    print("==================================================")
    print(f"Employee:        {name}")
    print(f"Gross Salary:    ${annual_salary:,.2f} / year (${biweekly_gross:,.2f} / period)")
    print("-" * 50)
    print("DEDUCTIONS:")
    print(f"  - Federal Income Tax (15.0%):                  ${fed_tax:>8.2f}")
    print(f"  - Social Security FICA (6.2%):                 ${fica:>8.2f}")
    print(f"  - Healthcare Insurance Plan:                   ${health_deduction:>8.2f}")
    print("-" * 50)
    print(f"{'NET DIRECT DEPOSIT:':<40} ${net_pay:>8.2f}")
    print("==================================================")

generate_paystub("Elena Rostova", 120_000.00)
```
</details>

---

## 13. Car Rental Fleet Reservation & Mileage Fee Engine

### 🏢 Real-Life Scenario
A car rental agency rents vehicles (Sedan, SUV, Luxury) with a daily rate plus a mileage overage charge for miles driven beyond 100 miles/day ($0.25/mile).

### 📋 Requirements
1. Rates: `Sedan = $45/day`, `SUV = $75/day`, `Luxury = $130/day`.
2. Compute mileage overages and security deposit refunds.

### 🎯 Expected Output
```text
==================================================
          CAR RENTAL RETURN INVOICE               
==================================================
Renter:           David Kim
Vehicle:          SUV ($75.00/day)
Days Rented:      3 Days
Total Miles:      420.0 miles (Allowance: 300.0 miles)
--------------------------------------------------
Base Rental Cost:                              $225.00
Overage Mileage (120.0 mi @ $0.25/mi):          $30.00
Collision Damage Waiver ($15/day):              $45.00
--------------------------------------------------
TOTAL RENTAL CHARGES:                          $300.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 13: Car Rental Fleet & Mileage Surcharge Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. MILEAGE OVERAGE MATH: Uses max(0.0, miles - allowance) to guard against negative fees.
# 2. OPTIONAL WAIVERS: Evaluates Collision Damage Waiver ($15/day) add-on.
# =====================================================================

FLEET = {"Sedan": 45.0, "SUV": 75.0, "Luxury": 130.0}

def compute_rental_return(renter: str, model: str, days: int, miles: float, cdw: bool = True) -> None:
    """Calculates vehicle rental charges with mileage allowances and insurance options."""
    base_rate = FLEET[model]
    base_cost = base_rate * days
    
    # 100 miles allowed per day
    allowed_miles = days * 100.0
    extra_miles = max(0.0, miles - allowed_miles)
    mileage_fee = extra_miles * 0.25
    cdw_fee = (15.0 * days) if cdw else 0.0
    total = base_cost + mileage_fee + cdw_fee

    print("==================================================")
    print("          CAR RENTAL RETURN INVOICE               ")
    print("==================================================")
    print(f"Renter:           {renter}")
    print(f"Vehicle:          {model} (${base_rate:.2f}/day)")
    print(f"Days Rented:      {days} Days")
    print(f"Total Miles:      {miles:.1f} miles (Allowance: {allowed_miles:.1f} miles)")
    print("-" * 50)
    print(f"{'Base Rental Cost:':<40} ${base_cost:>8.2f}")
    print(f"{f'Overage Mileage ({extra_miles:.1f} mi @ $0.25/mi):':<40} ${mileage_fee:>8.2f}")
    print(f"{'Collision Damage Waiver ($15/day):':<40} ${cdw_fee:>8.2f}")
    print("-" * 50)
    print(f"{'TOTAL RENTAL CHARGES:':<40} ${total:>8.2f}")
    print("==================================================")

compute_rental_return("David Kim", "SUV", days=3, miles=420.0)
```
</details>

---

## 14. Real Estate Property Listing & Mortgage Filter Engine

### 🏢 Real-Life Scenario
A real estate agency filters listings based on client criteria (Max Price, Min Bedrooms, Min Bathrooms) and estimates monthly mortgage payments at current interest rates.

### 📋 Requirements
1. List of property dictionaries with `address`, `price`, `beds`, `baths`.
2. Filter matching properties and calculate estimated 30-year fixed mortgage payments.

### 🎯 Expected Output
```text
==================================================
         REAL ESTATE PROPERTY SEARCH ENGINE       
==================================================
Client Budget: Max $500,000 | Min 3 Beds
--------------------------------------------------
MATCHING PROPERTIES FOUND (2):
  1. 742 Evergreen Terrace - $380,000 (3 Bed / 2 Bath)
     -> Est. Monthly Mortgage (6.5% 30yr): $2,401.86/mo
  2. 104 Willow Lane - $465,000 (4 Bed / 3 Bath)
     -> Est. Monthly Mortgage (6.5% 30yr): $2,939.12/mo
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 14: Real Estate Listing Filter & Mortgage Amortization Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. MORTGAGE AMORTIZATION FORMULA: M = P * [r(1+r)^n] / [(1+r)^n - 1]
# 2. LIST COMPREHENSION FILTERING: Filters candidate records against multi-criteria bounds.
# =====================================================================

PROPERTIES = [
    {"address": "742 Evergreen Terrace", "price": 380_000.0, "beds": 3, "baths": 2},
    {"address": "104 Willow Lane", "price": 465_000.0, "beds": 4, "baths": 3},
    {"address": "12 Ocean Drive", "price": 850_000.0, "beds": 5, "baths": 4},
]

def calculate_mortgage(principal: float, rate_pct: float = 6.5, years: int = 30) -> float:
    """Computes monthly fixed mortgage payment using standard financial amortization."""
    monthly_rate = (rate_pct / 100.0) / 12.0
    total_months = years * 12
    return principal * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)

def filter_properties(max_price: float, min_beds: int) -> None:
    """Filters listings and displays estimated monthly financing costs."""
    matches = [p for p in PROPERTIES if p["price"] <= max_price and p["beds"] >= min_beds]
    
    print("==================================================")
    print("         REAL ESTATE PROPERTY SEARCH ENGINE       ")
    print("==================================================")
    print(f"Client Budget: Max ${max_price:,.0f} | Min {min_beds} Beds")
    print("-" * 50)
    print(f"MATCHING PROPERTIES FOUND ({len(matches)}):")
    for idx, p in enumerate(matches, start=1):
        m = calculate_mortgage(p["price"])
        print(f"  {idx}. {p['address']} - ${p['price']:,.0f} ({p['beds']} Bed / {p['baths']} Bath)")
        print(f"     -> Est. Monthly Mortgage (6.5% 30yr): ${m:,.2f}/mo")
    print("==================================================")

filter_properties(max_price=500_000.0, min_beds=3)
```
</details>

---

## 15. Warehouse Logistics Pallet Inventory & Space Allocator

### 🏢 Real-Life Scenario
A logistics warehouse manages 5 storage bays, tracking capacity limits (100 pallets per bay) and allocating inbound freight shipments across available bays.

### 📋 Requirements
1. Track bay occupancies in a dictionary.
2. Inbound shipment assigns to the first bay with sufficient capacity.

### 🎯 Expected Output
```text
==================================================
        WAREHOUSE BAY ALLOCATION ENGINE           
==================================================
Inbound Freight: 40 Pallets (Shipment #SHP-901)
  ✓ Assigned 40 pallets to Bay 1 (Occupancy: 85/100)
Inbound Freight: 50 Pallets (Shipment #SHP-902)
  ✓ Assigned 50 pallets to Bay 2 (Occupancy: 70/100)
Inbound Freight: 60 Pallets (Shipment #SHP-903)
  ✓ Assigned 60 pallets to Bay 3 (Occupancy: 60/100)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 15: Warehouse Bay Space Allocation Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. FIRST-FIT BIN PACKING: Iterates through warehouse bays in numerical order,
#    allocating cargo to the first bay where (current_load + shipment <= 100).
# 2. STATE MUTATION: Modifies bay occupancy values dynamically.
# =====================================================================

BAYS = {1: 45, 2: 20, 3: 0, 4: 0, 5: 0} # Bay ID -> Current Pallet Count (Max 100)

def allocate_pallets(shipment_id: str, count: int) -> bool:
    """Assigns inbound freight to the first bay with sufficient capacity."""
    for bay_id, current_load in BAYS.items():
        if current_load + count <= 100:
            BAYS[bay_id] += count
            print(f"Inbound Freight: {count} Pallets (Shipment #{shipment_id})")
            print(f"  ✓ Assigned {count} pallets to Bay {bay_id} (Occupancy: {BAYS[bay_id]}/100)")
            return True
            
    print(f"❌ Overflow: Insufficient space for shipment #{shipment_id} ({count} pallets)!")
    return False

print("==================================================")
print("        WAREHOUSE BAY ALLOCATION ENGINE           ")
print("==================================================")
allocate_pallets("SHP-901", 40)
allocate_pallets("SHP-902", 50)
allocate_pallets("SHP-903", 60)
print("==================================================")
```
</details>

---

## 16. Cinema Ticket Seat Booking & Dynamic Pricing System

### 🏢 Real-Life Scenario
A movie theater books tickets for seat tiers (Standard: $12.50, Premium Recliner: $18.50, VIP Box: $25.00) with matinee discounts (20% off before 5 PM) and popcorn concession combos.

### 📋 Requirements
1. Calculate ticket pricing based on seat type and showtime hour.
2. Add concessions and output ticket receipt.

### 🎯 Expected Output
```text
==================================================
             CINEMA BOX OFFICE TICKET             
==================================================
Movie:        Interstellar 4K IMAX
Showtime:     14:00 (Matinee 20% Discount Applied)
Seats:        2x Premium Recliner ($29.60)
Combos:       1x Large Popcorn & Soda ($12.00)
--------------------------------------------------
TOTAL CHARGED: $41.60
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 16: Box Office Dynamic Pricing & Concession Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. TIME-BASED MATINEE DISCOUNTS: Showtimes prior to 17:00 (5 PM) receive 20% off tickets.
# 2. COMPOSITE TOTALS: Sums seat tickets and concession combos into final total.
# =====================================================================

SEAT_PRICES = {"Standard": 12.50, "Premium Recliner": 18.50, "VIP Box": 25.00}

def book_movie_tickets(movie: str, hour_24: int, seat_type: str, seat_count: int, combo_count: int = 0) -> None:
    """Calculates ticket pricing with matinee discounts and concession totals."""
    unit_price = SEAT_PRICES[seat_type]
    is_matinee = hour_24 < 17
    
    # Apply 20% matinee discount if before 5 PM
    if is_matinee:
        unit_price *= 0.80

    tickets_total = unit_price * seat_count
    combos_total = combo_count * 12.00
    grand_total = tickets_total + combos_total

    print("==================================================")
    print("             CINEMA BOX OFFICE TICKET             ")
    print("==================================================")
    print(f"Movie:        {movie}")
    matinee_str = "(Matinee 20% Discount Applied)" if is_matinee else ""
    print(f"Showtime:     {hour_24:02d}:00 {matinee_str}")
    print(f"Seats:        {seat_count}x {seat_type} (${tickets_total:.2f})")
    if combo_count > 0:
        print(f"Combos:       {combo_count}x Large Popcorn & Soda (${combos_total:.2f})")
    print("-" * 50)
    print(f"TOTAL CHARGED: ${grand_total:.2f}")
    print("==================================================")

book_movie_tickets("Interstellar 4K IMAX", hour_24=14, seat_type="Premium Recliner", seat_count=2, combo_count=1)
```
</details>

---

## 17. Coffee Shop Drink Customizer & Loyalty Points Ledger

### 🏢 Real-Life Scenario
A specialty café prices beverages with size multipliers (Small x1.0, Medium x1.3, Large x1.6), custom dairy modifiers (Oat/Almond +$0.75), and rewards customers with 10 loyalty points per dollar spent.

### 📋 Requirements
1. Base drink menu: `Espresso = $3.50, Latte = $4.50, Cold Brew = $4.00`.
2. Compute final cost and awarded loyalty points.

### 🎯 Expected Output
```text
==================================================
           ROAST & BREW CAFE ORDER                
==================================================
Order:       Large Latte with Oat Milk
Base Price:  $4.50
Size Factor: 1.6x -> $7.20
Add-ons:     Oat Milk (+$0.75)
--------------------------------------------------
Total Paid:  $7.95
Loyalty Pts: +79 Points Earned (New Balance: 240 pts)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 17: Specialty Beverage Customizer & Loyalty Ledger
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. MULTI-FACTOR PRICING: Base drink price * size scaling factor + add-on modifications.
# 2. LOYALTY LEDGER: Computes integer loyalty points earned (10 pts per dollar spent).
# =====================================================================

SIZES = {"Small": 1.0, "Medium": 1.3, "Large": 1.6}
DRINKS = {"Espresso": 3.50, "Latte": 4.50, "Cold Brew": 4.00}

def order_coffee(drink: str, size: str, milk_alt: str = None, current_pts: int = 161) -> None:
    """Calculates custom drink pricing and updates customer loyalty points ledger."""
    base_price = DRINKS[drink]
    factor = SIZES[size]
    sized_price = base_price * factor
    alt_cost = 0.75 if milk_alt else 0.0
    total = sized_price + alt_cost
    
    # 10 loyalty points per dollar spent
    earned_pts = int(total * 10)
    new_pts = current_pts + earned_pts

    print("==================================================")
    print("           ROAST & BREW CAFE ORDER                ")
    print("==================================================")
    milk_str = f" with {milk_alt}" if milk_alt else ""
    print(f"Order:       {size} {drink}{milk_str}")
    print(f"Base Price:  ${base_price:.2f}")
    print(f"Size Factor: {factor}x -> ${sized_price:.2f}")
    if milk_alt:
        print(f"Add-ons:     {milk_alt} (+${alt_cost:.2f})")
    print("-" * 50)
    print(f"Total Paid:  ${total:.2f}")
    print(f"Loyalty Pts: +{earned_pts} Points Earned (New Balance: {new_pts} pts)")
    print("==================================================")

order_coffee("Latte", "Large", milk_alt="Oat Milk")
```
</details>

---

## 18. Emergency Hotline Dispatch & Incident Priority Logger

### 🏢 Real-Life Scenario
A municipal emergency response center ingests 911 dispatch calls, flags high-urgency keywords ("fire", "smoke", "weapon", "cardiac"), assigns responding service units (Police, Fire, EMS), and records incidents.

### 📋 Requirements
1. Scan call description text for high-priority emergency keywords.
2. Assign responding department based on keyword categorization.

### 🎯 Expected Output
```text
==================================================
         911 EMERGENCY DISPATCH CONSOLE           
==================================================
Incident:     INC-4910
Caller Text:  'Structure fire reported with heavy smoke in kitchen'
Severity:     🚨 CODE RED (HIGH PRIORITY)
Dispatching:  FIRE DEPARTMENT & RESCUE SQUAD
Status:       Units Dispatched en route (ETA: 4 mins)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 18: Emergency Dispatch Keyword Routing Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. STRING NORMALIZATION: text.lower() provides case-insensitive keyword inspection.
# 2. DOMAIN ROUTING: Directs incidents to Fire, Police, or EMS triage dispatchers.
# =====================================================================

def dispatch_emergency(inc_id: str, caller_notes: str) -> None:
    """Parses emergency caller text and routes dispatch units by domain keywords."""
    text_lower = caller_notes.lower()
    
    # Priority keyword evaluation
    if "fire" in text_lower or "smoke" in text_lower:
        unit = "FIRE DEPARTMENT & RESCUE SQUAD"
        sev = "🚨 CODE RED (HIGH PRIORITY)"
    elif "weapon" in text_lower or "robbery" in text_lower:
        unit = "POLICE TACTICAL PATROL"
        sev = "🚨 CODE RED (HIGH PRIORITY)"
    elif "cardiac" in text_lower or "breathing" in text_lower:
        unit = "PARAMEDIC EMS ADVANCED LIFE SUPPORT"
        sev = "🚨 CODE RED (HIGH PRIORITY)"
    else:
        unit = "COMMUNITY PATROL / NON-EMERGENCY"
        sev = "⚠️ CODE YELLOW (STANDARD)"

    print("==================================================")
    print("         911 EMERGENCY DISPATCH CONSOLE           ")
    print("==================================================")
    print(f"Incident:     {inc_id}")
    print(f"Caller Text:  '{caller_notes}'")
    print(f"Severity:     {sev}")
    print(f"Dispatching:  {unit}")
    print(f"Status:       Units Dispatched en route (ETA: 4 mins)")
    print("==================================================")

dispatch_emergency("INC-4910", "Structure fire reported with heavy smoke in kitchen")
```
</details>

---

## 19. Electric Vehicle (EV) Charging Station Billing & KWh Meter

### 🏢 Real-Life Scenario
An electric vehicle fast-charging network measures session kWh energy delivered, charging tiered rates based on on-peak vs off-peak hours ($0.45/kWh peak vs $0.28/kWh off-peak) and idle parking fees ($0.50/min if plugged in after charging completes).

### 📋 Requirements
1. Compute energy cost based on kWh delivered.
2. Add idle parking fees if vehicle remains plugged past 10-minute grace period.

### 🎯 Expected Output
```text
==================================================
        VOLTFLOW FAST CHARGE SESSION RECEIPT      
==================================================
Vehicle:          Tesla Model 3
Energy Delivered: 52.4 kWh @ $0.45/kWh (On-Peak)
Idle Time:        25 mins (15 mins billable @ $0.50/min)
--------------------------------------------------
Energy Charge:                                 $23.58
Idle Parking Surcharge:                         $7.50
Session Service Fee:                            $1.50
--------------------------------------------------
TOTAL SESSION AMOUNT:                          $32.58
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 19: Electric Vehicle Charging Station Meter & Billing Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. TIME-OF-USE ENERGY TARIFFS: $0.45/kWh on-peak vs $0.28/kWh off-peak.
# 2. COURTESY GRACE PERIOD: max(0, idle_mins - 10) gives 10 mins free before assessing parking fees.
# =====================================================================

def generate_ev_receipt(vehicle: str, kwh: float, is_peak: bool, idle_minutes: int) -> None:
    """Calculates EV charging session invoices with energy tariffs and idle fees."""
    rate = 0.45 if is_peak else 0.28
    energy_cost = kwh * rate
    
    # 10-minute courtesy grace period before idle penalty triggers
    billable_idle = max(0, idle_minutes - 10)
    idle_fee = billable_idle * 0.50
    total = energy_cost + idle_fee + 1.50 # $1.50 session infrastructure fee

    print("==================================================")
    print("        VOLTFLOW FAST CHARGE SESSION RECEIPT      ")
    print("==================================================")
    print(f"Vehicle:          {vehicle}")
    peak_str = "On-Peak" if is_peak else "Off-Peak"
    print(f"Energy Delivered: {kwh:.1f} kWh @ ${rate:.2f}/kWh ({peak_str})")
    print(f"Idle Time:        {idle_minutes} mins ({billable_idle} mins billable @ $0.50/min)")
    print("-" * 50)
    print(f"{'Energy Charge:':<40} ${energy_cost:>8.2f}")
    print(f"{'Idle Parking Surcharge:':<40} ${idle_fee:>8.2f}")
    print(f"{'Session Service Fee:':<40} $1.50")
    print("-" * 50)
    print(f"{'TOTAL SESSION AMOUNT:':<40} ${total:>8.2f}")
    print("==================================================")

generate_ev_receipt("Tesla Model 3", kwh=52.4, is_peak=True, idle_minutes=25)
```
</details>

---

## 20. Password Policy Compliance & Credential Vault Manager

### 🏢 Real-Life Scenario
An enterprise security tool evaluates user passwords against security rules (Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special character), calculates strength scores, and encrypts valid credentials in memory.

### 📋 Requirements
1. Check length $\ge 8$.
2. Check presence of uppercase, lowercase, digit, and special characters.
3. Assign strength: Score 5 = "Very Strong", 4 = "Strong", 3 = "Moderate", $\le 2$ = "Weak".

### 🎯 Expected Output
```text
==================================================
       ENTERPRISE PASSWORD POLICY AUDITOR         
==================================================
Credential Handle: admin@enterprise.com
Password Evaluated: 'Apex#2026Secure'
--------------------------------------------------
POLICY CRITERIA:
  [x] Minimum 8 characters (Length: 15)
  [x] Contains uppercase letter
  [x] Contains lowercase letter
  [x] Contains numeric digit
  [x] Contains special character (#, $, %, etc.)
--------------------------------------------------
COMPLIANCE STATUS:  ✅ APPROVED (Score: 5/5 - Very Strong)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 20: Enterprise Password Security Policy Auditor
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. CHARACTER SET SCANNERS: Uses any(...) generator expressions to inspect character sets.
# 2. BOOLEAN INTEGER ARITHMETIC: sum([bools]) computes clean numeric scores from 0 to 5.
# 3. AUDIT REPORTING: Displays itemized policy criteria checkmarks and compliance verdict.
# =====================================================================

def audit_password_security(user_handle: str, pwd: str) -> None:
    """Evaluates password complexity against enterprise security standards."""
    has_len = len(pwd) >= 8
    has_upper = any(c.isupper() for c in pwd)
    has_lower = any(c.islower() for c in pwd)
    has_digit = any(c.isdigit() for c in pwd)
    has_special = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in pwd)

    # Boolean sum computes numeric security score (0 to 5)
    score = sum([has_len, has_upper, has_lower, has_digit, has_special])
    strength_map = {5: "Very Strong", 4: "Strong", 3: "Moderate", 2: "Weak", 1: "Very Weak", 0: "Invalid"}
    strength = strength_map.get(score, "Weak")

    print("==================================================")
    print("       ENTERPRISE PASSWORD POLICY AUDITOR         ")
    print("==================================================")
    print(f"Credential Handle: {user_handle}")
    print(f"Password Evaluated: '{pwd}'")
    print("-" * 50)
    print("POLICY CRITERIA:")
    print(f"  [{'x' if has_len else ' '}] Minimum 8 characters (Length: {len(pwd)})")
    print(f"  [{'x' if has_upper else ' '}] Contains uppercase letter")
    print(f"  [{'x' if has_lower else ' '}] Contains lowercase letter")
    print(f"  [{'x' if has_digit else ' '}] Contains numeric digit")
    print(f"  [{'x' if has_special else ' '}] Contains special character (#, $, %, etc.)")
    print("-" * 50)
    status = "✅ APPROVED" if score >= 4 else "❌ REJECTED"
    print(f"COMPLIANCE STATUS:  {status} (Score: {score}/5 - {strength})")
    print("==================================================")

audit_password_security("admin@enterprise.com", "Apex#2026Secure")
```
</details>
