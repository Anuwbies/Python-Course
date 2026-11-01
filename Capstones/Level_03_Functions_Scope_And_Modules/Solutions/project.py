def add_expense(records, category, amount):
    category = category.strip().lower()
    if not category or amount < 0:
        return None
    updated = records.copy()
    updated.append({"category": category, "amount": amount})
    return updated


def summarize(records):
    total = 0
    by_category = {}
    for record in records:
        category = record["category"]
        amount = record["amount"]
        total = total + amount
        by_category[category] = by_category.get(category, 0) + amount
    return {"count": len(records), "total": total, "by_category": by_category}


def print_summary(summary):
    print(f"Entries: {summary['count']}")
    print(f"Total: PHP {summary['total']}")
    for category in sorted(summary["by_category"]):
        print(f"{category}: PHP {summary['by_category'][category]}")


if __name__ == "__main__":
    original = []
    first = add_expense(original, " FOOD ", 120)
    updated = add_expense(first, "travel", 30)
    assert original == []
    assert summarize([]) == {"count": 0, "total": 0, "by_category": {}}
    assert add_expense(original, "", 10) is None
    assert add_expense(original, "food", -1) is None
    print(f"Original entries: {len(original)}")
    print_summary(summarize(updated))
