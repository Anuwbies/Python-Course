expenses = []
while True:
    print("Command (add/summary/quit):")
    command = input().strip().lower()
    if command == "quit":
        print("Goodbye")
        break
    elif command == "add":
        print("Category:")
        category = input().strip().lower()
        print("Amount (whole PHP):")
        amount = int(input())
        if category == "" or amount < 0:
            print("Rejected")
        else:
            expenses.append({"category": category, "amount": amount})
            print("Added")
    elif command == "summary":
        total = 0
        by_category = {}
        for expense in expenses:
            category = expense["category"]
            amount = expense["amount"]
            total = total + amount
            by_category[category] = by_category.get(category, 0) + amount
        print(f"Entries: {len(expenses)}")
        print(f"Total: PHP {total}")
        for category in sorted(by_category):
            print(f"{category}: PHP {by_category[category]}")
    else:
        print("Unknown command")
