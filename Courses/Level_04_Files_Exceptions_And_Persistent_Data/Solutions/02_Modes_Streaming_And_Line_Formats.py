from pathlib import Path
from tempfile import TemporaryDirectory

def append_amount(path, amount):
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(f"{amount}\n")

def load_amounts(path):
    amounts = []
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            text = raw.strip()
            if text:
                amounts.append(int(text))
    return amounts

if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        path = Path(folder) / "amounts.txt"
        append_amount(path, 120)
        append_amount(path, 80)
        values = load_amounts(path)
        print(values)
        print(sum(values))
