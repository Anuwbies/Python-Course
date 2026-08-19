"""
================================================================================
Level 1: Beginner Python
Lesson 4: Conditional Statements (if, elif, else)
================================================================================
📝 Quick Exercise: Commercial Loan & Credit Underwriting System

🏢 Real-Life Scenario:
You are developing the core automated risk assessment engine for a commercial
business lending fintech platform. The system evaluates loan applications based
on business registration status, years of operation, credit score, annual revenue,
and Debt-to-Income (DTI) ratio.

📋 Requirements:
1. Capture applicant details:
   - business_name (str, .strip().title())
   - business_status (str, .strip().lower())
   - years_in_business (float)
   - credit_score (int)
   - annual_revenue (float)
   - monthly_debt (float)
2. Compute financial ratios:
   - monthly_revenue = annual_revenue / 12.0
   - dti_ratio = (monthly_debt / monthly_revenue) * 100.0
3. Multi-branch underwriting logic:
   - If business_status != "active": Rejected (entity inactive)
   - Else if years_in_business < 1.0: Rejected (minimum 1 yr history)
   - Else if credit_score >= 740 and dti_ratio <= 30.0: Approved Tier 1 (5.25% rate, 25% credit line)
   - Else if 650 <= credit_score < 740 and dti_ratio <= 45.0: Approved Tier 2 (8.50% rate, 15% credit line)
   - Else if credit_score < 600 or dti_ratio > 50.0: Rejected (high risk)
   - Else: Manual Review (11.00% rate, 8% credit line)
4. Output structured underwriting report.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-4 (variables, primitives, input(), int(),
float(), string methods, arithmetic, comparisons, logic, if/elif/else,
f-strings, and print()). No loops, no lists, no functions.
================================================================================
"""

# 1. Capture and sanitize applicant inputs
business_name = input("Enter business name: ").strip().title()
business_status = input("Enter entity status (active/pending/suspended): ").strip().lower()
years_in_business = float(input("Enter years in operation: "))
credit_score = int(input("Enter principal credit score (300-850): "))
annual_revenue = float(input("Enter annual revenue ($): "))
monthly_debt = float(input("Enter total monthly debt payments ($): "))

# 2. Compute financial ratios
monthly_revenue = annual_revenue / 12.0
dti_ratio = (monthly_debt / monthly_revenue) * 100.0

# 3. Multi-branch underwriting logic
if business_status != "active":
    decision = "REJECTED: Business entity status is not active."
    interest_rate = 0.0
    max_credit_line = 0.0
elif years_in_business < 1.0:
    decision = "REJECTED: Minimum 1.0 year of operational history required."
    interest_rate = 0.0
    max_credit_line = 0.0
elif credit_score >= 740 and dti_ratio <= 30.0:
    decision = "APPROVED: Tier 1 Prime Business Line of Credit"
    interest_rate = 5.25
    max_credit_line = annual_revenue * 0.25
elif 650 <= credit_score < 740 and dti_ratio <= 45.0:
    decision = "APPROVED: Tier 2 Standard Commercial Facility"
    interest_rate = 8.50
    max_credit_line = annual_revenue * 0.15
elif credit_score < 600 or dti_ratio > 50.0:
    decision = "REJECTED: Subprime credit score or excessive debt burden."
    interest_rate = 0.0
    max_credit_line = 0.0
else:
    decision = "MANUAL REVIEW: Application flagged for Senior Committee review."
    interest_rate = 11.00
    max_credit_line = annual_revenue * 0.08

# 4. Formatted underwriting report
print("\n==================================================")
print("        COMMERCIAL LOAN UNDERWRITING REPORT       ")
print("==================================================")
print(f"Applicant:        {business_name}")
print(f"Entity Status:    {business_status} | Experience: {years_in_business:.1f} yrs")
print(f"Credit Score:     {credit_score}")
print(f"Annual Revenue:   ${annual_revenue:,.2f} (Monthly: ${monthly_revenue:,.2f})")
print(f"Monthly Debt:     ${monthly_debt:,.2f}")
print(f"Calculated DTI:   {dti_ratio:.2f}%")
print("--------------------------------------------------")
print(f"DECISION:         {decision}")
print(f"Interest Rate:    {interest_rate:.2f}%")
print(f"Max Credit Line:  ${max_credit_line:,.2f}")
print("==================================================")
