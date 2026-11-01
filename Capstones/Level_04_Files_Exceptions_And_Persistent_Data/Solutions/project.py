import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

def validate_records(value):
    if not isinstance(value, list):
        raise ValueError("Expenses must be a list")
    valid = []
    for record in value:
        if not isinstance(record, dict) or set(record) != {"category", "amount"}:
            raise ValueError("Invalid expense fields")
        category = record["category"]
        amount = record["amount"]
        if not isinstance(category, str) or not category.strip():
            raise ValueError("Invalid category")
        if type(amount) is not int or amount < 0:
            raise ValueError("Invalid amount")
        valid.append({"category": category.strip().lower(), "amount": amount})
    return valid


def load_expenses(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            document = json.load(handle)
    except FileNotFoundError:
        return []
    if not isinstance(document, dict) or set(document) != {"version", "expenses"}:
        raise ValueError("Invalid document")
    if type(document["version"]) is not int or document["version"] != 1:
        raise ValueError("Unsupported version")
    return validate_records(document["expenses"])


def save_expenses(path, records):
    document = {"version": 1, "expenses": validate_records(records)}
    text = json.dumps(document, ensure_ascii=False, indent=2)
    path = Path(path)
    candidate = None
    try:
        with NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            candidate = Path(handle.name)
            handle.write(text)
        candidate.replace(path)
    finally:
        if candidate is not None:
            candidate.unlink(missing_ok=True)


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "expenses.json"
        print(f"Missing entries: {len(load_expenses(path))}")
        records = [{"category": " FOOD ", "amount": 120}, {"category": "travel", "amount": 30}]
        save_expenses(path, records)
        loaded = load_expenses(path)
        print(f"Entries: {len(loaded)}")
        total = 0
        for record in loaded:
            total = total + record["amount"]
        print(f"Total: PHP {total}")
        try:
            save_expenses(path, [{"category": "food", "amount": -1}])
        except ValueError:
            print("Invalid save rejected")
        print(f"Preserved: {load_expenses(path) == loaded}")
