def total_expenses(amounts):
    """Return the total without changing the input list."""
    total = 0
    for amount in amounts:
        total = total + amount
    return total

print(total_expenses([120, 80, 50]))
print(total_expenses([]))
