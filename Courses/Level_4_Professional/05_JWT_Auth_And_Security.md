# Lesson 5: Authentication & Security: JWT, OAuth2 & Password Hashing

Security is non-negotiable in production backend systems. In this lesson, you will master cryptographic password hashing, stateless JSON Web Tokens (JWT), and OAuth2 password flows.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Securely hash passwords with salted **Argon2** / **Bcrypt**.
2. Generate, sign, and verify cryptographic **JSON Web Tokens (JWT)**.
3. Protect FastAPI endpoints using OAuth2 Bearer token dependencies.
4. Implement Role-Based Access Control (RBAC).

---

## 1. Password Hashing (Argon2 / Passlib)

Never store plaintext passwords or reversible encrypted strings in a database. Use salted cryptographic hashing:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Example:
hashed = hash_password("MySecureP@ss123")
print(verify_password("MySecureP@ss123", hashed)) # True
print(verify_password("WrongPassword", hashed))    # False
```

---

## 2. JWT Generation & Token Verification

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "SUPER_SECRET_PRODUCTION_KEY_DO_NOT_LEAK"
ALGORITHM = "HS256"

def create_access_token(user_id: int, role: str, expires_delta: timedelta = timedelta(minutes=30)) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": str(user_id),
        "role": role,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid authentication token")
```

---

## 📝 Quick Exercise

**Prompt**:
Create a FastAPI dependency `require_admin_role` that extracts the JWT token from the `Authorization: Bearer <token>` header, decodes it, and raises HTTP 403 Forbidden if `payload["role"] != "admin"`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from fastapi import Header, HTTPException, status, Depends
import jwt

def require_admin_role(authorization: str = Header(...)) -> dict:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token scheme")
    
    token = authorization.split(" ")[1]
    try:
        payload = decode_access_token(token)
        if payload.get("role") != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
```
</details>
