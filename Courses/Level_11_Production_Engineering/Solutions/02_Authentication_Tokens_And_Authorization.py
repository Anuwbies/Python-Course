from datetime import datetime, timedelta, timezone
import secrets
import jwt
from pwdlib import PasswordHash

passwords = PasswordHash.recommended()
hashed = passwords.hash("example learning phrase")
print(passwords.verify("example learning phrase", hashed))
print(passwords.verify("wrong", hashed))
key = secrets.token_urlsafe(32)
now = datetime.now(timezone.utc)
token = jwt.encode({"sub":"mika", "role":"reader", "iat":now,
                    "exp":now + timedelta(minutes=5), "aud":"course-api", "iss":"course-issuer"}, key, algorithm="HS256")
claims = jwt.decode(token, key, algorithms=["HS256"], audience="course-api", issuer="course-issuer",
                    options={"require":["sub","role","iat","exp","aud","iss"]})
if not isinstance(claims["sub"], str) or not claims["sub"].strip():
    raise jwt.InvalidTokenError("Invalid subject")
if not isinstance(claims["role"], str) or claims["role"] not in {"reader","admin"}:
    raise jwt.InvalidTokenError("Invalid role")
print(claims["role"])
