# Lesson 5: Loops & Iteration: `for`, `while` & Flow Control

Repetition is what makes computers so exceptionally powerful. An algorithm can execute a calculation billions of times without fatigue or error. In this lesson, you will master definite loops (`for`), indefinite loops (`while`), loop controls (`break`, `continue`), and loop `else` clauses.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Construct definite loops with `for` and the built-in `range()` generator.
2. Build indefinite, condition-driven `while` loops and sentinel-controlled input loops.
3. Master loop flow control using `break` and `continue`.
4. Understand and utilize Python's unique `for...else` and `while...else` construct.
5. Implement nested loops for multi-dimensional data grids and tabular calculations.

---

## 1. Definite Loops with `for` and `range()`

Use a `for` loop when the number of iterations is known before entering the loop.

The `range(start, stop, step)` function generates an arithmetic progression of integers:
- `range(stop)`: From `0` up to (but not including) `stop`.
- `range(start, stop)`: From `start` up to (not including) `stop`.
- `range(start, stop, step)`: Increments or decrements by `step`.

```python
# Counting 1 to 5:
for i in range(1, 6):
    print(f"Iteration #{i}")

# Stepping in increments of 5:
for score in range(0, 26, 5):
    print(score, end=" ") # 0 5 10 15 20 25
print()

# Stepping backwards (countdown):
for seconds in range(5, 0, -1):
    print(f"T-minus {seconds}...", end=" ")
print("LIFTOFF! 🚀")
```

---

## 2. Indefinite Loops with `while`

Use a `while` loop when an operation must repeat until a dynamic runtime condition changes:

```python
battery_charge = 15
print("Charging device...")

while battery_charge < 100:
    battery_charge += 25
    if battery_charge > 100:
        battery_charge = 100
    print(f"Charge level: {battery_charge}%")

print("Battery fully charged.")
```

---

## 3. Loop Flow Control: `break` and `continue`

- **`break`**: Immediately terminates the entire loop and jumps to the code following the loop block.
- **`continue`**: Immediately halts the current iteration and jumps to the start of the next iteration.

```python
# Skipping unhealthy nodes (continue) and stopping at critical alert (break):
for node_id in range(101, 110):
    if node_id == 104:
        print(f"Node {node_id}: Maintenance mode (Skipping).")
        continue # Skip rest of this loop iteration

    if node_id == 108:
        print(f"Node {node_id}: CRITICAL HARDWARE FAULT! Halting batch.")
        break # Exit the loop completely

    print(f"Node {node_id}: Health check PASS.")
```

---

## 4. The Python Loop `else` Clause

Python features a unique syntax where an `else` block can follow a `for` or `while` loop.

> [!NOTE]
> The loop `else` block executes **only if the loop completes normally without encountering a `break` statement**. If a `break` terminates the loop early, the `else` block is skipped.

```python
# Searching for a prime number or target key:
search_target = 42
numbers = range(10, 50)

for num in numbers:
    if num == search_target:
        print(f"Target {search_target} located!")
        break
else:
    print(f"Target {search_target} was not found in the search space.")
```

---

## 5. Sentinel-Controlled User Input Loops

In production CLI tools, loops are frequently kept running until the user types a sentinel word (such as `"exit"`, `"quit"`, or `"done"`):

```python
total_expenses = 0.0

while True:
    entry = input("Enter expense amount ($) or type 'done' to calculate: ").strip()
    if entry.lower() == "done":
        break
    
    amount = float(entry)
    if amount <= 0:
        print("Expense must be greater than zero.")
        continue
        
    total_expenses += amount

print(f"Total Logged Expenses: ${total_expenses:,.2f}")
```

---

## 💻 Code Example & Reference

The following real-life program models an **Automated Compound Interest & Retirement Wealth Projection Simulator**, combining all loop and control mechanics from this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Retirement Investment & Compound Growth Engine
# =====================================================================

print("=" * 70)
print(f"{'📈 FINANCIAL RETIREMENT & COMPOUND WEALTH PROJECTION ENGINE':^70}")
print("=" * 70)

# 1. Inputs & Input Validation Loop (Lessons 1, 2, 5)
while True:
    starting_principal = float(input("Enter Initial Investment Capital ($): "))
    if starting_principal >= 500.0:
        break
    print("❌ Minimum initial investment required is $500.00. Please re-enter.")

