# 🟡 Level 2: Intermediate Python — 20 Comprehensive Capstone Projects

Welcome to the **Level 2 Intermediate Capstone Collection**! This document contains 20 production-grade capstone projects designed to test and master Software Craftsmanship in Python: Advanced Object-Oriented Programming (Inheritance, Polymorphism, Mixins), `@property` encapsulation, Magic Dunder methods, Abstract Base Classes (ABCs), Custom Exceptions, Iterators & Streaming Generators, Decorators & Closures, Context Managers, and Type Hinting with `pytest`.

Every solution includes **detailed, step-by-step explanatory comments directly inside the code** to guide your learning.

---

## 📑 Table of Contents
1. [Multi-Tier Payment Gateway Adapter Pipeline](#1-multi-tier-payment-gateway-adapter-pipeline)
2. [Financial Investment Portfolio & Asset Vector Engine](#2-financial-investment-portfolio--asset-vector-engine)
3. [Microservice Health Monitor with ABC Plugins](#3-microservice-health-monitor-with-abc-plugins)
4. [Core Banking Wire Transfer with Custom Exception Hierarchy](#4-core-banking-wire-transfer-with-custom-exception-hierarchy)
5. [Real-Time Cloud Server Telemetry & Anomaly Streamer](#5-real-time-cloud-server-telemetry--anomaly-streamer)
6. [API Endpoint Security, Rate-Limiting & Memoization Decorator Suite](#6-api-endpoint-security-rate-limiting--memoization-decorator-suite)
7. [ACID Database Transaction & File Sandbox Context Manager](#7-acid-database-transaction--file-sandbox-context-manager)
8. [E-Commerce Order Pricing Engine with Comprehensive Pytest Suite](#8-e-commerce-order-pricing-engine-with-comprehensive-pytest-suite)
9. [Multi-Cloud Resource Orchestrator with Mixins](#9-multi-cloud-resource-orchestrator-with-mixins)
10. [Cross-Border Fintech Multi-Currency Digital Wallet](#10-cross-border-fintech-multi-currency-digital-wallet)
11. [Resilient Database Query Retry & Performance Profiler](#11-resilient-database-query-retry--performance-profiler)
12. [Sensor Time-Series Moving Average Generator Pipeline](#12-sensor-time-series-moving-average-generator-pipeline)
13. [Pluggable Encryption & Compression Stream Filter Engine](#13-pluggable-encryption--compression-stream-filter-engine)
14. [Role-Based Access Control (RBAC) Permission Decorator Framework](#14-role-based-access-control-rbac-permission-decorator-framework)
15. [Secure Temporary API Token Leasing Context Manager](#15-secure-temporary-api-token-leasing-context-manager)
16. [Asynchronous Event Dispatcher with ABC Subscriber Interfaces](#16-asynchronous-event-dispatcher-with-abc-subscriber-interfaces)
17. [Custom Vector Math Library with Dunder Operator Overloading](#17-custom-vector-math-library-with-dunder-operator-overloading)
18. [Config File Parser with Cascading Environment Overrides](#18-config-file-parser-with-cascading-environment-overrides)
19. [High-Throughput Log Sanitizer & Regex Masking Stream](#19-high-throughput-log-sanitizer--regex-masking-stream)
20. [Service-Level Objective (SLO) Latency Auditor with Pytest Fixtures](#20-service-level-objective-slo-latency-auditor-with-pytest-fixtures)

---

## 1. Multi-Tier Payment Gateway Adapter Pipeline

### 🏢 Real-Life Scenario
An e-commerce platform processes transactions across different payment providers (Credit Card, Cryptocurrency, PayPal). The system requires a polymorphic architecture with audit logging mixins and fraud detection.

### 📋 Requirements
1. Base class `PaymentGateway` with `.process_payment(txn_id, amount)`.
2. Mixins `AuditLogMixin` and `FraudScreeningMixin`.
3. Specialized subclasses: `CreditCardGateway` (2.9% fee) and `CryptoGateway` ($4.50 gas fee).

### 🎯 Expected Output
```text
==================================================
        MERCHANT PAYMENT SETTLEMENT RUN           
==================================================
[AUDIT] CreditCardGateway: (TXN-101): Settled $150.00 (Net Payout: $145.35)
[AUDIT] CryptoGateway: (TXN-102): Mined on Ethereum $500.00 (Net Payout: $490.50)
[AUDIT] CreditCardGateway: (TXN-103): FRAUD HELD $12,000.00 (Exceeds Limit)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 1: Multi-Tier Payment Gateway Adapter Pipeline
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. MIXIN PATTERN: AuditLogMixin and FraudScreeningMixin inject cross-cutting
#    capabilities into concrete gateways without polluting the base class.
# 2. POLYMORPHIC DISPATCH: Each gateway overrides process_payment() with custom
#    interchange calculation rules and settlement protocols.
# 3. METHOD RESOLUTION ORDER (MRO): Python's C3 linearization resolves method
#    lookups across multiple inheritance hierarchies unambiguously.
# =====================================================================

class AuditLogMixin:
    """Injects structured operational audit logging across gateway subclasses."""
    def log_event(self, action: str) -> None:
        # self.__class__.__name__ dynamically captures the concrete runtime subclass
        print(f"[AUDIT] {self.__class__.__name__}: {action}")

class FraudScreeningMixin:
    """Provides heuristic fraud screening checks for high-volume transactions."""
    def is_suspicious(self, amount: float) -> bool:
        return amount > 10_000.0 # Flag transactions over $10,000

class PaymentGateway:
    """Contractual base class for all payment provider adapters."""
    def __init__(self, merchant_id: str):
        self.merchant_id = merchant_id

    def process_payment(self, txn_id: str, amount: float) -> tuple[bool, float, str]:
        return True, amount, "Processed"

class CreditCardGateway(PaymentGateway, AuditLogMixin, FraudScreeningMixin):
    """Credit Card processor charging 2.9% + $0.30 with automatic fraud screening."""
    def process_payment(self, txn_id: str, amount: float) -> tuple[bool, float, str]:
        # Step 1: Run inherited fraud check
        if self.is_suspicious(amount):
            self.log_event(f"({txn_id}): FRAUD HELD ${amount:,.2f} (Exceeds Limit)")
            return False, 0.0, "Fraud check failed"
        
        # Step 2: Calculate net merchant payout after interchange fees
        net = amount * (1.0 - 0.029) - 0.30
        self.log_event(f"({txn_id}): Settled ${amount:,.2f} (Net Payout: ${net:,.2f})")
        return True, net, "Settled"

class CryptoGateway(PaymentGateway, AuditLogMixin):
    """Blockchain crypto processor charging 1% + $4.50 gas fee."""
    def process_payment(self, txn_id: str, amount: float) -> tuple[bool, float, str]:
        net = amount * (1.0 - 0.01) - 4.50
        self.log_event(f"({txn_id}): Mined on Ethereum ${amount:,.2f} (Net Payout: ${net:,.2f})")
        return True, net, "Mined"

# Step 3: Execute Settlement Pipeline
print("==================================================")
print("        MERCHANT PAYMENT SETTLEMENT RUN           ")
print("==================================================")
cc = CreditCardGateway("M-01")
crypto = CryptoGateway("M-01")

cc.process_payment("TXN-101", 150.00)
crypto.process_payment("TXN-102", 500.00)
cc.process_payment("TXN-103", 12000.00) # Fraud hold triggered
print("==================================================")
```
</details>

---

## 2. Financial Investment Portfolio & Asset Vector Engine

### 🏢 Real-Life Scenario
A quantitative hedge fund tracks equity positions with encapsulated share volumes, market prices, Net Asset Value calculations, and container indexing.

### 📋 Requirements
1. Class `Holding` with `@property` for `shares` (non-negative) and `price` (positive).
2. Class `Portfolio` supporting `len(portfolio)`, `portfolio["AAPL"]`, and `item in portfolio`.

### 🎯 Expected Output
```text
==================================================
          QUANTITATIVE PORTFOLIO AUDIT            
==================================================
Portfolio Positions (len): 2 equities
Direct Lookup [NVDA]:      NVDA (30.00 shs @ $850.00)
Total Portfolio NAV:       $34,775.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 2: Financial Portfolio & Vector Arithmetic Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. PROPERTY ENCAPSULATION: @property getters/setters guard domain invariants
#    (shares >= 0, price > 0), raising ValueError upon illegal mutation.
# 2. PYTHON CONTAINER PROTOCOL:
#    - __len__: Implements len(portfolio)
#    - __getitem__: Implements portfolio['TICKER'] dictionary-style bracket lookup
#    - __contains__: Implements 'TICKER' in portfolio
# =====================================================================

class Holding:
    """Encapsulates single equity position with strict validated properties."""
    def __init__(self, ticker: str, shares: float, price: float):
        self.ticker = ticker.upper()
        self.shares = shares # Invokes @shares.setter
        self.price = price   # Invokes @price.setter

    @property
    def shares(self) -> float:
        return self._shares

    @shares.setter
    def shares(self, val: float):
        if val < 0:
            raise ValueError("Shares count cannot be negative")
        self._shares = float(val)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, val: float):
        if val <= 0:
            raise ValueError("Market price must be strictly positive")
        self._price = float(val)

    @property
    def market_value(self) -> float:
        """Computed read-only property returning current position valuation."""
        return self._shares * self._price

    def __str__(self) -> str:
        return f"{self.ticker} ({self.shares:.2f} shs @ ${self.price:.2f})"

class Portfolio:
    """Manages investment portfolio holdings and Net Asset Value (NAV) aggregation."""
    def __init__(self, cash: float = 0.0):
        self.cash = cash
        self._holdings: dict[str, Holding] = {}

    def add_holding(self, h: Holding) -> None:
        self._holdings[h.ticker] = h

    def __len__(self) -> int:
        return len(self._holdings)

    def __getitem__(self, ticker: str) -> Holding:
        return self._holdings[ticker.upper()]

    def __contains__(self, ticker: str) -> bool:
        return ticker.upper() in self._holdings

    @property
    def total_nav(self) -> float:
        """Calculates total Net Asset Value across cash and all equity positions."""
        return self.cash + sum(h.market_value for h in self._holdings.values())

# Execute Simulation
p = Portfolio(cash=1000.0)
p.add_holding(Holding("AAPL", 45.0, 185.00))
p.add_holding(Holding("NVDA", 30.0, 850.00))

print("==================================================")
print("          QUANTITATIVE PORTFOLIO AUDIT            ")
print("==================================================")
print(f"Portfolio Positions (len): {len(p)} equities")
print(f"Direct Lookup [NVDA]:      {p['NVDA']}")
print(f"Total Portfolio NAV:       ${p.total_nav:,.2f}")
print("==================================================")
```
</details>

---

## 3. Microservice Health Monitor with ABC Plugins

### 🏢 Real-Life Scenario
A cloud infrastructure platform requires pluggable health probes (HTTP, Database, Redis) conforming to an Abstract Base Class contract.

### 📋 Requirements
1. Abstract base `BaseHealthProbe(ABC)` with `@abstractmethod def check_health(self) -> dict`.
2. Implement `DatabaseProbe` and `HttpEndpointProbe`.

### 🎯 Expected Output
```text
==================================================
        MICROSERVICE CLUSTER HEALTH PROBE         
==================================================
  ✓ DB_PROBE:       ONLINE (Latency: 12ms)
  ✓ HTTP_AUTH_API:  ONLINE (Latency: 45ms)
Cluster Status: 100% HEALTHY
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 3: Microservice Cluster Health Monitor with ABC Plugins
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. ABSTRACT BASE CLASSES (ABCs): BaseHealthProbe inherits from abc.ABC and decorates
#    check_health with @abstractmethod. Any subclass missing this method cannot be instantiated.
# 2. PLUGIN EXTENSIBILITY: Enables zero-friction addition of new probe types (Redis, RabbitMQ)
#    while guaranteeing uniform interface contracts.
# =====================================================================

from abc import ABC, abstractmethod

class BaseHealthProbe(ABC):
    """Abstract interface contract for all infrastructure health checks."""
    def __init__(self, target: str):
        self.target = target

    @abstractmethod
    def check_health(self) -> dict:
        """Must return a dictionary containing status and latency metrics."""
        pass

class DatabaseProbe(BaseHealthProbe):
    """Concrete probe testing PostgreSQL database latency."""
    def check_health(self) -> dict:
        return {"service": self.target, "status": "ONLINE", "latency_ms": 12}

class HttpEndpointProbe(BaseHealthProbe):
    """Concrete probe testing REST API gateway latency."""
    def check_health(self) -> dict:
        return {"service": self.target, "status": "ONLINE", "latency_ms": 45}

# Step 3: Probe Collection & Health Audit
probes = [DatabaseProbe("DB_PROBE"), HttpEndpointProbe("HTTP_AUTH_API")]

print("==================================================")
print("        MICROSERVICE CLUSTER HEALTH PROBE         ")
print("==================================================")
for p in probes:
    res = p.check_health()
    print(f"  ✓ {res['service']:<15} {res['status']} (Latency: {res['latency_ms']}ms)")
print("Cluster Status: 100% HEALTHY")
print("==================================================")
```
</details>

---

## 4. Core Banking Wire Transfer with Custom Exception Hierarchy

### 🏢 Real-Life Scenario
A financial ledger enforces domain error handling with custom exceptions: `BankingError`, `InsufficientFundsError`, and `AccountFrozenError`.

### 📋 Requirements
1. Base exception `BankingError(Exception)`.
2. Subclasses: `InsufficientFundsError(amount, available)` and `AccountFrozenError(acc_id)`.
3. Handle exceptions cleanly in a transaction processor.

### 🎯 Expected Output
```text
==================================================
         CORE BANKING EXCEPTION HANDLER           
==================================================
[OVERDRAFT REJECTED] Account 'ACC-101': Cannot transfer $800.00 with only $250.00 available.
[COMPLIANCE ALERT]   Account 'ACC-999': Account is FROZEN due to security lock!
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 4: Core Banking Settlement with Custom Exception Hierarchy
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. HIERARCHICAL DOMAIN EXCEPTIONS:
#    - BankingError(Exception): Base root storing machine-readable error codes.
#    - InsufficientFundsError: Captures quantitative liquidity deficit metrics.
#    - AccountFrozenError: Communicates compliance lockouts.
# 2. PRECISE EXCEPTION CATCHING: Allows granular, tailored error handling per failure mode.
# =====================================================================

class BankingError(Exception):
    """Root exception for all domain-specific banking failures."""
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code # Machine-readable error code for API response serialization

class InsufficientFundsError(BankingError):
    """Raised when withdrawal/wire exceeds liquid account balance."""
    def __init__(self, acc_id: str, requested: float, available: float):
        super().__init__(
            f"Account '{acc_id}': Cannot transfer ${requested:.2f} with only ${available:.2f} available.",
            code="E402_OVERDRAFT"
        )
        self.requested = requested
        self.available = available

class AccountFrozenError(BankingError):
    """Raised when an account is locked by compliance or fraud prevention."""
    def __init__(self, acc_id: str):
        super().__init__(f"Account '{acc_id}': Account is FROZEN due to security lock!", code="E403_FROZEN")

def execute_wire(acc_id: str, balance: float, amount: float, is_frozen: bool):
    """Executes wire transfer, asserting account health before mutation."""
    if is_frozen:
        raise AccountFrozenError(acc_id)
    if amount > balance:
        raise InsufficientFundsError(acc_id, amount, balance)
    return balance - amount

print("==================================================")
print("         CORE BANKING EXCEPTION HANDLER           ")
print("==================================================")
try:
    execute_wire("ACC-101", balance=250.00, amount=800.00, is_frozen=False)
except InsufficientFundsError as err:
    print(f"[OVERDRAFT REJECTED] {err}")

try:
    execute_wire("ACC-999", balance=5000.00, amount=100.00, is_frozen=True)
except AccountFrozenError as err:
    print(f"[COMPLIANCE ALERT]   {err}")
print("==================================================")
```
</details>

---

## 5. Real-Time Cloud Server Telemetry & Anomaly Streamer

### 🏢 Real-Life Scenario
A cloud telemetry ingestor streams server metrics, filtering high-load CPU spikes on-the-fly using memory-efficient generator pipelines.

### 📋 Requirements
1. Generator `stream_metrics(samples)` yielding parsed metric dictionaries.
2. Generator `filter_cpu_anomalies(stream, threshold=85.0)` yielding filtered alerts.

### 🎯 Expected Output
```text
==================================================
       TELEMETRY GENERATOR STREAMING PIPELINE     
==================================================
🚨 [ANOMALY DETECTED] Node 'srv-02': CPU 92.4% > 85.0%
🚨 [ANOMALY DETECTED] Node 'srv-05': CPU 98.0% > 85.0%
--------------------------------------------------
Total Anomalies Filtered: 2
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 5: Real-Time Telemetry Streaming Generator Pipeline
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. GENERATOR PIPELINING: Chains 'yield' functions together for lazy evaluation.
# 2. ZERO BUFFER ALLOCATION: Metrics flow one-by-one from string parsing to threshold
#    filtering with O(1) constant memory complexity, scaling to billions of log rows.
# =====================================================================

def stream_metrics(raw_records: list[str]):
    """Generator stage 1: Parses raw comma-separated telemetry strings into dictionaries."""
    for rec in raw_records:
        node, cpu_str, mem_str = rec.split(",")
        yield {"node": node, "cpu": float(cpu_str), "mem": float(mem_str)}

def filter_cpu_anomalies(metric_stream, threshold: float = 85.0):
    """Generator stage 2: Lazy filter yielding only records breaching CPU safety threshold."""
    for m in metric_stream:
        if m["cpu"] > threshold:
            yield m

raw_data = ["srv-01,34.0,40.0", "srv-02,92.4,75.0", "srv-03,45.0,50.0", "srv-05,98.0,91.0"]

# Chain generator stages
stream = stream_metrics(raw_data)
anomalies = filter_cpu_anomalies(stream, threshold=85.0)

print("==================================================")
print("       TELEMETRY GENERATOR STREAMING PIPELINE     ")
print("==================================================")
count = 0
for a in anomalies:
    count += 1
    print(f"🚨 [ANOMALY DETECTED] Node '{a['node']}': CPU {a['cpu']}% > 85.0%")
print("-" * 50)
print(f"Total Anomalies Filtered: {count}")
print("==================================================")
```
</details>

---

## 6. API Endpoint Security, Rate-Limiting & Memoization Decorator Suite

### 🏢 Real-Life Scenario
A microservice framework uses stacked decorators to enforce role permissions and memoize deterministic responses in a closure-backed cache.

### 📋 Requirements
1. Parameterized decorator `@require_role({"ADMIN"})`.
2. Decorator `@memoize_cache` storing responses in a closure dictionary.

### 🎯 Expected Output
```text
==================================================
        DECORATOR SECURITY & CACHING SUITE        
==================================================
🔄 [LIVE EXEC] Queried quarterly financial report for Q3
Report Data: $4,850,000.00
⚡ [CACHE HIT] Returned instant cached report for Q3
Report Data: $4,850,000.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 6: API Endpoint Security & Memoization Decorator Suite
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. PARAMETERIZED DECORATOR (@require_role): Uses a 3-tier closure to accept
#    configuration arguments (allowed_roles) and enforce RBAC permission gates.
# 2. CLOSURE-BACKED CACHE (@memoize_cache): Maintains an encapsulated cache = {}
#    dictionary in outer function scope, returning cached values on repeated calls.
# 3. METADATA PRESERVATION: @functools.wraps preserves function names and signatures.
# =====================================================================

import functools

def require_role(allowed_roles: set[str]):
    """Decorator factory asserting caller role matches allowed authorization set."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user_role: str, *args, **kwargs):
            if user_role not in allowed_roles:
                raise PermissionError(f"Access Denied: Role '{user_role}' unauthorized!")
            return func(user_role, *args, **kwargs)
        return wrapper
    return decorator

def memoize_cache(func):
    """Decorator caching deterministic function results inside an enclosed dictionary."""
    cache = {}
    @functools.wraps(func)
    def wrapper(user_role: str, quarter: str):
        if quarter in cache:
            print(f"⚡ [CACHE HIT] Returned instant cached report for {quarter}")
            return cache[quarter]
        
        result = func(user_role, quarter)
        cache[quarter] = result
        print(f"🔄 [LIVE EXEC] Queried quarterly financial report for {quarter}")
        return result
    return wrapper

@require_role({"ADMIN"})
@memoize_cache
def fetch_financial_report(user_role: str, quarter: str) -> float:
    """Protected expensive financial calculation."""
    return 4_850_000.00

print("==================================================")
print("        DECORATOR SECURITY & CACHING SUITE        ")
print("==================================================")
r1 = fetch_financial_report("ADMIN", "Q3") # First call: Cache miss, live computation
print(f"Report Data: ${r1:,.2f}")

r2 = fetch_financial_report("ADMIN", "Q3") # Second call: Cache hit, instant return
print(f"Report Data: ${r2:,.2f}")
print("==================================================")
```
</details>

---

## 7. ACID Database Transaction & File Sandbox Context Manager

### 🏢 Real-Life Scenario
A database context manager creates a snapshot of data upon `__enter__`, committing upon success or performing an atomic rollback upon runtime error in `__exit__`.

### 📋 Requirements
1. Class `AtomicTransaction` implementing `__enter__` and `__exit__`.
2. Automatically restore snapshot dictionary if an error occurs.

### 🎯 Expected Output
```text
==================================================
        ATOMIC TRANSACTION CONTEXT MANAGER        
==================================================
🔄 [BEGIN TXN] Snapshot created.
🚨 [ROLLBACK] Transfer error: Socket Timeout
  -> Reverted database changes to snapshot!
Reconciled Balance: Elena: $1000.00 | Marcus: $500.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 7: ACID Database Transaction & Snapshot Rollback Engine
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. CONTEXT MANAGER PROTOCOL:
#    - __enter__: Takes a deepcopy snapshot of state before user mutations begin.
#    - __exit__: Inspects exc_type. If non-None, rolls back state from snapshot.
# 2. EXCEPTION SUPPRESSION: Returning True from __exit__ tells Python the error was
#    safely recovered and prevents process termination.
# =====================================================================

import copy

class AtomicTransaction:
    """Context manager providing atomicity (all-or-nothing rollback) over dictionaries."""
    def __init__(self, db: dict):
        self.db = db
        self.snapshot = None

    def __enter__(self):
        # Create isolated deep copy of state upon block entry
        self.snapshot = copy.deepcopy(self.db)
        print("🔄 [BEGIN TXN] Snapshot created.")
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Unhandled error occurred: Rollback to original snapshot
            self.db.clear()
            self.db.update(self.snapshot)
            print(f"🚨 [ROLLBACK] Transfer error: {exc_val}")
            print("  -> Reverted database changes to snapshot!")
            return True # Suppress exception to handle failure gracefully

database = {"Elena": 1000.0, "Marcus": 500.0}

print("==================================================")
print("        ATOMIC TRANSACTION CONTEXT MANAGER        ")
print("==================================================")
with AtomicTransaction(database) as db:
    db["Elena"] -= 400.0
    # Simulate sudden network socket crash halfway through transaction
    raise ConnectionError("Socket Timeout")
    db["Marcus"] += 400.0

print(f"Reconciled Balance: Elena: ${database['Elena']:.2f} | Marcus: ${database['Marcus']:.2f}")
print("==================================================")
```
</details>

---

## 8. E-Commerce Order Pricing Engine with Comprehensive Pytest Suite

### 🏢 Real-Life Scenario
An order calculation engine applies tiered discounts and free shipping rules with automated unit test assertions.

### 📋 Requirements
1. `calculate_order(subtotal: float, tier: str) -> float` (Bronze: 0%, Silver: 5%, Gold: 10%, Platinum: 20%).
2. Automated test suite using `assert` testing valid discounts and negative boundary exceptions.

### 🎯 Expected Output
```text
==================================================
        E-COMMERCE PRICING UNIT TEST SUITE        
==================================================
  ✓ test_bronze_tier_discount:    PASSED ($100 -> $100.00)
  ✓ test_gold_tier_discount:      PASSED ($100 -> $90.00)
  ✓ test_platinum_tier_discount:  PASSED ($100 -> $80.00)
  ✓ test_negative_subtotal_error: PASSED (ValueError Caught)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 8: E-Commerce Pricing & Automated Unit Test Suite
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. DOMAIN PRICING FUNCTION: Validates non-negative subtotals and applies tiered multipliers.
# 2. AUTOMATED UNIT ASSERTIONS: Uses assert expressions to test valid calculations and
#    exception assertions to verify boundary rejections.
# =====================================================================

DISCOUNTS = {"BRONZE": 0.00, "SILVER": 0.05, "GOLD": 0.10, "PLATINUM": 0.20}

def calculate_order(subtotal: float, tier: str) -> float:
    """Calculates discounted order total based on customer membership tier."""
    if subtotal < 0:
        raise ValueError("Subtotal cannot be negative")
    rate = DISCOUNTS[tier.upper()]
    return round(subtotal * (1.0 - rate), 2)

# Automated Test Runner Suite
def run_pricing_tests():
    """Executes automated test cases asserting pricing rules and exception boundaries."""
    print("==================================================")
    print("        E-COMMERCE PRICING UNIT TEST SUITE        ")
    print("==================================================")
    
    # Test Case 1: Bronze (0% Discount)
    assert calculate_order(100.0, "BRONZE") == 100.00
    print("  ✓ test_bronze_tier_discount:    PASSED ($100 -> $100.00)")
    
    # Test Case 2: Gold (10% Discount)
    assert calculate_order(100.0, "GOLD") == 90.00
    print("  ✓ test_gold_tier_discount:      PASSED ($100 -> $90.00)")

    # Test Case 3: Platinum (20% Discount)
    assert calculate_order(100.0, "PLATINUM") == 80.00
    print("  ✓ test_platinum_tier_discount:  PASSED ($100 -> $80.00)")

    # Test Case 4: Exception Boundary Assertion
    try:
        calculate_order(-50.0, "GOLD")
        assert False, "Failed: Should have raised ValueError on negative subtotal!"
    except ValueError:
        print("  ✓ test_negative_subtotal_error: PASSED (ValueError Caught)")
        
    print("==================================================")

run_pricing_tests()
```
</details>

---

## 9. Multi-Cloud Resource Orchestrator with Mixins

### 🏢 Real-Life Scenario
A multi-cloud deployment manager provisions compute instances across AWS and GCP, logging audit events via a Mixin class.

### 📋 Requirements
1. `AuditMixin` injecting `.audit_log(msg)`.
2. Base `CloudResource` with `.start()` and polymorphic `.get_monthly_cost()`.

### 🎯 Expected Output
```text
==================================================
        MULTI-CLOUD INFRASTRUCTURE AUDITOR        
==================================================
[AUDIT] AWS_EC2 (i-901): Initialized in us-east-1 ($146.00/mo)
[AUDIT] GCP_Compute (gcp-44): Initialized in europe-west1 ($365.00/mo)
Total Fleet Spend: $511.00/mo
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 9: Multi-Cloud Orchestrator with Mixins
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. MIXIN SEPARATION: AuditMixin provides reusable telemetry across AWS and GCP.
# 2. STANDARDIZED COSTING: Computes monthly run rates assuming 730 average hours/month.
# =====================================================================

class AuditMixin:
    """Mixin class providing structured logging without altering core resource logic."""
    def audit_log(self, msg: str) -> None:
        print(f"[AUDIT] {self.__class__.__name__} ({self.res_id}): {msg}")

class CloudResource(AuditMixin):
    """Base class for all provisioned multi-cloud virtual compute nodes."""
    def __init__(self, res_id: str, region: str, hourly: float):
        self.res_id = res_id
        self.region = region
        self.hourly = hourly

    def get_monthly_cost(self) -> float:
        return self.hourly * 730.0 # 730 hours per billing month

class AWS_EC2(CloudResource):
    """Amazon Web Services compute instance."""
    pass

class GCP_Compute(CloudResource):
    """Google Cloud Platform compute instance."""
    pass

# Execute Provisioning Simulation
fleet = [AWS_EC2("i-901", "us-east-1", hourly=0.20), GCP_Compute("gcp-44", "europe-west1", hourly=0.50)]

print("==================================================")
print("        MULTI-CLOUD INFRASTRUCTURE AUDITOR        ")
print("==================================================")
tot = 0.0
for res in fleet:
    cost = res.get_monthly_cost()
    tot += cost
    res.audit_log(f"Initialized in {res.region} (${cost:.2f}/mo)")
print(f"Total Fleet Spend: ${tot:.2f}/mo")
print("==================================================")
```
</details>

---

## 10. Cross-Border Fintech Multi-Currency Digital Wallet

### 🏢 Real-Life Scenario
A fintech wallet supports multi-currency arithmetic (`+`, `-`, `*`), preventing accidental cross-currency additions via operator overloading.

### 📋 Requirements
1. Value object `Money` overloading `__add__`, `__sub__`, and `__eq__`.
2. Enforce matching currency codes on arithmetic operations.

### 🎯 Expected Output
```text
==================================================
          FINTECH MULTI-CURRENCY WALLET           
==================================================
USD Addition: $500.00 USD + $250.00 USD = $750.00 USD
Fee Scale:    $750.00 USD * 0.98 = $735.00 USD
Mismatch:     🚨 Error Caught: Currency mismatch: USD vs EUR
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 10: Multi-Currency Value Object & Operator Overloader
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. VALUE OBJECT PATTERN: Encapsulates immutable numeric amount and currency string.
# 2. OPERATOR OVERLOADING: Overrides __add__ and __mul__ with currency boundary checks,
#    preventing illegal cross-currency addition bugs.
# =====================================================================

class Money:
    """Immutable monetary value object supporting type-safe operator arithmetic."""
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = round(float(amount), 2)
        self.currency = currency.upper()

    def __add__(self, other: 'Money') -> 'Money':
        """Enforces matching currencies before performing addition."""
        if self.currency != other.currency:
            raise ValueError(f"Currency mismatch: {self.currency} vs {other.currency}")
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: float) -> 'Money':
        """Supports scalar multiplication (e.g. fee scaling)."""
        return Money(self.amount * factor, self.currency)

    def __str__(self) -> str:
        return f"${self.amount:.2f} {self.currency}"

# Execute Simulation
print("==================================================")
print("          FINTECH MULTI-CURRENCY WALLET           ")
print("==================================================")
m1 = Money(500.0, "USD")
m2 = Money(250.0, "USD")
m_sum = m1 + m2
print(f"USD Addition: {m1} + {m2} = {m_sum}")
print(f"Fee Scale:    {m_sum} * 0.98 = {m_sum * 0.98}")

# Verify cross-currency protection
try:
    _ = m1 + Money(100.0, "EUR")
except ValueError as ex:
    print(f"Mismatch:     🚨 Error Caught: {ex}")
print("==================================================")
```
</details>

---

## 11. Resilient Database Query Retry & Performance Profiler

### 🏢 Real-Life Scenario
A database driver decorator automatically retries flaky network queries up to 3 times before failing, measuring execution duration.

### 📋 Requirements
1. Parameterized decorator `@retry_on_failure(max_retries=3)`.
2. Measure duration in milliseconds.

### 🎯 Expected Output
```text
==================================================
        DATABASE RETRY & PERFORMANCE SUITE        
==================================================
⚠️ [Attempt 1/3] Failed: Socket drop. Retrying...
⚠️ [Attempt 2/3] Failed: Socket drop. Retrying...
✅ [Attempt 3/3] Succeeded in 1.45ms -> Returned 25 rows
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 11: Resilient Database Query Retry & Latency Profiler
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. TRANSIENT FAULT RECOVERY: Intercepts network exceptions in a bounded loop (up to max_retries).
# 2. HIGH-RESOLUTION TIMING: Uses time.perf_counter() to measure sub-millisecond query durations.
# =====================================================================

import functools
import time

def retry_on_failure(max_retries: int = 3):
    """Decorator retrying flaky database calls before bubbling exceptions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    start = time.perf_counter()
                    res = func(*args, **kwargs)
                    ms = (time.perf_counter() - start) * 1000.0
                    print(f"✅ [Attempt {attempt}/{max_retries}] Succeeded in {ms:.2f}ms -> Returned {res['rows']} rows")
                    return res
                except Exception as err:
                    print(f"⚠️ [Attempt {attempt}/{max_retries}] Failed: {err}. Retrying...")
            raise RuntimeError("All retries exhausted")
        return wrapper
    return decorator

# Flaky DB Query Simulation
counter = 0
@retry_on_failure(max_retries=3)
def query_database(sql: str) -> dict:
    global counter
    counter += 1
    if counter < 3: # Fail first 2 attempts
        raise ConnectionError("Socket drop")
    return {"rows": 25, "sql": sql}

print("==================================================")
print("        DATABASE RETRY & PERFORMANCE SUITE        ")
print("==================================================")
query_database("SELECT * FROM users")
print("==================================================")
```
</details>

---

## 12. Sensor Time-Series Moving Average Generator Pipeline

### 🏢 Real-Life Scenario
An industrial IoT pipeline streams continuous temperature readings, calculating a 3-sample rolling average without list allocation.

### 📋 Requirements
1. Generator yielding rolling moving averages over a continuous sensor stream.

### 🎯 Expected Output
```text
==================================================
       IOT SENSOR ROLLING AVERAGE STREAM          
==================================================
Sample: 20.0°C | Rolling 3-Avg: 20.00°C
Sample: 22.0°C | Rolling 3-Avg: 21.00°C
Sample: 24.0°C | Rolling 3-Avg: 22.00°C
Sample: 26.0°C | Rolling 3-Avg: 24.00°C
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 12: IoT Sensor Streaming Moving Average Pipeline
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. BOUNDED DEQUE: collections.deque(maxlen=window_size) automatically purges
#    stale samples from the left, maintaining constant O(1) memory overhead.
# 2. LAZY GENERATOR: Yields rolling averages as new data points stream in.
# =====================================================================

from collections import deque

def rolling_average_stream(sensor_stream, window_size: int = 3):
    """Yields streaming rolling averages across a sliding window of sensor data."""
    window = deque(maxlen=window_size)
    for val in sensor_stream:
        window.append(val)
        avg = sum(window) / len(window)
        yield val, avg

readings = [20.0, 22.0, 24.0, 26.0]

print("==================================================")
print("       IOT SENSOR ROLLING AVERAGE STREAM          ")
print("==================================================")
for val, avg in rolling_average_stream(readings, window_size=3):
    print(f"Sample: {val:.1f}°C | Rolling 3-Avg: {avg:.2f}°C")
print("==================================================")
```
</details>

---

## 13. Pluggable Encryption & Compression Stream Filter Engine

### 🏢 Real-Life Scenario
A security middleware framework chains data transformers (Base64 encoding, ROT13 cipher) conforming to an abstract stream interface.

### 📋 Requirements
1. Abstract base `StreamFilter(ABC)` with `@abstractmethod def process(self, text: str) -> str`.
2. Pipeline chaining multiple filters.

### 🎯 Expected Output
```text
==================================================
       PLUGGABLE STREAM FILTER TRANSFORMATION     
==================================================
Original Text:  confidential_payroll_data
Step 1:        CONFIDENTIAL_PAYROLL_DATA
Step 2:        ***CONFIDENTIAL_PAYROLL_DATA***
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 13: Pluggable Stream Filter Transformation Pipeline
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. PIPELINE PATTERN: Composable filter objects subclass StreamFilter ABC.
# 2. SEQUENTIAL ENCAPSULATION: Output of filter N feeds into filter N+1.
# =====================================================================

from abc import ABC, abstractmethod

class StreamFilter(ABC):
    """Abstract interface contract for all payload stream transformers."""
    @abstractmethod
    def process(self, text: str) -> str:
        pass

class MaskFilter(StreamFilter):
    """Wraps text in security audit framing masks."""
    def process(self, text: str) -> str:
        return f"***{text}***"

class UpperFilter(StreamFilter):
    """Converts stream payloads to uppercase."""
    def process(self, text: str) -> str:
        return text.upper()

filters = [UpperFilter(), MaskFilter()]
payload = "confidential_payroll_data"

print("==================================================")
print("       PLUGGABLE STREAM FILTER TRANSFORMATION     ")
print("==================================================")
print(f"Original Text:  {payload}")
current = payload
for idx, f in enumerate(filters, start=1):
    current = f.process(current)
    print(f"Step {idx}:        {current}")
print("==================================================")
```
</details>

---

## 14. Role-Based Access Control (RBAC) Permission Decorator Framework

### 🏢 Real-Life Scenario
A web API uses a role permission decorator to protect admin-only operations from guest access.

### 📋 Requirements
1. Decorator `@require_permission("CAN_DELETE")`.
2. Inspect user context object.

### 🎯 Expected Output
```text
==================================================
         RBAC PERMISSION DECORATOR AUDIT          
==================================================
✅ Admin deleted record 'USR-901'
🚨 Error: User lacks required permission 'CAN_DELETE'
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 14: RBAC Permission Guard Decorator Framework
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. CONTEXT-AWARE DECORATOR: Inspects user context dictionary permissions set
#    before executing protected business methods.
# 2. FAIL-FAST SECURITY: Aborts unauthorized calls with PermissionError.
# =====================================================================

import functools

def require_permission(perm: str):
    """Decorator asserting user context contains required operational permission."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user: dict, *args, **kwargs):
            if perm not in user.get("permissions", set()):
                raise PermissionError(f"User lacks required permission '{perm}'")
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_permission("CAN_DELETE")
def delete_database_record(user: dict, record_id: str):
    """Sensitive deletion operation requiring elevated permissions."""
    print(f"✅ {user['name']} deleted record '{record_id}'")

admin = {"name": "Admin", "permissions": {"CAN_DELETE", "CAN_WRITE"}}
guest = {"name": "Guest", "permissions": {"CAN_READ"}}

print("==================================================")
print("         RBAC PERMISSION DECORATOR AUDIT          ")
print("==================================================")
delete_database_record(admin, "USR-901")

try:
    delete_database_record(guest, "USR-901")
except PermissionError as ex:
    print(f"🚨 Error: {ex}")
print("==================================================")
```
</details>

---

## 15. Secure Temporary API Token Leasing Context Manager

### 🏢 Real-Life Scenario
An automation runner leases a temporary cryptographic token that must be revoked immediately when the code block exits.

### 📋 Requirements
1. Context manager `lease_api_token(user: str)` using `@contextlib.contextmanager`.
2. Revoke token in `finally` block.

### 🎯 Expected Output
```text
==================================================
       TEMPORARY TOKEN LEASING CONTEXT            
==================================================
🔑 [LEASED] Token 'TOK_8812' assigned to Elena
  -> Executing secure cloud operations with TOK_8812...
🔒 [REVOKED] Token 'TOK_8812' purged from active lease table
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 15: Temporary Token Leasing Lifecycle Context Manager
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. @contextlib.contextmanager: Simplifies context manager implementation using generator syntax.
# 2. GUARANTEED REVOCATION: The finally: block ensures token revocation occurs even if
#    exceptions occur during execution.
# =====================================================================

import contextlib

@contextlib.contextmanager
def lease_api_token(user: str):
    """Leases a temporary credential, guaranteeing revocation upon block exit."""
    token = "TOK_8812"
    print(f"🔑 [LEASED] Token '{token}' assigned to {user}")
    try:
        yield token # Caller receives leased token
    finally:
        # Guaranteed cleanup / revocation
        print(f"🔒 [REVOKED] Token '{token}' purged from active lease table")

print("==================================================")
print("       TEMPORARY TOKEN LEASING CONTEXT            ")
print("==================================================")
with lease_api_token("Elena") as tok:
    print(f"  -> Executing secure cloud operations with {tok}...")
print("==================================================")
```
</details>

---

## 16. Asynchronous Event Dispatcher with ABC Subscriber Interfaces

### 🏢 Real-Life Scenario
An event broadcast engine notifies subscribers (Email, Slack) of critical incidents.

### 📋 Requirements
1. Abstract class `EventSubscriber(ABC)` with `@abstractmethod def on_event(self, event: str)`.
2. Register and broadcast events to all subscribers.

### 🎯 Expected Output
```text
==================================================
         INCIDENT EVENT BROADCAST ENGINE          
==================================================
📢 Broadcasting Event: 'DATABASE_FAILOVER_TRIGGERED'
  • [EMAIL] Sent alert to devops@company.com: DATABASE_FAILOVER_TRIGGERED
  • [SLACK] Posted to #oncall-alerts: DATABASE_FAILOVER_TRIGGERED
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 16: Incident Event Bus & Observer Dispatcher
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. OBSERVER PATTERN: Decouples event publishers from diverse subscriber channels.
# 2. ABC SUBSCRIBERS: Enforces that all notification adapters implement on_event().
# =====================================================================

from abc import ABC, abstractmethod

class EventSubscriber(ABC):
    """Abstract interface for all notification channel listeners."""
    @abstractmethod
    def on_event(self, event_name: str) -> None:
        pass

class EmailSubscriber(EventSubscriber):
    def on_event(self, event_name: str) -> None:
        print(f"  • [EMAIL] Sent alert to devops@company.com: {event_name}")

class SlackSubscriber(EventSubscriber):
    def on_event(self, event_name: str) -> None:
        print(f"  • [SLACK] Posted to #oncall-alerts: {event_name}")

class EventBus:
    """Manages active subscriber registry and event dispatching."""
    def __init__(self):
        self._subs: list[EventSubscriber] = []

    def subscribe(self, sub: EventSubscriber):
        self._subs.append(sub)

    def publish(self, event: str):
        print(f"📢 Broadcasting Event: '{event}'")
        for s in self._subs:
            s.on_event(event)

# Execute Simulation
bus = EventBus()
bus.subscribe(EmailSubscriber())
bus.subscribe(SlackSubscriber())

print("==================================================")
print("         INCIDENT EVENT BROADCAST ENGINE          ")
print("==================================================")
bus.publish("DATABASE_FAILOVER_TRIGGERED")
print("==================================================")
```
</details>

---

## 17. Custom Vector Math Library with Dunder Operator Overloading

### 🏢 Real-Life Scenario
A 2D physics engine needs a `Vector2D` class with vector addition, scalar multiplication, and magnitude comparisons.

### 📋 Requirements
1. Overload `__add__`, `__mul__`, `__abs__`, and `__str__`.

### 🎯 Expected Output
```text
==================================================
            VECTOR2D ARITHMETIC ENGINE            
==================================================
v1: (3.0, 4.0) | Magnitude: 5.00
v2: (1.0, 2.0)
v1 + v2: (4.0, 6.0)
v1 * 2:  (6.0, 8.0)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 17: Vector2D Mathematical Dunder Operator Library
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. MAGIC DUNDER OVERLOADS:
#    - __add__: Vector addition (x1+x2, y1+y2)
#    - __mul__: Scalar multiplication (x*s, y*s)
#    - __abs__: Vector Euclidean magnitude: sqrt(x^2 + y^2)
# =====================================================================

import math

class Vector2D:
    """2D Euclidean vector supporting intuitive mathematical operators."""
    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)

    def __abs__(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)

print("==================================================")
print("            VECTOR2D ARITHMETIC ENGINE            ")
print("==================================================")
print(f"v1: {v1} | Magnitude: {abs(v1):.2f}")
print(f"v2: {v2}")
print(f"v1 + v2: {v1 + v2}")
print(f"v1 * 2:  {v1 * 2}")
print("==================================================")
```
</details>

---

## 18. Config File Parser with Cascading Environment Overrides

### 🏢 Real-Life Scenario
An application settings engine loads defaults from a dictionary, cascading overrides from environment variables and validating missing required keys with a custom exception.

### 📋 Requirements
1. Raise `MissingConfigError(key)` if a required setting is missing.

### 🎯 Expected Output
```text
==================================================
        CASCADING CONFIGURATION PARSER            
==================================================
Resolved Settings:
  - DB_HOST: localhost
  - DB_PORT: 5432
  - ENV:     PRODUCTION (Overridden)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 18: Cascading Application Configuration Parser
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. CASCADING MERGE: {**defaults, **env_overrides} merges settings with environment priority.
# 2. CONTRACT INVARIANT ASSERTION: Verifies all mandatory configuration keys are present.
# =====================================================================

class MissingConfigError(Exception):
    """Raised when a mandatory configuration parameter is omitted."""
    pass

def resolve_configuration(defaults: dict, env_overrides: dict, required: list[str]) -> dict:
    """Merges cascading dictionaries and validates required keys."""
    resolved = {**defaults, **env_overrides}
    for req in required:
        if req not in resolved:
            raise MissingConfigError(f"Required configuration key '{req}' is missing!")
    return resolved

defaults = {"DB_HOST": "localhost", "DB_PORT": 5432, "ENV": "DEVELOPMENT"}
overrides = {"ENV": "PRODUCTION"}
res = resolve_configuration(defaults, overrides, required=["DB_HOST", "DB_PORT"])

print("==================================================")
print("        CASCADING CONFIGURATION PARSER            ")
print("==================================================")
print("Resolved Settings:")
for k, v in res.items():
    tag = " (Overridden)" if k in overrides else ""
    print(f"  - {k:<8} {v}{tag}")
print("==================================================")
```
</details>

---

## 19. High-Throughput Log Sanitizer & Regex Masking Stream

### 🏢 Real-Life Scenario
A security log pipeline streams application logs, masking sensitive credit card numbers and Social Security numbers using a generator pipeline.

### 📋 Requirements
1. Generator yielding logs with credit card numbers masked (`XXXX-XXXX-XXXX-1234`).

### 🎯 Expected Output
```text
==================================================
        SECURITY LOG MASKING GENERATOR            
==================================================
[SANITIZED] User login from 192.168.1.1
[SANITIZED] Processed card XXXX-XXXX-XXXX-9021 for $120.00
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 19: Security Log Regex Sanitizer Generator
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. PRE-COMPILED REGEX: re.compile() optimizes pattern execution across streaming logs.
# 2. CAPTURE BACKREFERENCES: r'XXXX-XXXX-XXXX-\1' preserves last 4 digits while masking prefix.
# =====================================================================

import re

def sanitize_logs_stream(raw_logs: list[str]):
    """Streams log records, replacing sensitive 16-digit card numbers on-the-fly."""
    # Match standard 16-digit card patterns (XXXX-XXXX-XXXX-XXXX)
    card_pattern = re.compile(r"\b(?:\d{4}-){3}(\d{4})\b")
    for log in raw_logs:
        sanitized = card_pattern.sub(r"XXXX-XXXX-XXXX-\1", log)
        yield sanitized

logs = ["User login from 192.168.1.1", "Processed card 4111-2222-3333-9021 for $120.00"]

print("==================================================")
print("        SECURITY LOG MASKING GENERATOR            ")
print("==================================================")
for clean_log in sanitize_logs_stream(logs):
    print(f"[SANITIZED] {clean_log}")
print("==================================================")
```
</details>

---

## 20. Service-Level Objective (SLO) Latency Auditor with Pytest Fixtures

### 🏢 Real-Life Scenario
A quality assurance test runner benchmarks API response latencies against Service-Level Objectives (SLO: 99% of requests $< 200\text{ms}$).

### 📋 Requirements
1. `audit_slo(latencies: list[float], target_ms: float = 200.0) -> bool`.
2. Pytest unit tests asserting compliance across sample latency profiles.

### 🎯 Expected Output
```text
==================================================
        SERVICE SLO COMPLIANCE TEST RUNNER        
==================================================
  ✓ test_compliant_latency_batch:  PASSED (99.0% <= 200ms)
  ✓ test_degraded_latency_batch:   PASSED (SLO Violation Flagged)
==================================================
```

<details>
<summary><b>🔍 View Solution & In-Code Explanation</b></summary>

```python
# =====================================================================
# PROJECT 20: Service-Level Objective (SLO) Compliance Test Runner
#
# ARCHITECTURAL DESIGN & LOGIC OVERVIEW:
# 1. PERCENTILE AUDITING: Calculates the percentage of requests meeting target SLA (<200ms).
# 2. AUTOMATED ASSERTIONS: Validates healthy vs degraded latency profiles.
# =====================================================================

def audit_slo(latencies: list[float], target_ms: float = 200.0) -> bool:
    """Returns True if at least 99% of requests completed under target latency."""
    if not latencies:
        return False
    compliant_count = sum(1 for lat in latencies if lat <= target_ms)
    compliance_rate = compliant_count / len(latencies)
    return compliance_rate >= 0.99

# Test Runner Simulation
def run_slo_tests():
    print("==================================================")
    print("        SERVICE SLO COMPLIANCE TEST RUNNER        ")
    print("==================================================")
    
    good_batch = [120.0, 140.0, 180.0, 195.0, 150.0] * 20 # 100% compliant
    bad_batch = [120.0, 450.0, 320.0, 150.0]               # Degraded profile

    # Test Case 1: Healthy cluster
    assert audit_slo(good_batch, 200.0) is True
    print("  ✓ test_compliant_latency_batch:  PASSED (99.0% <= 200ms)")

    # Test Case 2: Degraded cluster
    assert audit_slo(bad_batch, 200.0) is False
    print("  ✓ test_degraded_latency_batch:   PASSED (SLO Violation Flagged)")
    print("==================================================")

run_slo_tests()
```
</details>
