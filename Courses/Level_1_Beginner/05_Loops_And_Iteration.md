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

---

## 6. Under the Hood: The Iterator Protocol (`iter()` and `next()`)

How does Python actually execute a `for item in collection:` loop under the hood?

When Python encounters a `for` loop, it:
1. Calls `iter(collection)` to request an iterator object.
2. Repeatedly calls `next(iterator)` on every turn to fetch the next element.
3. Automatically catches the `StopIteration` exception to terminate the loop cleanly.

```python
# What you write:
fruits = ["Apple", "Banana"]
for f in fruits:
    print(f)

# What Python executes under the hood:
iterator = iter(fruits)
while True:
    try:
        f = next(iterator)
        print(f)
    except StopIteration:
        break # Clean loop termination
```

---

## 7. Pythonic Iteration Helpers: `enumerate()` and `zip()`

### 1. `enumerate()`: Tracking Index & Value Cleanly
Avoid initializing manual counter variables (`i = 0` ... `i += 1`). Use `enumerate()`:

```python
servers = ["web-01", "web-02", "db-primary", "cache-01"]

for rank, server in enumerate(servers, start=1):
    print(f"Node #{rank}: {server}")
```

### 2. `zip()`: Parallel Synchronized Iteration
Iterate over multiple collections in lockstep simultaneously:

```python
users = ["Alice", "Bob", "Charlie"]
roles = ["Admin", "Developer", "Analyst"]
access_tiers = [1, 2, 3]

# In Python 3.10+, strict=True guarantees ValueError if lengths mismatch
for name, role, tier in zip(users, roles, access_tiers, strict=True):
    print(f"User: {name:<10} | Role: {role:<12} | Clearance: Tier {tier}")
```
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

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master definite loops, while loops, loop flow controls (`break`, `continue`), `for-else`, `enumerate`, and `zip`:

---

### 🟢 Tier 1: Definite Loops & Range Mechanics (Exercises 1–3)

#### 🔹 Exercise 1: Multiples of Three Counter
* **Goal**: Write a `for` loop that iterates from 3 to 30 (inclusive) in steps of 3 and prints each number on a single line separated by spaces.

#### 🔹 Exercise 2: Cumulative Sum Accumulator
* **Goal**: Compute the sum of all integers from 1 to 100 using a `for` loop and an accumulator variable `total_sum`. Print the final sum (`5050`).

#### 🔹 Exercise 3: Dynamic Countdown Timer
* **Goal**: Prompt for integer `start_seconds`. Use a `for` loop stepping downwards (`-1`) to print `T-minus X...` ending with `"BLASTOFF!"`.

---

### 🟡 Tier 2: While Loops & Sentinel Controls (Exercises 4–6)

#### 🔹 Exercise 4: Number Guessing Game (Binary Search Logic)
* **Goal**: Secret number is `42`.
* **Requirement**: Use `while True` to prompt the user for a guess. Give `"Too High"`, `"Too Low"`, or `"Correct!"` feedback. Break on correct answer and report total attempts.

#### 🔹 Exercise 5: Continuous Expense Ingestion Sentinel Loop
* **Goal**: Continuously prompt for expense amounts until user enters `"done"`.
* **Requirement**: Ignore negative amounts (`continue`), sum valid numbers, and print total count and total amount when finished.

#### 🔹 Exercise 6: Prime Number Search with `for...else`
* **Goal**: Given integer `n = 29`.
* **Requirement**: Use a `for divisor in range(2, int(n**0.5) + 1):` loop to test divisibility. If divisible, print composite and `break`. Use the loop's `else` clause to print that `n` is prime!

---

### 🟠 Tier 3: Enumerate, Zip & Nested Iteration (Exercises 7–9)

#### 🔹 Exercise 7: Leaderboard Ranker with `enumerate()`
* **Goal**: Given `runners = ["Kipchoge", "Bekele", "Cheptegei", "Farah"]`.
* **Requirement**: Print each runner with their 1-indexed podium place using `enumerate(runners, start=1)`.

#### 🔹 Exercise 8: Multi-Sensor Alignment with `zip(strict=True)`
* **Goal**: Given lists `timestamps = ["12:00", "12:05", "12:10"]`, `temps = [21.5, 22.1, 23.0]`, and `pressures = [1013, 1012, 1015]`.
* **Requirement**: Use `zip()` to iterate and print formatted synchronized readings.

#### 🔹 Exercise 9: Multiplication Matrix Generator (Nested Loops)
* **Goal**: Use nested `for` loops to print a formatted 1 to 5 multiplication grid table.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: ATM Authentication & Interactive Banking Engine
* **Goal**: Multi-attempt PIN gate using `for...else` followed by continuous stateful transaction menu loop with balance tracking.

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
<summary><b>🔍 View Exercise Solutions (ATM & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Apex Bank ATM Engine
# =====================================================================
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

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
for n in range(3, 31, 3): print(n, end=" ")
print()

# Ex 2:
total_sum = sum(range(1, 101))
print(f"Total Sum: {total_sum}")

# Ex 3:
sec = int(input("Start seconds: "))
for s in range(sec, 0, -1): print(f"T-minus {s}...")
print("BLASTOFF!")

# Ex 4:
secret, attempts = 42, 0
while True:
    guess = int(input("Guess: "))
    attempts += 1
    if guess == secret:
        print(f"Correct in {attempts} attempts!")
        break
    elif guess < secret: print("Too Low")
    else: print("Too High")

# Ex 5:
tot, cnt = 0.0, 0
while True:
    e = input("Expense (or 'done'): ").strip().lower()
    if e == "done": break
    val = float(e)
    if val <= 0: continue
    tot += val
    cnt += 1
print(f"Total: ${tot:.2f} across {cnt} entries")

# Ex 6:
n = 29
for d in range(2, int(n**0.5) + 1):
    if n % d == 0:
        print(f"{n} is composite")
        break
else:
    print(f"{n} is PRIME!")

# Ex 7:
runners = ["Kipchoge", "Bekele", "Cheptegei", "Farah"]
for place, name in enumerate(runners, start=1):
    print(f"Place #{place}: {name}")

# Ex 8:
ts = ["12:00", "12:05", "12:10"]
t = [21.5, 22.1, 23.0]
p = [1013, 1012, 1015]
for time_str, temp, press in zip(ts, t, p):
    print(f"[{time_str}] Temp: {temp}°C, Pressure: {press} hPa")

# Ex 9:
for r in range(1, 6):
    for c in range(1, 6):
        print(f"{r * c:>4}", end=" ")
    print()
```
</details>
