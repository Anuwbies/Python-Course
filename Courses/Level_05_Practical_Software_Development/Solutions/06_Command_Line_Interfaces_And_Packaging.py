import argparse

def main(argv=None):
    parser = argparse.ArgumentParser(description="Calculate a whole-peso allowance")
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--days", type=int, required=True)
    args = parser.parse_args(argv)
    if args.budget < 0 or args.days <= 0:
        parser.error("budget must be nonnegative and days positive")
    print(args.budget // args.days)
    return 0

if __name__ == "__main__":
    main(["--budget", "500", "--days", "5"])
