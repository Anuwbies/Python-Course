"""
================================================================================
Level 1: Beginner Python
Lesson 8: Functions & Scope
================================================================================
📝 Quick Exercise: Modular Enterprise Payroll & Deductions Suite

🏢 Real-Life Scenario:
You are developing the compensation calculation engine for an enterprise Human
Resources Management System (HRMS). The system requires a modular suite of
functions to calculate employee gross pay (including 1.5x overtime for hours
exceeding 40.0), calculate mandatory and elective payroll deductions (tax, 401k,
health insurance), and package an itemized payslip dictionary.

📋 Requirements:
1. calculate_gross_pay(hours_worked, hourly_rate, overtime_multiplier=1.5) -> float:
   - Calculates gross pay with 1.5x overtime pay for hours > 40.0.
2. calculate_deductions(gross_pay, tax_rate=0.18, retirement_rate=0.05, health_insurance=45.00) -> dict:
   - Computes income_tax, retirement_401k, health_insurance, total_deductions, net_pay.
3. generate_payslip(employee_name, employee_id, hours_worked, hourly_rate, **deduction_options) -> dict:
   - Integrates gross pay and deductions into a consolidated payslip dict.
4. Test with employee "Marcus Vance" (EMP-4081), 46.5 hours at $45.00/hr, retirement_rate=0.06.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-8 (variables, primitives, input(), numbers,
strings, conditionals, loops, lists, tuples, dictionaries, sets, def functions,
default parameters, *args, **kwargs, docstrings, type annotations, f-strings,
and print()). No file I/O, try/except, or classes.
================================================================================
"""

def calculate_gross_pay(hours_worked: float, hourly_rate: float, overtime_multiplier: float = 1.5) -> float:
    """Calculates total gross pay with 1.5x overtime for hours exceeding 40.0."""
    if hours_worked <= 40.0:
        gross = hours_worked * hourly_rate
    else:
        regular_pay = 40.0 * hourly_rate
        overtime_hours = hours_worked - 40.0
        overtime_pay = overtime_hours * (hourly_rate * overtime_multiplier)
        gross = regular_pay + overtime_pay
    return round(gross, 2)


def calculate_deductions(gross_pay: float, tax_rate: float = 0.18, retirement_rate: float = 0.05, health_insurance: float = 45.00) -> dict:
    """Calculates itemized payroll deductions and net take-home earnings."""
    income_tax = round(gross_pay * tax_rate, 2)
    retirement_401k = round(gross_pay * retirement_rate, 2)
    health_fee = round(health_insurance, 2)
    total_deductions = round(income_tax + retirement_401k + health_fee, 2)
    net_pay = round(gross_pay - total_deductions, 2)
    
    return {
        "income_tax": income_tax,
        "retirement_401k": retirement_401k,
        "health_insurance": health_fee,
        "total_deductions": total_deductions,
        "net_pay": net_pay
    }


def generate_payslip(employee_name: str, employee_id: str, hours_worked: float, hourly_rate: float, **deduction_options) -> dict:
    """Generates a complete consolidated employee payslip record."""
    gross_pay = calculate_gross_pay(hours_worked, hourly_rate)
    deductions = calculate_deductions(gross_pay, **deduction_options)
    
    return {
        "employee_name": employee_name,
        "employee_id": employee_id,
        "hours_worked": hours_worked,
        "hourly_rate": hourly_rate,
        "gross_pay": gross_pay,
        "deductions": deductions,
        "net_pay": deductions["net_pay"]
    }


# Test Execution
payslip = generate_payslip(
    employee_name="Marcus Vance",
    employee_id="EMP-4081",
    hours_worked=46.5,
    hourly_rate=45.00,
    retirement_rate=0.06
)

reg_hours = min(payslip["hours_worked"], 40.0)
ot_hours = max(payslip["hours_worked"] - 40.0, 0.0)
d = payslip["deductions"]

print("==================================================")
print("              APEX HR ENTERPRISE PAYSLIP          ")
print("==================================================")
print(f"Employee:         {payslip['employee_name']} (ID: {payslip['employee_id']})")
print(f"Hours Logged:     {payslip['hours_worked']:.2f} hrs ({reg_hours:.2f} reg + {ot_hours:.2f} OT)")
print(f"Hourly Base Rate: ${payslip['hourly_rate']:.2f}/hr")
print("--------------------------------------------------")
print(f"GROSS COMPENSATION: ${payslip['gross_pay']:,.2f}")
print("--------------------------------------------------")
print("PAYROLL DEDUCTIONS:")
print(f"- Income Tax (18%):  ${d['income_tax']:>8.2f}")
print(f"- 401(k) Plan (6%):  ${d['retirement_401k']:>8.2f}")
print(f"- Health Insurance:  ${d['health_insurance']:>8.2f}")
print(f"- Total Deductions:  ${d['total_deductions']:>8.2f}")
print("--------------------------------------------------")
print(f"NET TAKE-HOME PAY:  ${payslip['net_pay']:,.2f}")
print("==================================================")