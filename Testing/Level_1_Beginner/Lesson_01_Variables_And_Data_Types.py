"""
================================================================================
Level 1: Beginner Python
Lesson 1: Printing, Variables & Primitive Data Types
================================================================================
📝 Quick Exercise: Point of Sale (POS) Retail Receipt Generator

🏢 Real-Life Scenario:
You are developing the terminal checkout billing module for a modern retail electronics
store. When a customer purchases units of a product, the register calculates line item
totals, applies a loyalty member discount, adds shipping costs, and prints an itemized
customer receipt.

📋 Requirements:
1. Declare the following variables with appropriate types:
   - customer_name = "Eleanor Vance" (str)
   - item_name = "Noise-Cancelling Headphones" (str)
   - unit_price = 149.95 (float)
   - quantity = 2 (int)
   - is_loyalty_member = True (bool)
   - member_discount = 25.00 (float)
   - shipping_fee = 8.50 (float)
2. Compute:
   - subtotal = unit_price * quantity
   - final_total = subtotal - member_discount + shipping_fee
3. Using only f-strings and print(), output an itemized invoice formatted cleanly,
   with all monetary values formatted to 2 decimal places (:.2f).

⚠️ Strict Constraint:
Use ONLY concepts covered in Lesson 1 (variables, primitives, basic math operators,
f-strings, and print()). No input(), no if statements, no loops, no functions.
================================================================================
"""

# 1. Customer & Product Variables
customer_name = "Eleanor Vance"
item_name = "Noise-Cancelling Headphones"
unit_price = 149.95
quantity = 2
is_loyalty_member = True
member_discount = 25.00
shipping_fee = 8.50

# 2. Arithmetic Calculations
subtotal = unit_price * quantity
final_total = subtotal - member_discount + shipping_fee

# 3. Formatted POS Receipt Output
print("==================================================")
print("              APEX ELECTRONICS POS                ")
print("==================================================")
print(f"Customer:       {customer_name}")
print(f"Loyalty Member: {is_loyalty_member}")
print("--------------------------------------------------")
print(f"Item:           {item_name}")
print(f"Quantity:       {quantity}")
print(f"Unit Price:     ${unit_price:.2f}")
print(f"Subtotal:       ${subtotal:.2f}")
print(f"Member Disc:   -${member_discount:.2f}")
print(f"Shipping Fee:   ${shipping_fee:.2f}")
print("--------------------------------------------------")
print(f"FINAL TOTAL:    ${final_total:.2f}")
print("==================================================")
