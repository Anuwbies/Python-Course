# Lesson 5: Security Architecture: JWT, Password Hashing & OAuth2

In enterprise web applications and distributed microservice clusters, protecting user credentials and securing API endpoints is paramount. Storing raw passwords or using stateful session storage creates severe security vulnerabilities and scalability limits. In this lesson, you will master cryptographic password hashing (via **Bcrypt**), stateless **JSON Web Tokens (JWT)**, the **OAuth2 Password Bearer Flow**, and **Role-Based Access Control (RBAC)**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Hash and verify passwords securely using adaptive cryptographic algorithms (**Bcrypt** / `passlib`).
2. Understand the 3-part anatomy of a **JSON Web Token (JWT)**: Header, Payload, and Signature.
3. Sign, encode, and decode JWTs with expiration timestamps (`exp`) and subject claims (`sub`).
4. Implement the **OAuth2 Password Bearer** specification in FastAPI.
5. Build fine-grained **Role-Based Access Control (RBAC)** security dependencies.
6. Understand token lifecycle architecture (Short-Lived Access Tokens vs. Long-Lived Refresh Tokens).

---

## 1. Cryptographic Password Hashing with Salt

> [!CAUTION]
> **Never store plaintext passwords or use fast hashing algorithms (MD5, SHA-256) for passwords!**
> Fast hashes are vulnerable to brute-force and GPU rainbow table attacks. Always use an adaptive, slow hashing algorithm like **Bcrypt** or **Argon2** which incorporates unique cryptographic salt and adjustable work factors.

```python
import hashlib
import os

def hash_password_secure(password: str, salt: bytes = None) -> tuple[str, str]:
    """Demonstrates PBKDF2-HMAC-SHA256 slow hashing with unique salt."""
    if salt is None:
        salt = os.urandom(16) # 128-bit unique cryptographic salt
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100_000)
    return pwd_hash.hex(), salt.hex()

def verify_password(plain_pwd: str, stored_hash_hex: str, stored_salt_hex: str) -> bool:
    salt = bytes.fromhex(stored_salt_hex)
    computed_hash, _ = hash_password_secure(plain_pwd, salt)
    return computed_hash == stored_hash_hex
```

---

## 2. JSON Web Token (JWT) Architecture

A JWT is a compact, URL-safe string containing three base64-url encoded components separated by dots (`.`):

$$\underbrace{\text{eyJhbGciOi...}}_{\text{Header (Algorithm)}} \cdot \underbrace{\text{eyJzdWIiOi...}}_{\text{Payload (Claims)}} \cdot \underbrace{\text{SflKxwRJS...}}_{\text{Cryptographic Signature}}$$

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "SUPER_SECRET_ENTERPRISE_KEY_CHANGE_IN_PRODUCTION"
ALGORITHM = "HS256"

