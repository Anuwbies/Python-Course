"""
================================================================================
Level 1: Beginner Python
Lesson 5: Loops & Iteration (while, for, range)
================================================================================
📝 Quick Exercise: Interactive Banking ATM Terminal Session

🏢 Real-Life Scenario:
You are developing the interactive terminal session manager for a commercial
Automated Teller Machine (ATM). The user starts with an opening balance of $1,500.00.
The ATM runs an event loop displaying a banking menu, processing deposits and
withdrawals with robust balance validations, and printing an itemized session
audit report upon logout.

📋 Requirements:
1. Initialize session variables:
   - balance = 1500.00, total_deposited = 0.00, total_withdrawn = 0.00
   - deposit_count = 0, withdrawal_count = 0, session_active = True
2. Run a while session_active: loop with menu options:
   1. Check Balance
   2. Deposit Funds (validate amount > 0)
   3. Withdraw Funds (validate amount > 0 and amount <= balance)
   4. Exit & Print Session Audit
3. Print an itemized session audit report upon logout.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-5 (variables, primitives, input(), int(),
float(), string methods, arithmetic, comparisons, logic, if/elif/else, while,
for, range(), break, continue, accumulator variables, f-strings, and print()).
No lists, dictionaries, or functions.
================================================================================
"""

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
