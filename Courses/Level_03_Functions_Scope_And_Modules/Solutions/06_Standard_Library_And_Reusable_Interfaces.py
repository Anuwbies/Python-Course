from statistics import mean

def average_or_none(amounts):
    """Return an arithmetic mean, or None when no data exists."""
    if not amounts:
        return None
    return mean(amounts)

print(f"{average_or_none([10, 20, 30]):.2f}")
print(average_or_none([]))
