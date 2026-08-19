# Lesson 5: Loops & Iteration (`while`, `for`, `range`)

Repetition is at the heart of computational power. Loops allow software to execute instructions repeatedly across datasets, process streaming transactions, and create interactive user interfaces without duplicating code.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Construct condition-controlled `while` loops safely and avoid infinite loops.
2. Build interactive, menu-driven CLI loops with sentinel exit conditions.
3. Master sequence-controlled `for` loops and the `range()` generator.
4. Alter loop execution flow dynamically with `break` and `continue`.
5. Understand Python's unique `for...else` and `while...else` constructs.
6. Implement the 4 core algorithmic loop patterns: **Accumulator**, **Min/Max Tracker**, **Sentinel Loop**, and **Input Validation Loop**.

---

## 1. The `while` Loop (Condition-Controlled)

A `while` loop checks a boolean condition before each iteration and continues executing its indented block as long as that condition evaluates to `True`.

```python
# Anatomy of a while loop:
counter = 1                 # 1. Initialization

while counter <= 5:         # 2. Condition evaluation
    print(f"Cycle #{counter}")
    counter += 1            # 3. State update (CRUCIAL!)

print("Loop finished!")
```

> [!CAUTION]
> **The Infinite Loop Bug**:
> If you forget to update the loop condition variable inside the loop (`counter += 1`), the condition never becomes `False`, and your program will freeze in an infinite loop. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> in your terminal to forcefully terminate a stuck program.

---

## 2. The `for` Loop & `range()` (Sequence-Controlled)

The `for` loop in Python iterates directly over elements in an ordered sequence (such as a range of numbers, or characters in a string).

### The `range()` Generator
`range()` generates a sequence of integers on-the-fly without allocating memory for the entire list:

- `range(stop)`: Starts at `0`, increments by `1`, stops *before* `stop`.
- `range(start, stop)`: Starts at `start`, stops *before* `stop`.
- `range(start, stop, step)`: Increments by `step` (can be negative for countdowns).

```python
# 1. Standard count (0 to 4):
for i in range(5):
    print(f"Index: {i}")

# 2. Custom bounds (10 to 15):
for val in range(10, 16):
    print(f"Value: {val}")

# 3. Stepping by 5s (0, 5, 10, 15, 20):
for score in range(0, 25, 5):
    print(f"Milestone: {score}")

# 4. Counting backwards (5 down to 1):
for t in range(5, 0, -1):
    print(f"T-minus: {t}s")
print("🚀 Lift off!")

# 5. Iterating through characters in a string:
for char in "Python":
    print(f"Character: {char}")
```

---

## 3. Loop Control: `break` and `continue`

- **`break`**: Immediately terminates and exits the enclosing loop entirely.
- **`continue`**: Skips the remainder of the *current* iteration and jumps straight to the next loop cycle.

```python
# 'break' Example: Linear Search for Target ID
target_id = 42
for user_id in range(1, 100):
    if user_id == target_id:
        print(f"Target found: #{user_id}! Halting search.")
        break

# 'continue' Example: Filter out corrupted records
for packet_id in range(1, 10):
    if packet_id % 3 == 0:
        print(f"⚠️ Corrupted packet #{packet_id} skipped.")
        continue
    print(f"✅ Packet #{packet_id} processed successfully.")
```

---

## 4. Python's Unique `for...else` & `while...else`

In Python, loops can have an optional `else` block. The `else` block executes **only if the loop completes normally without encountering a `break`**:

```python
# Search for prime number divisor:
candidate = 17
for divisor in range(2, candidate):
    if candidate % divisor == 0:
        print(f"{candidate} is divisible by {divisor}. Not a prime.")
        break
else:
    # Runs ONLY if the loop never hit 'break':
    print(f"{candidate} is a PRIME number! 🌟")
```

---

## 5. Core Algorithmic Loop Patterns

### 1. The Accumulator Pattern (Totals & Averages):
```python
total_revenue = 0.0
transaction_count = 0

for sale in (120.50, 45.00, 89.90, 310.00):
    total_revenue += sale
    transaction_count += 1

average_sale = total_revenue / transaction_count
print(f"Total: ${total_revenue:.2f} | Average: ${average_sale:.2f}")
```

