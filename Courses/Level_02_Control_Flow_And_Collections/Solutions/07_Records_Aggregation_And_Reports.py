expenses = [
    {"category": "food", "amount": 120},
    {"category": "travel", "amount": 30},
    {"category": "food", "amount": 80},
]
total = 0
by_category = {}
for expense in expenses:
    category = expense["category"]
    amount = expense["amount"]
    total = total + amount
    by_category[category] = by_category.get(category, 0) + amount
print(f"Total: PHP {total}")
for category in sorted(by_category):
    print(f"{category}: PHP {by_category[category]}")
