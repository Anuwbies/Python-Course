def daily_allowance(budget, days=5, reserve=0):
    """Return a whole-peso daily share under the documented valid limits."""
    return (budget - reserve) // days

print(daily_allowance(500))
print(daily_allowance(500, days=4, reserve=100))