### 2. The Input Validation Loop:
```python
valid_port = False
while not valid_port:
    port = int(input("Enter network port (1024-65535): "))
    if 1024 <= port <= 65535:
        valid_port = True
        print(f"Port {port} bound successfully.")
    else:
        print("❌ Invalid port range. Please try again.")
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_05_Loops_And_Iteration.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_05_Loops_And_Iteration.py):

```python
# Compound Interest Investment Projection
initial_principal = float(input("Enter initial deposit ($): "))
annual_interest_rate = float(input("Enter annual interest rate (e.g. 0.07 for 7%): "))
years = int(input("Enter investment duration in years: "))

current_balance = initial_principal

print("\n--- Year-by-Year Growth ---")
for year in range(1, years + 1):
    interest_earned = current_balance * annual_interest_rate
    current_balance += interest_earned
    print(f"Year {year:>2}: +${interest_earned:>8.2f} interest | Balance: ${current_balance:>10.2f}")
```

---

## 📝 Quick Exercise: Interactive Banking ATM Terminal Session

### 🏢 Real-Life Scenario
You are developing the interactive terminal session manager for a commercial Automated Teller Machine (ATM). The user starts with an opening balance of `$1,500.00`. The ATM runs an event loop displaying a banking menu, processing deposits and withdrawals with robust balance validations, and printing an itemized session audit report upon logout.

### 📋 Requirements
1. Initialize session variables:
   - `balance = 1500.00`
   - `total_deposited = 0.00`
   - `total_withdrawn = 0.00`
   - `deposit_count = 0`
   - `withdrawal_count = 0`
   - `session_active = True`
2. Run a `while session_active:` loop displaying:
   ```text
   \n=== APEX SECURE ATM TERMINAL ===
   1. Check Balance
   2. Deposit Funds
   3. Withdraw Funds
   4. Exit & Print Session Audit
   ```
3. Process user choice (`input("Select option (1-4): ").strip()`):
   - **Option 1 (Check Balance)**:
     - Print `f"Current Available Balance: ${balance:,.2f}"`.
   - **Option 2 (Deposit)**:
     - Prompt for `amount` (`float`).
     - If `amount <= 0`: Print error `"[ERROR] Deposit amount must be greater than zero."` and `continue`.
     - Else: `balance += amount`, `total_deposited += amount`, `deposit_count += 1`, print success.
   - **Option 3 (Withdrawal)**:
     - Prompt for `amount` (`float`).
     - If `amount <= 0`: Print error `"[ERROR] Withdrawal amount must be greater than zero."` and `continue`.
     - If `amount > balance`: Print error `f"[ERROR] Insufficient Funds! Available: ${balance:,.2f}"` and `continue`.
     - Else: `balance -= amount`, `total_withdrawn += amount`, `withdrawal_count += 1`, print success.
   - **Option 4 (Exit)**:
     - Set `session_active = False` (or use `break`).
   - **Invalid Option**:
     - Print `"[ERROR] Invalid option. Please select 1, 2, 3, or 4."`
4. When the loop ends, output a comprehensive session audit report showing total deposits, total withdrawals, total transaction counts, net cash flow, and final balance.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 through 5 (variables, primitives, `input()`, `int()`, `float()`, string methods, arithmetic, comparisons, logic, `if`/`elif`/`else`, `while`, `for`, `range()`, `break`, `continue`, accumulator variables, f-strings, and `print()`). Do **not** use lists, dictionaries, or functions.

### 🎯 Sample Interactive Run
```text
=== APEX SECURE ATM TERMINAL ===
1. Check Balance
2. Deposit Funds
3. Withdraw Funds
4. Exit & Print Session Audit
Select option (1-4): 1
Current Available Balance: $1,500.00

=== APEX SECURE ATM TERMINAL ===
1. Check Balance
2. Deposit Funds
3. Withdraw Funds
4. Exit & Print Session Audit
Select option (1-4): 2
Enter deposit amount ($): 350.00
[SUCCESS] Deposited $350.00. New balance: $1,850.00