def create_access_token(user_id: str, role: str, expires_minutes: int = 15) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    # jwt.decode automatically verifies signature AND checks expiration timestamps!
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
```

---

## 3. Role-Based Access Control (RBAC) with FastAPI Dependencies

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_access_token(token)
        return {"user_id": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token signature.")

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(status_code=403, detail="Forbidden: Insufficient privileges.")
        return user
    return role_checker
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Security Authentication & RBAC Authorization Microservice**, demonstrating secure password hashing, JWT token issuance, signature verification, token expiration enforcement, and role guards:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Enterprise JWT Authentication & RBAC Engine
# =====================================================================

import jwt
import hashlib
import os
from datetime import datetime, timedelta, timezone

# 1. Cryptographic Security Helpers (Lesson 5)
SECRET_JWT_KEY = "ApexEnterpriseSecretSigningKey2026"
ALGORITHM = "HS256"

def hash_user_password(password: str) -> tuple[str, str]:
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return hashed.hex(), salt.hex()

def verify_user_password(plain_password: str, expected_hash_hex: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    computed = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, 100_000)
    return computed.hex() == expected_hash_hex


# 2. In-Memory User Directory & JWT Token Service
class EnterpriseAuthService:
    def __init__(self):
        self._user_db: dict[str, dict] = {}

    def register_user(self, email: str, raw_password: str, role: str) -> dict:
        if email in self._user_db:
            raise ValueError(f"User with email '{email}' already registered.")
        
        pwd_hash, salt = hash_user_password(raw_password)
        user_record = {
            "email": email,
            "password_hash": pwd_hash,
            "salt": salt,
            "role": role.upper(),
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self._user_db[email] = user_record
        return user_record

    def authenticate_and_issue_jwt(self, email: str, raw_password: str) -> tuple[str, str]:
        user = self._user_db.get(email)
        if not user or not verify_user_password(raw_password, user["password_hash"], user["salt"]):
            raise PermissionError("Invalid email or password.")

        now = datetime.now(timezone.utc)
        # Short-lived access token (15 mins)
        access_payload = {
            "sub": user["email"],
            "role": user["role"],
            "exp": now + timedelta(minutes=15),
            "iat": now,
            "type": "access"
        }
        # Long-lived refresh token (7 days)
        refresh_payload = {
            "sub": user["email"],
            "exp": now + timedelta(days=7),
            "iat": now,
            "type": "refresh"
        }

        access_token = jwt.encode(access_payload, SECRET_JWT_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, SECRET_JWT_KEY, algorithm=ALGORITHM)
        return access_token, refresh_token

    def verify_and_authorize_request(self, token: str, allowed_roles: set[str]) -> dict:
        try:
            payload = jwt.decode(token, SECRET_JWT_KEY, algorithms=[ALGORITHM])
            user_role = payload.get("role", "GUEST")
            
            if user_role not in allowed_roles:
                raise PermissionError(f"Access Denied: Role '{user_role}' lacks required permissions {allowed_roles}.")

            return payload
        except jwt.ExpiredSignatureError:
            raise PermissionError("Authentication Failed: JWT has expired.")
        except jwt.InvalidTokenError as err:
            raise PermissionError(f"Authentication Failed: Invalid token signature: {err}")


# 3. Execution Simulation
auth_service = EnterpriseAuthService()

# Register Users
auth_service.register_user("elena.rostova@enterprise.com", "SecureMaster2026!", role="ADMIN")
auth_service.register_user("marcus.vance@enterprise.com", "DevOpsPassword123!", role="DEVELOPER")

print("=" * 75)
print(f"{'ENTERPRISE JWT AUTHENTICATION & RBAC SECURITY SUITE':^75}")
print("=" * 75)

# Authenticate Admin
admin_access_token, _ = auth_service.authenticate_and_issue_jwt(
    "elena.rostova@enterprise.com", "SecureMaster2026!"
)
print(f"🔑 Successfully Issued Admin Access Token:")
print(f"   {admin_access_token[:35]}...{admin_access_token[-20:]}")

# Test 1: Admin accesses privileged root infrastructure endpoint
print("\n--- Test 1: Admin queries /admin/infrastructure-purge ---")
admin_claims = auth_service.verify_and_authorize_request(admin_access_token, allowed_roles={"ADMIN"})
print(f"✅ Authorization Granted to Subject: {admin_claims['sub']} (Role: {admin_claims['role']})")

# Authenticate Developer
dev_access_token, _ = auth_service.authenticate_and_issue_jwt(
    "marcus.vance@enterprise.com", "DevOpsPassword123!"
)

# Test 2: Developer attempts to access Admin-only endpoint
print("\n--- Test 2: Developer attempts /admin/infrastructure-purge ---")
try:
    auth_service.verify_and_authorize_request(dev_access_token, allowed_roles={"ADMIN"})
except PermissionError as auth_err:
    print(f"🚨 RBAC Guard Blocked Unauthorized Access: {auth_err}")

# Test 3: Tampered Token
print("\n--- Test 3: Tampered Token Signature Check ---")
tampered_token = admin_access_token[:-5] + "XXXXX"
try:
    auth_service.verify_and_authorize_request(tampered_token, allowed_roles={"ADMIN"})
except PermissionError as tampered_err:
    print(f"🚨 Cryptographic Signature Guard: {tampered_err}")

print("=" * 75)
```

### 🔍 Code Explanation:
- **`PBKDF2-HMAC-SHA256`**: Computes 100,000 iterations with 16 bytes of unique salt per user, securing stored credentials against database leak compromise.
- **`jwt.encode` & `jwt.decode`**: Issues cryptographically signed tokens containing user identities and roles.
- **`ExpiredSignatureError` & RBAC**: The verification gateway checks signature integrity, enforces expiration deadlines, and restricts protected API endpoints to authorized roles.

