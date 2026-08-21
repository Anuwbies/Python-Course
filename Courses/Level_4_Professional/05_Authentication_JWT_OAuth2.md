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

---

## 4. Symmetric (HS256) vs Asymmetric (RS256) Signing

| Feature | HS256 (HMAC-SHA256) | RS256 (RSA Signature) |
| :--- | :--- | :--- |
| **Key Architecture** | Single Shared Secret Key | Private Key (sign) + Public Key (verify) |
| **Best Used For** | Monolithic backends, single-service APIs | Distributed microservices, auth providers (Auth0, Okta, Keycloak) |
| **Security Advantage** | Fast and simple | Microservices can verify tokens using the public key without knowing the signing private key! |

---

## 5. Refresh Token Rotation & Token Revocation (JTI Blocklist)

Stateless JWTs cannot be easily revoked before their expiration time. Enterprise architectures solve this using **Refresh Token Rotation**:
1. **Access Token**: Short-lived (15 minutes). Sent in `Authorization: Bearer <token>`.
2. **Refresh Token**: Long-lived (7 days). Stored in `HttpOnly, Secure` cookies.
3. **Rotation**: When the refresh token is exchanged for a new access token, the old refresh token is invalidated immediately.
4. **JTI (JWT ID) Blocklist**: Stolen tokens are blacklisted in Redis keyed by `jti` claim with an automated TTL equal to token expiration.

---

## 6. OAuth2 Authorization Code Flow with PKCE

For Single Page Applications (React, Vue) and mobile clients, **PKCE (Proof Key for Code Exchange)** prevents authorization code interception attacks without requiring a client secret:
1. Client generates random `code_verifier` and computes `code_challenge = SHA256(code_verifier)`.
2. User authenticates via browser; auth server issues authorization code.
3. Client exchanges code + original `code_verifier` for access token.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master password hashing, JWT signing, OAuth2 flows, refresh rotation, and RBAC guards:

---

### 🟢 Tier 1: Password Hashing & Salt Basics (Exercises 1–3)

#### 🔹 Exercise 1: Salted PBKDF2 Password Hasher
* **Goal**: Write a secure password hasher generating random 16-byte salts and 100,000 SHA256 iterations.

#### 🔹 Exercise 2: Password Verification Function
* **Goal**: Validate candidate passwords against stored hex hashes in constant time to prevent timing attacks.

#### 🔹 Exercise 3: Simple JWT Issuance & Decoding
* **Goal**: Encode a JWT with `sub`, `iat`, and `exp` claims and decode it with `jwt.decode()`.

---

### 🟡 Tier 2: Expiration, Roles & OAuth2 Dependencies (Exercises 4–6)

#### 🔹 Exercise 4: Token Expiration Error Handling
* **Goal**: Catch `jwt.ExpiredSignatureError` and return structured HTTP 401 response payload.

#### 🔹 Exercise 5: Role-Based Access Dependency (`require_roles`)
* **Goal**: Build a FastAPI dependency factory restricting routes to users with `"ADMIN"` or `"MANAGER"` roles.

#### 🔹 Exercise 6: OAuth2 Password Bearer Header Extractor
* **Goal**: Use `OAuth2PasswordBearer(tokenUrl="...")` to extract bearer tokens from request headers.

---

### 🟠 Tier 3: Refresh Tokens & Asymmetric Verification (Exercises 7–9)

#### 🔹 Exercise 7: Dual Token Pair Generation (Access + Refresh)
* **Goal**: Issue short-lived access token (15m) and long-lived refresh token (7d) with distinct `type` claims.

#### 🔹 Exercise 8: Refresh Token Rotation Engine
* **Goal**: Implement token exchange consuming a refresh token and issuing a brand new token pair.

#### 🔹 Exercise 9: Redis JTI Blacklist Simulation
* **Goal**: Implement `revoke_token(jti)` storing invalidated token IDs in a set to block future requests.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Enterprise JWT Security Guard & RBAC Gateway
* **Goal**: Build a production-grade authentication verification firewall validating signatures, expiration dates, and role permissions.

---

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
<summary><b>🔍 View Exercise Solutions (JWT Guard & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Enterprise JWT Security Guard & RBAC Gateway
# =====================================================================
import jwt
from datetime import datetime, timedelta, timezone

SECRET = "KEY_XYZ_SECURITY_2026"

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


admin_token = issue_test_jwt("admin@corp.io", "ADMIN", expires_in_seconds=300)
expired_token = issue_test_jwt("user@corp.io", "ADMIN", expires_in_seconds=-10)
dev_token = issue_test_jwt("dev@corp.io", "DEVELOPER", expires_in_seconds=300)

print("==================================================")
print("        ENTERPRISE JWT SECURITY GUARD TEST        ")
print("==================================================")

ok1, msg1, p1 = verify_jwt_access_guard(admin_token, {"ADMIN"})
print(f"  ✓ Valid Admin Token:     {'✅' if ok1 else '🚨'} {msg1} (User: {p1['sub']})")

ok2, msg2, _ = verify_jwt_access_guard(expired_token, {"ADMIN"})
print(f"  ✗ Expired User Token:    {'✅' if ok2 else '🚨'} {msg2}")

ok3, msg3, _ = verify_jwt_access_guard(dev_token, {"ADMIN"})
print(f"  ✗ Unauthorized Dev Token:{'✅' if ok3 else '🚨'} {msg3}")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Salted PBKDF2 Hasher
import hashlib, os
def hash_pwd(pwd: str):
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt, 100_000)
    return h.hex(), salt.hex()

# Ex 2: Password Verifier
import hmac
def verify_pwd(pwd, stored_h, stored_salt):
    salt = bytes.fromhex(stored_salt)
    h = hashlib.pbkdf2_hmac("sha256", pwd.encode(), salt, 100_000).hex()
    return hmac.compare_digest(h, stored_h)

# Ex 3: Encode/Decode JWT
# payload = {"sub": "123", "exp": datetime.now(timezone.utc) + timedelta(minutes=15)}
# token = jwt.encode(payload, "secret", algorithm="HS256")

# Ex 4: Handle Expiration
# try: jwt.decode(t, "secret", algorithms=["HS256"]) except jwt.ExpiredSignatureError: ...

# Ex 5: Role Requirement Dependency
# def require_roles(*roles): def dep(u = Depends(get_current_user)): if u["role"] not in roles: raise HTTPException(403)

# Ex 6: OAuth2PasswordBearer
# oauth2 = OAuth2PasswordBearer(tokenUrl="token")

# Ex 7: Dual Token Pair
# access_token = jwt.encode({"sub": u, "type": "access", "exp": ...}, s)
# refresh_token = jwt.encode({"sub": u, "type": "refresh", "exp": ...}, s)

# Ex 8: Token Rotation
# def rotate_tokens(old_refresh): revoke(old_refresh); return create_pair()

# Ex 9: JTI Blacklist
# REVOKED_JTIS = set()
# def is_revoked(jti): return jti in REVOKED_JTIS
```
</details>
