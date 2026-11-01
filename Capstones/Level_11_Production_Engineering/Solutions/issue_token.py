import argparse
from datetime import datetime, timedelta, timezone
import os
import jwt

def main():
    parser = argparse.ArgumentParser(description="Operator-only course token issuer")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--role", choices=["reader","admin"], required=True)
    args = parser.parse_args()
    key = os.environ["TOKEN_SECRET"]
    if len(key) < 32 or not args.subject.strip():
        parser.error("Valid subject and configured key required")
    now = datetime.now(timezone.utc)
    print(jwt.encode({"sub":args.subject.strip(),"role":args.role,"iat":now,
        "exp":now+timedelta(minutes=5),"aud":"course-api","iss":"course-issuer"}, key, algorithm="HS256"))

if __name__ == "__main__":
    main()
