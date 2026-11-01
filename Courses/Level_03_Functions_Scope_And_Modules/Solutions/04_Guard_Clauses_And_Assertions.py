def daily_allowance(budget, days=5, reserve=0):
    """Return a whole-unit share or None for invalid numeric limits."""
    if budget < 0 or reserve < 0 or reserve > budget or days <= 0:
        return None
    return (budget - reserve) // days

assert daily_allowance(500) == 100
assert daily_allowance(100, reserve=100) == 0
assert daily_allowance(100, days=0) is None
assert daily_allowance(100, reserve=101) is None
print("Allowance examples passed")
