# Lesson 4: Custom Exceptions & Advanced Error Architecture

Standard built-in exceptions like `ValueError` or `KeyError` are often too generic to communicate specific business logic failures in large applications. When a bank transfer fails because an account is frozen, raising a generic `ValueError` hides the true domain context. In this lesson, you will master architecting domain-specific custom exception hierarchies, embedding diagnostic metadata, and chaining exceptions with `raise ... from`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Design structured, hierarchical custom exceptions by inheriting from Python's standard `Exception` class.
2. Embed domain-specific diagnostic metadata (error codes, timestamps, failing payload IDs) into exception classes.
3. Preserve root cause debugging tracebacks using **Explicit Exception Chaining** (`raise ... from`).
4. Catch and handle exceptions hierarchically using polymorphic `except` handlers.
5. Follow industry best practices for exception boundaries in enterprise services.

---

## 1. Designing Custom Exception Hierarchies

Always create a single base domain exception for your package or module. All specific domain errors inherit from this base class:

```
        Exception (Built-in)
                 │
        ┌────────┴────────┐
   PaymentGatewayError (Domain Base)
        │
   ┌────┴──────────────────────────┬────────────────────────┐
CardExpiredError             InsufficientFundsError     FraudVelocityLimitError
```

```python
class PaymentGatewayError(Exception):
    """Base exception for all payment-processing failures."""
    def __init__(self, message: str, error_code: str, http_status: int = 400):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.http_status = http_status

class InsufficientFundsError(PaymentGatewayError):
    """Raised when an account balance is lower than requested withdrawal."""
    def __init__(self, account_id: str, requested: float, available: float):
        msg = f"Account '{account_id}' has ${available:,.2f} available; cannot debit ${requested:,.2f}."
        super().__init__(msg, error_code="PAY_INSUFFICIENT_FUNDS", http_status=402)
        self.account_id = account_id
        self.requested = requested
        self.available = available

class CardExpiredError(PaymentGatewayError):
    """Raised when payment instrument has passed expiration date."""
    def __init__(self, card_last_four: str, expiry_date: str):
        msg = f"Card ending in {card_last_four} expired on {expiry_date}."
        super().__init__(msg, error_code="PAY_CARD_EXPIRED", http_status=400)
```

---

## 2. Polymorphic Exception Catching

Because child exceptions inherit from `PaymentGatewayError`, caller code can catch either fine-grained errors or the entire family with a single handler:

```python
try:
    # Attempt processing transaction
    raise InsufficientFundsError("ACC-901", requested=500.0, available=120.0)
except InsufficientFundsError as err:
    # Fine-grained: Prompt user to add funds
    print(f"💰 Account Alert: {err.message} [Code: {err.error_code}]")
except PaymentGatewayError as base_err:
    # Broad fallback: Catches any other payment error
    print(f"❌ Payment Failure: {base_err.message}")
```

---

## 3. Explicit Exception Chaining (`raise ... from`)

When an unexpected low-level error (like a socket timeout or database disconnection) causes a domain failure, you should translate it into a domain exception while preserving the original cause:

```python
import json

class ConfigFileCorruptedError(Exception):
    """Raised when JSON configuration parsing fails."""
    pass

def load_system_settings(filepath: str) -> dict:
    try:
        with open(filepath, "r") as f:
            return json.loads(f.read())
    except (json.JSONDecodeError, FileNotFoundError) as original_err:
        # 'from original_err' links the low-level cause directly to the new exception in tracebacks
        raise ConfigFileCorruptedError(f"Failed to load critical system config: {filepath}") from original_err
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Fintech Account Settlement & Transaction Safety Pipeline**, combining hierarchical custom exceptions, contextual error codes, and exception chaining:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Core Banking Transaction Settlement & Error Core
# =====================================================================

from datetime import datetime

# 1. Domain Exception Hierarchy (Lesson 4)
class CoreBankingException(Exception):
    """Base exception for all core banking platform anomalies."""
    def __init__(self, message: str, error_code: str, audit_ref: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.audit_ref = audit_ref or f"REF-{int(datetime.now().timestamp())}"

    def to_audit_payload(self) -> dict:
        return {
            "exception_class": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "audit_reference": self.audit_ref,
        }


class AccountNotFoundException(CoreBankingException):
    def __init__(self, account_id: str):
        super().__init__(f"Account identifier '{account_id}' does not exist in master ledger.", "BANK_E404_ACC_MISSING")
        self.account_id = account_id


class AccountFrozenException(CoreBankingException):
    def __init__(self, account_id: str, reason: str):
        super().__init__(f"Account '{account_id}' is FROZEN. Action blocked: {reason}", "BANK_E403_ACC_FROZEN")
        self.account_id = account_id
        self.reason = reason


class InsufficientLiquidityException(CoreBankingException):
    def __init__(self, account_id: str, requested: float, available: float):
        super().__init__(
            f"Insufficient funds in account '{account_id}'. Requested: ${requested:,.2f}, Available: ${available:,.2f}",
            "BANK_E402_OVERDRAFT"
        )
        self.account_id = account_id
        self.requested = requested
        self.available = available


# 2. Banking Ledger Service
class CoreBankingLedger:
    def __init__(self):
        self._accounts = {
            "ACC-101": {"owner": "Elena Rostova", "balance": 5000.00, "status": "ACTIVE"},
            "ACC-102": {"owner": "Marcus Vance", "balance": 150.00, "status": "ACTIVE"},
            "ACC-103": {"owner": "Sarah Connor", "balance": 80000.00, "status": "FROZEN_FRAUD_LOCK"},
        }

    def execute_wire_transfer(self, source_id: str, dest_id: str, amount: float) -> dict:
        """Transfers funds between accounts with multi-layered invariant checks."""
        if amount <= 0:
            raise ValueError(f"Transfer amount must be strictly positive: ${amount}")

        # Check account existence
        if source_id not in self._accounts:
            raise AccountNotFoundException(source_id)
        if dest_id not in self._accounts:
            raise AccountNotFoundException(dest_id)

        source = self._accounts[source_id]
        dest = self._accounts[dest_id]

        # Check account status
        if source["status"] != "ACTIVE":
            raise AccountFrozenException(source_id, f"Security hold status: '{source['status']}'")

        # Check liquidity
        if source["balance"] < amount:
            raise InsufficientLiquidityException(source_id, requested=amount, available=source["balance"])

        # Execute atomic transfer
        source["balance"] -= amount
        dest["balance"] += amount

        return {
            "status": "SETTLED",
            "source_id": source_id,
            "dest_id": dest_id,
            "transferred_amount": amount,
            "source_remaining_balance": source["balance"],
        }


# 3. Execution Simulation & Exception Handling Boundary
ledger = CoreBankingLedger()

test_transactions = [
    ("ACC-101", "ACC-102", 500.00),     # Valid
    ("ACC-102", "ACC-101", 1000.00),    # Insufficient liquidity
    ("ACC-103", "ACC-101", 200.00),     # Frozen account
    ("ACC-999", "ACC-101", 100.00),     # Account not found
]

print("=" * 75)
print(f"{'CORE BANKING WIRE TRANSACTION SETTLEMENT PIPELINE':^75}")
print("=" * 75)

for src, dst, amt in test_transactions:
    try:
        result = ledger.execute_wire_transfer(src, dst, amt)
        print(f"✅ [SETTLED] Wire ${amt:>8.2f} from {src} -> {dst} (New Bal: ${result['source_remaining_balance']:,.2f})")
    except InsufficientLiquidityException as ex:
        print(f"⚠️ [OVERDRAFT] Code: {ex.error_code} | {ex.message}")
    except AccountFrozenException as ex:
        print(f"🚨 [COMPLIANCE] Code: {ex.error_code} | {ex.message}")
    except CoreBankingException as ex:
        print(f"❌ [BANK ERROR] Code: {ex.error_code} | {ex.message}")
    except ValueError as ex:
        print(f"❌ [VALIDATION] {ex}")

print("=" * 75)
```

### 🔍 Code Explanation:
- **Base Domain Exception**: `CoreBankingException` standardizes `error_code`, `audit_ref`, and serialization to structured JSON-friendly audit payloads.
- **Specialized Subclasses**: `InsufficientLiquidityException`, `AccountFrozenException`, and `AccountNotFoundException` carry typed domain fields (`account_id`, `available`, `reason`).
- **Granular Exception Handling**: The transaction engine catches individual error types to execute distinct business responses (compliance alert vs overdraft warning vs general bank failure).

---

## 📝 Quick Exercise: API Gateway Authentication, Token Expiry & Rate Limiting System

### 🏢 Real-Life Scenario
You are developing an API Gateway security firewall for a microservices cluster. Incoming HTTP requests pass an API authentication token and client IP address. You must design an exception hierarchy to handle authentication tokens that are missing, expired, revoked, or exceeding rate limits, returning structured HTTP status responses.

### 📋 Requirements
1. **Define Base Exception `GatewaySecurityException(Exception)`**:
   - Constructor: `__init__(self, message: str, status_code: int = 400, error_key: str = "SECURITY_FAULT")`