annual_contribution = float(input("Enter Annual Recurring Contribution ($): "))
annual_return_pct = float(input("Enter Estimated Annual Growth Rate (%) [e.g. 8.5]: "))
projection_years = int(input("Enter Horizon Duration in Years (1-40): "))
target_milestone = float(input("Enter Wealth Target Milestone ($) [e.g. 1000000]: "))

growth_multiplier = 1.0 + (annual_return_pct / 100.0)
current_balance = starting_principal
total_deposits = starting_principal
milestone_achieved_year = 0

# 2. Formatted Table Header (Lesson 1)
print("\n" + "=" * 70)
print(f"{'YEAR-BY-YEAR WEALTH ACCUMULATION SCHEDULE':^70}")
print("=" * 70)
print(f"{'Year':^6} | {'Start Balance':>14} | {'Interest Earned':>15} | {'End Balance':>15}")
print("-" * 70)

# 3. Iteration through projection years with range (Lesson 5)
for year in range(1, projection_years + 1):
    year_start = current_balance
    
    # Calculate investment return on starting balance
    interest_earned = year_start * (annual_return_pct / 100.0)
    
    # End of year: add interest + recurring contribution
    current_balance = year_start + interest_earned + annual_contribution
    total_deposits += annual_contribution
    
    # Check milestone (Lesson 4 & 5)
    if current_balance >= target_milestone and milestone_achieved_year == 0:
        milestone_achieved_year = year

    # Print yearly financial progress
    print(f"{year:^6} | {f'${year_start:,.2f}':>14} | {f'${interest_earned:,.2f}':>15} | {f'${current_balance:,.2f}':>15}")

# 4. Summary & Loop Completion Report
total_interest_gained = current_balance - total_deposits

print("=" * 70)
print(f"{'PORTFOLIO PERFORMANCE SUMMARY':^70}")
print("=" * 70)
print(f"{'Total Out-of-Pocket Deposits:':<35} ${total_deposits:,.2f}")
print(f"{'Total Compound Interest Gained:':<35} ${total_interest_gained:,.2f}")
print(f"{'Final Portfolio Value:':<35} ${current_balance:,.2f}")
print("-" * 70)

if milestone_achieved_year > 0:
    print(f"🎯 Milestone of ${target_milestone:,.2f} was successfully reached in Year {milestone_achieved_year}!")
else:
    print(f"ℹ️ Target of ${target_milestone:,.2f} requires additional years or higher contribution.")
print("=" * 70)
```

### 🔍 Code Explanation:
- **`while True` Validation Loop**: Protects against invalid starting deposits by repeatedly prompting until `starting_principal >= 500.0`.
- **`for year in range(...)`**: Accurately steps through each sequential financial year.
- **State Accumulators**: `current_balance` and `total_deposits` update incrementally with augmented arithmetic (`+=`).
- **Tabular f-string Layout**: Aligns financial figures across multiple columns cleanly.

---

## 📝 Quick Exercise: ATM Authentication & Interactive Banking Loop

### 🏢 Real-Life Scenario
You are developing the terminal control software for an automated teller machine (ATM). The user has a maximum of 3 attempts to enter the correct 4-digit security PIN (`"4829"`). Once authenticated, an interactive `while` loop presents an account menu allowing the user to check their balance, deposit funds, or withdraw funds until they choose to exit.

### 📋 Requirements
1. **Security PIN Gate**:
   - The correct PIN is `"4829"`.
   - Use a `for` loop with a maximum of 3 attempts.
   - If the user enters the correct PIN, print `"✅ PIN Accepted. Access Granted."` and `break`.
   - If incorrect, inform them how many attempts remain (`3 - attempt`).
   - Use the loop's `else` clause to display `"❌ Card Blocked: Maximum failed attempts exceeded."` and exit the program if all 3 attempts fail.
2. **Interactive Transaction Loop**:
   - Initial balance starts at `$1,250.00`.
   - Prompt with a menu:
     `"1: Check Balance | 2: Deposit | 3: Withdraw | 4: Exit"`
   - If `1`: Print formatted current balance.
   - If `2`: Prompt for deposit amount, ensure it is positive, and add to balance.
   - If `3`: Prompt for withdrawal amount; if positive and `<= balance`, deduct from balance; otherwise print an error.
   - If `4`: Print exit message and `break` the loop.
   - If invalid choice: Inform the user and `continue`.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1 through 5** (variables, types, input sanitization, type casting, arithmetic, compound conditionals, `for` loops, `range`, `while` loops, `break`, `continue`, loop `else`, and f-strings).

### 🎯 Expected Output
*(Assuming the user enters correct PIN on 1st try, deposits $250, withdraws $500, and exits)*

```text
==================================================
                 APEX BANK ATM                    
