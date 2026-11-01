import json
from pathlib import Path
from tempfile import TemporaryDirectory

def validate_amounts(value):
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    for amount in value:
        if type(amount) is not int or amount < 0:
            raise ValueError("Expected nonnegative plain integers")
    return value.copy()

def save_amounts(path, value):
    valid = validate_amounts(value)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(valid, handle)

def load_amounts(path):
    with open(path, "r", encoding="utf-8") as handle:
        return validate_amounts(json.load(handle))

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "amounts.json"
        save_amounts(path, [0, 25])
        print(load_amounts(path))
        try:
            validate_amounts([True])
        except ValueError:
            print("Boolean rejected")