2. **Define Specialized Subclasses**:
   - `TokenMissingException(GatewaySecurityException)`: `status_code = 401`, `error_key = "AUTH_TOKEN_MISSING"`.
   - `TokenExpiredException(GatewaySecurityException)`: Constructor accepts `token_id: str`, `expired_at: str`. `status_code = 401`, `error_key = "AUTH_TOKEN_EXPIRED"`.
   - `RateLimitExceededException(GatewaySecurityException)`: Constructor accepts `client_ip: str`, `requests_count: int`, `max_allowed: int`. `status_code = 429`, `error_key = "RATE_LIMIT_EXCEEDED"`.
3. **Define `authenticate_api_request(headers: dict, request_counts: dict)`**:
   - If `"Authorization"` not in `headers`: Raise `TokenMissingException`.
   - If token is `"TOKEN-EXPIRED"`: Raise `TokenExpiredException`.
   - If client IP has made $> 5$ requests: Raise `RateLimitExceededException`.
   - Otherwise: Return `{"status": "AUTHORIZED", "client": headers["Authorization"]}`.
4. Process test requests and format the security gateway firewall logs.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 custom exceptions and inheritance with Level 1 dictionaries, functions, and string formatting.

### 🎯 Expected Output
```text
==================================================
        API GATEWAY SECURITY FIREWALL LOGS        
==================================================
[200 OK]  Authorized: Bearer token_live_101 from 192.168.1.1
[401 ERR] Status 401 (AUTH_TOKEN_MISSING): Request is missing required Authorization header.
[401 ERR] Status 401 (AUTH_TOKEN_EXPIRED): Security token 'TOKEN-EXPIRED' expired at 2026-08-19 12:00:00.
[429 ERR] Status 429 (RATE_LIMIT_EXCEEDED): IP 10.0.0.99 exceeded limit: 12/5 requests.
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Custom Exception Hierarchy (Level 2)
class GatewaySecurityException(Exception):
    def __init__(self, message: str, status_code: int = 400, error_key: str = "SECURITY_FAULT"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_key = error_key


class TokenMissingException(GatewaySecurityException):
    def __init__(self):
        super().__init__(
            "Request is missing required Authorization header.",
            status_code=401,
            error_key="AUTH_TOKEN_MISSING"
        )


class TokenExpiredException(GatewaySecurityException):
    def __init__(self, token_id: str, expired_at: str):
        super().__init__(
            f"Security token '{token_id}' expired at {expired_at}.",
            status_code=401,
            error_key="AUTH_TOKEN_EXPIRED"
        )
        self.token_id = token_id
        self.expired_at = expired_at


class RateLimitExceededException(GatewaySecurityException):
    def __init__(self, client_ip: str, requests_count: int, max_allowed: int = 5):
        super().__init__(
            f"IP {client_ip} exceeded limit: {requests_count}/{max_allowed} requests.",
            status_code=429,
            error_key="RATE_LIMIT_EXCEEDED"
        )
        self.client_ip = client_ip
        self.requests_count = requests_count


# 2. Gateway Security Guard
def authenticate_api_request(headers: dict, client_ip: str, request_counts: dict) -> dict:
    if "Authorization" not in headers:
        raise TokenMissingException()

    auth_token = headers["Authorization"]
    if auth_token == "TOKEN-EXPIRED":
        raise TokenExpiredException(auth_token, "2026-08-19 12:00:00")

    count = request_counts.get(client_ip, 0) + 1
    request_counts[client_ip] = count

    if count > 5:
        raise RateLimitExceededException(client_ip, requests_count=count, max_allowed=5)

    return {"status": "AUTHORIZED", "client": auth_token, "ip": client_ip}


# 3. Test Firewall Requests
test_requests = [
    ({"Authorization": "Bearer token_live_101"}, "192.168.1.1"),
    ({}, "192.168.1.2"),
    ({"Authorization": "TOKEN-EXPIRED"}, "192.168.1.3"),
    ({"Authorization": "Bearer token_rate_test"}, "10.0.0.99"),
]

ip_history = {"10.0.0.99": 11} # Pre-existing requests exceeding rate threshold

print("==================================================")
print("        API GATEWAY SECURITY FIREWALL LOGS        ")
print("==================================================")

for headers, ip in test_requests:
    try:
        res = authenticate_api_request(headers, ip, ip_history)
        print(f"[200 OK]  Authorized: {res['client']} from {res['ip']}")
    except GatewaySecurityException as ex:
        print(f"[{ex.status_code} ERR] Status {ex.status_code} ({ex.error_key}): {ex.message}")

print("==================================================")
```

**Explanation of the Solution:**
- `GatewaySecurityException` establishes common HTTP status metadata across all security issues.
- Individual error subclasses specialize error codes and status responses (`401 Unauthorized`, `429 Too Many Requests`).
- Polymorphic `except GatewaySecurityException as ex:` cleanly captures all security failures.
</details>