---

## 📝 Quick Exercise: Multi-Tenant Role Verification & Expired Token Security Guard

### 🏢 Real-Life Scenario
You are developing the authentication firewall middleware for an enterprise cloud platform. Incoming requests arrive with JWT Bearer tokens. You must write the verification function that decodes tokens, verifies they have not expired, checks that the token is of type `"access"`, and verifies that the user's role matches permitted roles.

### 📋 Requirements
1. **Define `issue_test_jwt(email: str, role: str, expires_in_seconds: int = 300, secret: str = "KEY_XYZ") -> str`**:
   - Encodes payload: `{"sub": email, "role": role, "type": "access", "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in_seconds)}`.
2. **Define `verify_jwt_access_guard(token: str, required_roles: set[str], secret: str = "KEY_XYZ") -> tuple[bool, str, dict | None]`**:
   - Uses `jwt.decode()`.
   - Handles `jwt.ExpiredSignatureError`: Returns `False, "Token has expired", None`.
   - Handles `jwt.InvalidTokenError`: Returns `False, "Invalid token signature", None`.
   - If `payload["role"] not in required_roles`: Returns `False, f"Insufficient role privileges: requires {required_roles}", None`.
   - Otherwise: Returns `True, "Access authorized", payload`.
3. Test with valid tokens, expired tokens (`expires_in_seconds=-10`), and unauthorized roles.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 4 JWT security with Level 2 custom error flows and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        ENTERPRISE JWT SECURITY GUARD TEST        
==================================================
  ✓ Valid Admin Token:     ✅ Access authorized (User: admin@corp.io)
  ✗ Expired User Token:    🚨 Token has expired
  ✗ Unauthorized Dev Token:🚨 Insufficient role privileges: requires {'ADMIN'}
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import jwt
from datetime import datetime, timedelta, timezone

SECRET = "KEY_XYZ_SECURITY_2026"

# 1. Token Issuer (Level 4)
def issue_test_jwt(email: str, role: str, expires_in_seconds: int = 300) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": email,
        "role": role,
        "type": "access",
        "exp": now + timedelta(seconds=expires_in_seconds),
        "iat": now
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


# 2. JWT Verification Guard (Level 4)
def verify_jwt_access_guard(token: str, required_roles: set[str]) -> tuple[bool, str, dict | None]:
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        if payload.get("role") not in required_roles:
            return False, f"Insufficient role privileges: requires {required_roles}", None
        return True, "Access authorized", payload
    except jwt.ExpiredSignatureError:
        return False, "Token has expired", None
    except jwt.InvalidTokenError as err:
        return False, f"Invalid token: {err}", None


# 3. Execution Simulation
admin_token = issue_test_jwt("admin@corp.io", "ADMIN", expires_in_seconds=300)
expired_token = issue_test_jwt("user@corp.io", "ADMIN", expires_in_seconds=-10) # Expired
dev_token = issue_test_jwt("dev@corp.io", "DEVELOPER", expires_in_seconds=300)

print("==================================================")
print("        ENTERPRISE JWT SECURITY GUARD TEST        ")
print("==================================================")

# Test 1: Valid
ok1, msg1, p1 = verify_jwt_access_guard(admin_token, {"ADMIN"})
print(f"  ✓ Valid Admin Token:     {'✅' if ok1 else '🚨'} {msg1} (User: {p1['sub']})")

# Test 2: Expired
ok2, msg2, _ = verify_jwt_access_guard(expired_token, {"ADMIN"})
print(f"  ✗ Expired User Token:    {'✅' if ok2 else '🚨'} {msg2}")

# Test 3: Unauthorized Role
ok3, msg3, _ = verify_jwt_access_guard(dev_token, {"ADMIN"})
print(f"  ✗ Unauthorized Dev Token:{'✅' if ok3 else '🚨'} {msg3}")

print("==================================================")
```

**Explanation of the Solution:**
- `verify_jwt_access_guard` leverages PyJWT to validate both cryptographic signature integrity and timestamp expiration bounds in a single step.
- Role checks prevent non-administrative users from calling protected operations.
</details>
