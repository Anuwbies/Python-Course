def daily_allowance(budget: int, days: int) -> int | None:
    if budget < 0 or days <= 0:
        return None
    return budget // days

if __name__ == "__main__":
    print(daily_allowance(500, 5))
    print(daily_allowance(500, 0))
