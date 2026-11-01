# Lesson 2: Authentication, Tokens & Authorization

**Prerequisites:** Levels 1–10 and Lesson 1 of this level. **Practice file:** `Practice/02_Authentication_Tokens_And_Authorization.py`.

Identify the caller and then decide whether that identity may perform the operation. A signed token is one input to that decision; decoding readable JSON is not authentication.

## 1. Distinguish the boundaries

Authentication establishes an identity under a trusted mechanism. Authorization applies rules to that identity and the requested resource. A valid reader token can still be forbidden from an administrative write. Missing or invalid credentials commonly lead to 401 with a Bearer challenge; an authenticated caller lacking permission receives 403 under this course's policy.

JWT is a token format, not the OAuth protocol. OAuth/OIDC deployments involve an authorization server, clients, scopes, redirects, and trusted issuer/key configuration. Declaring a bearer scheme in an API's documentation does not implement that full flow.

## 2. Verify a constrained token contract

PyJWT can verify a signature with an explicit algorithm allowlist, audience, issuer, required claims, and expiration. Do not choose the accepted algorithm from an untrusted token header or disable signature verification simply to inspect the payload.

The course's small issuer contract includes sub, role, iat, exp, aud, and iss. Validate custom claim types and allowed role values after decoding. A signature establishes integrity under the trusted key; it does not make arbitrary role spelling or blank subject values meaningful.

## 3. Keep passwords and payloads separate

For a password-based identity store, use a password-hashing library such as pwdlib with a suitable configured algorithm rather than a fast general hash. Verification uses the library API; never compare a stored plaintext password or place passwords inside token claims.

A signed JWT payload is ordinarily readable by its holder. Signing is not encryption. Keep secrets and unnecessary personal data out of claims and logs. Short expiration bounds one risk but does not alone provide revocation or protect a stolen token before expiry.

## 4. Exercise failure and access rules

The task issues an ephemeral local token only to demonstrate signature and claim verification. The capstone's operator-side issuer is separate from the API; there is no unauthenticated endpoint minting admin credentials.

In a real identity integration, configure trusted providers and key rotation according to that deployment's protocol. Apply resource-level ownership rules when data is private; a role check alone is insufficient for a personal-record system. The capstone deliberately uses a shared catalog with coarse reader/admin operations.

## Use the password and token APIs directly

The hash verifier receives the candidate password first and its stored hash second. JWT timestamps use aware UTC datetimes; adding a timedelta defines a duration rather than modifying the wall clock.

```python
from datetime import datetime, timedelta, timezone
import secrets
import jwt
from pwdlib import PasswordHash

passwords = PasswordHash.recommended()
hashed = passwords.hash("classroom example phrase")
print(passwords.verify("classroom example phrase", hashed))  # True
key = secrets.token_urlsafe(32)
now = datetime.now(timezone.utc)
token = jwt.encode({"sub": "example-user", "role": "reader", "iat": now,
                    "exp": now + timedelta(minutes=5), "aud": "course-api",
                    "iss": "course-issuer"}, key, algorithm="HS256")
claims = jwt.decode(token, key, algorithms=["HS256"], audience="course-api",
                    issuer="course-issuer",
                    options={"require": ["sub", "role", "iat", "exp", "aud", "iss"]})
if not isinstance(claims["sub"], str) or not claims["sub"].strip():
    raise jwt.InvalidTokenError("Invalid subject")
if not isinstance(claims["role"], str) or claims["role"] not in {"reader", "admin"}:
    raise jwt.InvalidTokenError("Invalid role")
print(claims["role"])
```

The required list enforces presence; decoder validation and the application's custom type/value checks enforce meaning. InvalidTokenError is the common PyJWT error family to translate at the HTTP boundary. Do not catch an unrelated programming failure as bad credentials. A wrong key, expired token, wrong issuer/audience, missing claim, or disallowed role must not authorize a request.

## Adapt verified identity to FastAPI dependencies

Import HTTPBearer and HTTPAuthorizationCredentials from fastapi.security. `bearer = HTTPBearer(auto_error=False)` parses the header and returns credentials or None. A dependency can receive `credentials: HTTPAuthorizationCredentials | None = Depends(bearer)`, then pass credentials.credentials to the decoder above. Missing/invalid credentials raise `HTTPException(401, "Invalid token", headers={"WWW-Authenticate": "Bearer"})`. A second dependency receives `claims=Depends(principal)`, rejects a non-admin role with 403, and otherwise returns the verified claims. A protected route requests the appropriate dependency; it never trusts a raw role header.

Clients send `headers={"Authorization": "Bearer " + token}` with TestClient requests. For a custom header, `Header(alias="Idempotency-Key", min_length=1, max_length=80)` from fastapi declares its external spelling and length contract. Strip and reject whitespace-only values separately. The operator CLI can use argparse choices for reader/admin and the same signing contract; the API only verifies, rather than exposing unrestricted token issuance.

References: [FastAPI security](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [PyJWT claim verification](https://pyjwt.readthedocs.io/en/stable/usage.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the difference between an invalid token and a valid reader attempting an admin operation.
2. **Explain:** Explain why signed payloads should not contain passwords.
3. **Modify:** Require issuer and audience instead of verifying only the signature.
4. **Debug:** Find a decoder selecting an algorithm from untrusted token data.

<details>
<summary>Hints</summary>

Use the verified claims for authorization and keep the key and token out of the transcript.

</details>

## Independent task: authentication, tokens & authorization

In `Practice/02_Authentication_Tokens_And_Authorization.py`, complete this task:

Use pwdlib.PasswordHash.recommended to hash and verify an example password, printing True for the correct value and False for a wrong one. Generate an ephemeral key with secrets.token_urlsafe(32). Issue a five-minute HS256 JWT for sub=mika and role=reader with iat/exp/aud=course-api/iss=course-issuer. Decode with an explicit algorithm allowlist, required claims, audience and issuer, validate the custom subject/role, and print the verified role. Do not print the password hash, key, or token.

Expected output:

```text
True
False
reader
```