==================================================
Enter 4-Digit Security PIN (Attempt 1/3): 4829
✅ PIN Accepted. Access Granted.

--- ATM TRANSACTION MENU ---
1: Check Balance | 2: Deposit | 3: Withdraw | 4: Exit
Select option (1-4): 1
Current Account Balance: $1,250.00

--- ATM TRANSACTION MENU ---
1: Check Balance | 2: Deposit | 3: Withdraw | 4: Exit
Select option (1-4): 2
Enter deposit amount ($): 250.00
✅ Deposited $250.00. Updated Balance: $1,500.00

--- ATM TRANSACTION MENU ---
1: Check Balance | 2: Deposit | 3: Withdraw | 4: Exit
Select option (1-4): 3
Enter withdrawal amount ($): 500.00
✅ Dispensed $500.00. Remaining Balance: $1,000.00

--- ATM TRANSACTION MENU ---
1: Check Balance | 2: Deposit | 3: Withdraw | 4: Exit
Select option (1-4): 4
Thank you for banking with Apex Bank. Goodbye!
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Security Authentication Gate (Lessons 1-5)
CORRECT_PIN = "4829"
MAX_ATTEMPTS = 3
authenticated = False

print("==================================================")
print("                 APEX BANK ATM                    ")
print("==================================================")

for attempt in range(1, MAX_ATTEMPTS + 1):
    pin_input = input(f"Enter 4-Digit Security PIN (Attempt {attempt}/{MAX_ATTEMPTS}): ").strip()
    if pin_input == CORRECT_PIN:
        print("✅ PIN Accepted. Access Granted.")
        authenticated = True
        break
    else:
        remaining = MAX_ATTEMPTS - attempt
        if remaining > 0:
            print(f"❌ Invalid PIN. {remaining} attempt(s) remaining.")
else:
    print("❌ Card Blocked: Maximum failed attempts exceeded.")

# 2. Interactive Banking Loop (Lessons 1-5)
if authenticated:
    account_balance = 1250.00

    while True:
        print("\n--- ATM TRANSACTION MENU ---")
        print("1: Check Balance | 2: Deposit | 3: Withdraw | 4: Exit")
        choice = input("Select option (1-4): ").strip()

        if choice == "1":
            print(f"Current Account Balance: ${account_balance:,.2f}")
        elif choice == "2":
            deposit_amount = float(input("Enter deposit amount ($): "))
            if deposit_amount > 0:
                account_balance += deposit_amount
                print(f"✅ Deposited ${deposit_amount:,.2f}. Updated Balance: ${account_balance:,.2f}")
            else:
                print("❌ Invalid deposit amount.")
        elif choice == "3":
            withdraw_amount = float(input("Enter withdrawal amount ($): "))
            if 0 < withdraw_amount <= account_balance:
                account_balance -= withdraw_amount
                print(f"✅ Dispensed ${withdraw_amount:,.2f}. Remaining Balance: ${account_balance:,.2f}")
            else:
                print("❌ Insufficient funds or invalid withdrawal amount.")
        elif choice == "4":
            print("Thank you for banking with Apex Bank. Goodbye!")
            break
        else:
            print("❌ Invalid selection. Please choose an option from 1 to 4.")
```

**Explanation of the Solution:**
- The PIN verification uses `for attempt in range(1, 4)` and `break` upon correct entry, pairing with `for...else` to block the card if all attempts fail.
- The transaction engine uses `while True` to provide continuous banking services until user selection `"4"` initiates a graceful exit.
</details>