=== APEX SECURE ATM TERMINAL ===
1. Check Balance
2. Deposit Funds
3. Withdraw Funds
4. Exit & Print Session Audit
Select option (1-4): 3
Enter withdrawal amount ($): 200.00
[SUCCESS] Withdrew $200.00. Remaining balance: $1,650.00

=== APEX SECURE ATM TERMINAL ===
1. Check Balance
2. Deposit Funds
3. Withdraw Funds
4. Exit & Print Session Audit
Select option (1-4): 4

==================================================
              ATM SESSION AUDIT REPORT            
==================================================
Opening Balance:      $1,500.00
Total Deposits (1):  +$350.00
Total Withdrawals (1):-$200.00
Net Session Flow:    +$150.00
--------------------------------------------------
FINAL CLOSING BALANCE:$1,650.00
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Initialize session state variables
balance = 1500.00
total_deposited = 0.00
total_withdrawn = 0.00
deposit_count = 0
withdrawal_count = 0
session_active = True

# 2. Interactive event loop
while session_active:
    print("\n=== APEX SECURE ATM TERMINAL ===")
    print("1. Check Balance")
    print("2. Deposit Funds")
    print("3. Withdraw Funds")
    print("4. Exit & Print Session Audit")
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        print(f"\nCurrent Available Balance: ${balance:,.2f}")
        
    elif choice == "2":
        amount = float(input("Enter deposit amount ($): "))
        if amount <= 0.0:
            print("[ERROR] Deposit amount must be greater than zero.")
            continue
        balance += amount
        total_deposited += amount
        deposit_count += 1
        print(f"[SUCCESS] Deposited ${amount:,.2f}. New balance: ${balance:,.2f}")
        
    elif choice == "3":
        amount = float(input("Enter withdrawal amount ($): "))
        if amount <= 0.0:
            print("[ERROR] Withdrawal amount must be greater than zero.")
            continue
        if amount > balance:
            print(f"[ERROR] Insufficient Funds! Available: ${balance:,.2f}")
            continue
        balance -= amount
        total_withdrawn += amount
        withdrawal_count += 1
        print(f"[SUCCESS] Withdrew ${amount:,.2f}. Remaining balance: ${balance:,.2f}")
        
    elif choice == "4":
        session_active = False
        
    else:
        print("[ERROR] Invalid option. Please select 1, 2, 3, or 4.")

# 3. Post-session audit report
net_flow = total_deposited - total_withdrawn

print("\n==================================================")
print("              ATM SESSION AUDIT REPORT            ")
print("==================================================")
print(f"Opening Balance:      $1,500.00")
print(f"Total Deposits ({deposit_count}):  +${total_deposited:,.2f}")
print(f"Total Withdrawals ({withdrawal_count}):-${total_withdrawn:,.2f}")
print(f"Net Session Flow:    +${net_flow:,.2f}" if net_flow >= 0 else f"Net Session Flow:    -${abs(net_flow):,.2f}")
print("--------------------------------------------------")
print(f"FINAL CLOSING BALANCE:${balance:,.2f}")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **How many times will `for i in range(2, 11, 3):` execute?**
   - A) 4 times (`2, 5, 8, 11`)
   - B) 3 times (`2, 5, 8`)
   - C) 5 times
   - D) 3 times (`3, 6, 9`)

2. **What does the `continue` keyword do when encountered inside a loop?**
   - A) Terminates the loop permanently.
   - B) Skips the rest of the current iteration and starts the next iteration.
   - C) Restarts the loop from the initial condition.
   - D) Pauses execution for 1 second.

3. **When does the `else` block of a `for...else` statement execute?**
   - A) Every time the `for` condition evaluates to `False`.
   - B) Only when the loop finishes iterating all elements without hitting a `break`.
   - C) Only when an error occurs.
   - D) Whenever `break` is triggered.

<details>
<summary><b>View Answers</b></summary>
1: B (Values generated are 2, 5, 8. 11 is excluded because stop index is non-inclusive)<br>
2: B (continue skips the remainder of the current iteration)<br>
3: B (The loop else clause executes only upon natural completion without break)
</details>
