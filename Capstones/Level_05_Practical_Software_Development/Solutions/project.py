import argparse
import json
from pathlib import Path

def load_amounts(path: Path) -> list[int]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError("Expected a list")
    for amount in value:
        if type(amount) is not int or amount < 0:
            raise ValueError("Amounts must be nonnegative integers")
    return value

def summarize(amounts: list[int], budget: int) -> dict[str, int]:
    total = sum(amounts)
    return {"count": len(amounts), "total": total, "remaining": budget - total}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Report a JSON expense list")
    parser.add_argument("path", type=Path)
    parser.add_argument("--budget", type=int, required=True)
    args = parser.parse_args(argv)
    if args.budget < 0:
        parser.error("budget must be nonnegative")
    try:
        summary = summarize(load_amounts(args.path), args.budget)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(f"Entries: {summary['count']}")
    print(f"Spent: PHP {summary['total']}")
    print(f"Remaining: PHP {summary['remaining']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
