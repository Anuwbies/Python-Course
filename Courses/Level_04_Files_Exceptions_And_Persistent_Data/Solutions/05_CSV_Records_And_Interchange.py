import csv
from pathlib import Path
from tempfile import TemporaryDirectory

def write_expenses(path, records):
    with open(path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["category", "amount"])
        writer.writeheader()
        writer.writerows(records)

def read_expenses(path):
    records = []
    with open(path, "r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["category", "amount"]:
            raise ValueError("Unexpected columns")
        for row in reader:
            if None in row or row.get("category") is None or row.get("amount") is None:
                raise ValueError("Missing or extra fields")
            category = row["category"].strip()
            amount = int(row["amount"])
            if not category or amount < 0:
                raise ValueError("Invalid expense")
            records.append({"category": category, "amount": amount})
    return records

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "expenses.csv"
        write_expenses(path, [{"category": "food, lunch", "amount": 120}])
        first = read_expenses(path)[0]
        print(f"Category: {first['category']}")
        print(f"Amount: {first['amount']}")
