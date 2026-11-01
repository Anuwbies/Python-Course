def add_amount(amount, amounts=None):
    """Return a new outer list; omitted collections start independently."""
    if amounts is None:
        amounts = []
    updated = amounts.copy()
    updated.append(amount)
    return updated

print(add_amount(10))
print(add_amount(20))
original = [120, 80]
print(add_amount(50, original))
print(original)
