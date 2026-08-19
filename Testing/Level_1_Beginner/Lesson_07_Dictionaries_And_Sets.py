"""
================================================================================
Level 1: Beginner Python
Lesson 7: Dictionaries & Sets
================================================================================
📝 Quick Exercise: E-Commerce Cart & Category Analytics Tracker

🏢 Real-Life Scenario:
You are developing the shopping cart analytics module for an online computer
hardware store. When a customer completes checkout, the system receives a raw list
of scanned item slugs. The program calculates item quantities, looks up prices from
a catalog dictionary to generate an itemized bill, determines unique items
purchased using sets, and cross-references category sets for promo eligibility.

📋 Requirements:
1. Declare collections:
   - catalog = {"laptop": 999.99, "mouse": 29.50, "keyboard": 79.00, "monitor": 249.99, "usb_hub": 19.95}
   - scanned_cart = ["laptop", "mouse", "keyboard", "mouse", "usb_hub", "mouse", "monitor"]
   - peripherals = {"mouse", "keyboard", "monitor", "usb_hub"}
   - promo_eligible = {"mouse", "usb_hub", "keyboard"}
2. Count item frequencies into item_counts using .get().
3. Calculate invoice totals and display itemized lines.
4. Set operations for category and promo analysis:
   - unique_purchased = set(scanned_cart)
   - purchased_peripherals = unique_purchased & peripherals
   - promotional_items = unique_purchased & promo_eligible
   - standard_items = unique_purchased - promo_eligible
5. Print receipt and analytics breakdown.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-7 (variables, primitives, input(), numbers,
strings, conditionals, loops, lists, tuples, dictionaries, dict methods, sets,
set operators, f-strings, and print()). No functions (def), files, or classes.
================================================================================
"""

# 1. Product catalog, cart stream, and department sets
catalog = {
    "laptop": 999.99,
    "mouse": 29.50,
    "keyboard": 79.00,
    "monitor": 249.99,
    "usb_hub": 19.95
}

scanned_cart = ["laptop", "mouse", "keyboard", "mouse", "usb_hub", "mouse", "monitor"]

peripherals = {"mouse", "keyboard", "monitor", "usb_hub"}
promo_eligible = {"mouse", "usb_hub", "keyboard"}

# 2. Count item frequencies using dictionary .get()
item_counts = {}
for item in scanned_cart:
    item_counts[item] = item_counts.get(item, 0) + 1

# 3. Calculate invoice totals and display itemized lines
grand_total = 0.0
total_units = len(scanned_cart)

print("==================================================")
print("           APEX HARDWARE CHECKOUT AUDIT           ")
print("==================================================")
print("ITEMIZED RECEIPT:")

for item, count in item_counts.items():
    unit_price = catalog.get(item, 0.0)
    line_total = unit_price * count
    grand_total += line_total
    print(f"- {item.capitalize():<18}: {count} x ${unit_price:>6.2f} = ${line_total:>8.2f}")

print("--------------------------------------------------")
print(f"Total Units Scanned:  {total_units} items")
print(f"GRAND TOTAL INVOICE:  ${grand_total:,.2f}")
print("--------------------------------------------------")

# 4. Set operations for category and promo analysis
unique_purchased = set(scanned_cart)
purchased_peripherals = unique_purchased & peripherals
promotional_items = unique_purchased & promo_eligible
standard_items = unique_purchased - promo_eligible

print("CATEGORY & PROMO ANALYSIS:")
print(f"Unique Products:      {len(unique_purchased)} types")
print(f"Peripherals Bought:   {purchased_peripherals}")
print(f"Promo Discount Items: {promotional_items}")
print(f"Standard Price Items: {standard_items}")
print("==================================================")