"""
================================================================================
Level 1: Beginner Python
Lesson 2: User Input & Type Casting
================================================================================
📝 Quick Exercise: Freelance Billing & Invoice Calculator

🏢 Real-Life Scenario:
You are building an automated invoicing utility for freelance software consultants.
The program prompts the consultant for client details, hourly billing rate,
billable project hours, and any software/cloud infrastructure expenses incurred.
It then calculates the labor subtotal, total invoice amount, estimated income tax
withholding, and expected net earnings.

📋 Requirements:
1. Capture and sanitize text inputs:
   - client_name: Prompt with "Enter client business name: ", formatted with .strip().title()
   - project_title: Prompt with "Enter project title: ", formatted with .strip()
2. Capture and cast numeric inputs:
   - hourly_rate: Prompt with "Enter hourly billing rate ($): ", cast to float
   - hours_worked: Prompt with "Enter total billable hours: ", cast to float
   - expenses: Prompt with "Enter cloud/hardware expenses incurred ($): ", cast to float
3. Perform calculations:
   - labor_cost = hourly_rate * hours_worked
   - invoice_total = labor_cost + expenses
   - tax_withholding = invoice_total * 0.22
   - net_earnings = invoice_total - tax_withholding
4. Output a formatted invoice summary with values rounded to 2 decimal places.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1 and 2 (variables, primitives, input(), int(),
float(), str(), string methods, basic arithmetic, f-strings, and print()).
No if statements, no loops, no functions.
================================================================================
"""

# 1. Capture and sanitize text inputs
client_name = input("Enter client business name: ").strip().title()
project_title = input("Enter project title: ").strip()

# 2. Capture and cast numeric inputs
hourly_rate = float(input("Enter hourly billing rate ($): "))
hours_worked = float(input("Enter total billable hours: "))
expenses = float(input("Enter cloud/hardware expenses incurred ($): "))

# 3. Perform calculations
labor_cost = hourly_rate * hours_worked
invoice_total = labor_cost + expenses
tax_withholding = invoice_total * 0.22
net_earnings = invoice_total - tax_withholding

# 4. Formatted invoice display
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
