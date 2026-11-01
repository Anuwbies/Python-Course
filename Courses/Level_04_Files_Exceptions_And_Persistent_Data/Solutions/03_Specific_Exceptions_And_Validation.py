def parse_amount(text):
    amount = int(text.strip())
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount

for text in ["0", "-1", "tea"]:
    try:
        amount = parse_amount(text)
    except ValueError:
        print("Rejected")
    else:
        print(f"Accepted: {amount}")
