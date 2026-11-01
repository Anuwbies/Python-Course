import json
from contextlib import contextmanager
from functools import wraps
from pathlib import Path
from tempfile import TemporaryDirectory

class RowError(ValueError):
    """A malformed JSON-lines expense record."""

def parse_rows(lines):
    for number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
            if not isinstance(record, dict) or set(record) != {"category", "amount"}:
                raise ValueError("Invalid fields")
            category = record["category"]
            amount = record["amount"]
            if not isinstance(category, str) or not category.strip():
                raise ValueError("Invalid category")
            if type(amount) is not int or amount < 0:
                raise ValueError("Invalid amount")
        except ValueError as error:
            raise RowError(f"Invalid record at line {number}") from error
        yield {"category": category.strip().lower(), "amount": amount}

@contextmanager
def open_rows(path):
    with open(path, "r", encoding="utf-8") as handle:
        yield parse_rows(handle)

def completed_calls(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        wrapper.calls += 1
        return result
    wrapper.calls = 0
    return wrapper

@completed_calls
def summarize(records):
    totals = {}
    for record in records:
        category = record["category"]
        totals[category] = totals.get(category, 0) + record["amount"]
    return totals

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "expenses.jsonl"
        path.write_text('\n'.join([
            json.dumps({"category": "food", "amount": 120}),
            json.dumps({"category": "travel", "amount": 30}),
            json.dumps({"category": "food", "amount": 80}),
        ]) + '\n', encoding="utf-8")
        with open_rows(path) as records:
            totals = summarize(records)
        for category in sorted(totals):
            print(f"{category}: PHP {totals[category]}")
        print(f"Completed calls: {summarize.calls}")
