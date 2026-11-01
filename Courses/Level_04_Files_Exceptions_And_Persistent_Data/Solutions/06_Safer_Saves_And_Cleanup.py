import json
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

def save_amounts(path, amounts):
    if not isinstance(amounts, list):
        raise ValueError("Expected a list")
    for amount in amounts:
        if type(amount) is not int or amount < 0:
            raise ValueError("Invalid amount")
    text = json.dumps(amounts)
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
        path = Path(folder) / "amounts.json"
        save_amounts(path, [10])
        try:
            save_amounts(path, [-1])
        except ValueError:
            print("Invalid save rejected")
        print(json.loads(path.read_text(encoding="utf-8")))
