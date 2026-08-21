# Lesson 1: Advanced OOP: Inheritance, Polymorphism & super()

Welcome to Level 2! In this lesson, we level up our Object-Oriented Programming (OOP) craftsmanship by mastering how classes inherit attributes, override behaviors, dynamically resolve methods via the Method Resolution Order (MRO), and achieve true polymorphic dispatch.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Architect robust class hierarchies using Single, Hierarchical, and Multiple Inheritance.
2. Delegate constructor and method calls safely using `super()`.
3. Implement Method Overriding and design uniform Polymorphic interfaces.
4. Inspect and understand the **Method Resolution Order (MRO)** algorithm (C3 Linearization).
5. Build decoupled, composable functionality using **Mixin Classes**.

---

## 1. Single & Hierarchical Inheritance

Inheritance establishes an **"is-a"** relationship (e.g., a `Manager` *is an* `Employee`). The derived child class inherits attributes and methods from its parent base class while specializing behavior.

```python
class Employee:
    def __init__(self, emp_id: str, name: str, base_salary: float):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self) -> float:
        """Base compensation calculation."""
        return self.base_salary

    def get_details(self) -> str:
        return f"[{self.emp_id}] {self.name} - Annual Pay: ${self.calculate_pay():,.2f}"

# Child Class specializing Employee
class Manager(Employee):
    def __init__(self, emp_id: str, name: str, base_salary: float, annual_bonus: float):
        # Delegate base initialization to parent class using super()
        super().__init__(emp_id, name, base_salary)
        self.annual_bonus = annual_bonus

    # Method Overriding: Specialize calculate_pay for managers
    def calculate_pay(self) -> float:
        return self.base_salary + self.annual_bonus
```

---

## 2. Polymorphic Dispatch in Practice

**Polymorphism** ("many forms") allows client code to interact with different objects through a shared interface without needing to know the concrete child class at runtime:

```python
class SoftwareEngineer(Employee):
    def __init__(self, emp_id: str, name: str, base_salary: float, equity_shares: int):
        super().__init__(emp_id, name, base_salary)
        self.equity_shares = equity_shares

    def calculate_pay(self) -> float:
        # Software engineers receive stock unit dividends added to base salary
        return self.base_salary + (self.equity_shares * 12.50)

# Polymorphic consumer function
def generate_payroll_report(staff_roster: list[Employee]) -> None:
    total_payroll = 0.0
    print("=== 💼 COMPANY PAYROLL DISBURSEMENT ===")
    for employee in staff_roster:
        # Every object responds polymorphically to .get_details() and .calculate_pay()
        print(employee.get_details())
        total_payroll += employee.calculate_pay()
    print(f"Total Department Disbursal: ${total_payroll:,.2f}")
```

---

---

## 4. Under the Hood: C3 Linearization & Method Resolution Order (MRO)

When multiple inheritance creates complex inheritance diamonds, Python determines the exact method lookup sequence using the **C3 Linearization Algorithm**:

```
        ┌───────────────┐
        │    object     │
        └───────┬───────┘
                ▲
        ┌───────┴───────┐
        │  BaseService  │
        └───────┬───────┘
          ▲           ▲
   ┌──────┴─────┐ ┌───┴─────────┐
   │ AuthMixin  │ │ LoggerMixin │
   └──────┬─────┘ └───┬─────────┘
          ▲           ▲
          └─────┬─────┘
        ┌───────┴───────┐
        │  UserService  │
        └───────────────┘
```

### 🧠 How C3 Linearization Works
1. **Local Precedence**: Subclasses appear before base classes (`UserService` before `AuthMixin`).
2. **Order of Declaration**: Classes declared first in `class Child(A, B):` take precedence over those declared later (`A` before `B`).
3. **Monotonicity**: If class $A$ precedes class $B$ in any sub-hierarchy, it must precede $B$ across the entire resolved MRO.

You can view the MRO of any class using `.mro()` or `.__mro__`:
```python
print([c.__name__ for c in SecurityLead.mro()])
# ['SecurityLead', 'Manager', 'Employee', 'TimestampAuditMixin', 'EncryptionMixin', 'object']
```

### ⚡ Cooperative Multiple Inheritance with `super()` and `**kwargs`
To ensure all parent classes in a diamond hierarchy initialize without hardcoded class names, use cooperative `super().__init__(**kwargs)`:

```python
class BaseComponent:
    def __init__(self, **kwargs):
        super().__init__() # Calls object.__init__()
        print("BaseComponent Initialized")

class LoggingComponent(BaseComponent):
    def __init__(self, log_level: str = "INFO", **kwargs):
        super().__init__(**kwargs)
        self.log_level = log_level
        print(f"LoggingComponent ({self.log_level}) Initialized")

class NetworkComponent(BaseComponent):
    def __init__(self, port: int = 8080, **kwargs):
        super().__init__(**kwargs)
        self.port = port
        print(f"NetworkComponent (Port {self.port}) Initialized")

# Diamond Child
class ServerApplication(LoggingComponent, NetworkComponent):
    def __init__(self, app_name: str, **kwargs):
        super().__init__(**kwargs)
        self.app_name = app_name
        print(f"ServerApplication '{self.app_name}' Ready!")

app = ServerApplication(app_name="OrderAPI", log_level="DEBUG", port=443)
```

---

## 5. Type Checking: `isinstance()` vs. `issubclass()` vs. `type()`

| Check | Syntax | Meaning | Handles Inheritance? |
| :--- | :--- | :--- | :---: |
| **Exact Type** | `type(obj) is Class` | Checks if `obj` was instantiated strictly from `Class` | ❌ No |
| **Instance Check** | `isinstance(obj, (Base, Mixin))` | Checks if `obj` is an instance of `Base` or any subclass | ✅ Yes |
| **Subclass Check** | `issubclass(Child, Parent)` | Checks if `Child` inherits from `Parent` | ✅ Yes |

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Multi-Channel Payment Gateway Processing Pipeline**, combining single/multiple inheritance, method overriding, `super()`, mixins, and polymorphic execution:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Enterprise Payment Gateway & Transaction Engine
# =====================================================================

class AuditLoggerMixin:
    """Mixin for compliance logging across disparate financial services."""
    def log_transaction(self, txn_id: str, status: str, amount: float) -> None:
        print(f"[AUDIT TRAIL] Service: {self.__class__.__name__:<20} | Txn: {txn_id} | Status: {status:<10} | Amount: ${amount:,.2f}")


class FraudDetectionMixin:
    """Mixin providing real-time heuristic fraud screening."""
    def scan_for_fraud(self, amount: float, account_country: str) -> bool:
        HIGH_RISK_COUNTRIES = {"XX", "ZZ"}
        if amount > 10_000.0 or account_country.upper() in HIGH_RISK_COUNTRIES:
            return True # Flagged for suspicious activity
        return False


class PaymentGateway:
    """Base payment processor class defining the standard transaction interface."""
    
    GATEWAY_PROVIDER = "Apex Global Payments Core"

    def __init__(self, merchant_id: str, api_key: str, processing_fee_pct: float = 0.029):
        self.merchant_id = merchant_id
        self.api_key = api_key
        self.processing_fee_pct = processing_fee_pct

    def compute_fee(self, amount: float) -> float:
        """Calculates default credit network fee ($0.30 flat + percentage)."""
        return (amount * self.processing_fee_pct) + 0.30

    def process_payment(self, txn_id: str, amount: float, country: str = "US") -> tuple[bool, float, str]:
        """Base payment execution template method."""
        fee = self.compute_fee(amount)
        net_settlement = amount - fee
        return True, net_settlement, f"Processed via {self.GATEWAY_PROVIDER}"


class CreditCardProcessor(PaymentGateway, AuditLoggerMixin, FraudDetectionMixin):
    """Credit card gateway with fraud detection and interchange fee logic."""

    def __init__(self, merchant_id: str, api_key: str, cvv_required: bool = True):
        super().__init__(merchant_id, api_key, processing_fee_pct=0.022)
        self.cvv_required = cvv_required

    def process_payment(self, txn_id: str, amount: float, country: str = "US") -> tuple[bool, float, str]:
        # Fraud check inherited from FraudDetectionMixin
        if self.scan_for_fraud(amount, country):
            self.log_transaction(txn_id, "FRAUD_HELD", amount)
            return False, 0.0, "Transaction held: Exceeds automated fraud threshold."

        fee = self.compute_fee(amount)
        net_payout = amount - fee
        self.log_transaction(txn_id, "SETTLED", amount)
        return True, net_payout, "Credit card authorized and batch settled."


class CryptoPaymentProcessor(PaymentGateway, AuditLoggerMixin):
    """Cryptocurrency processor with network gas fee calculation."""

    def __init__(self, merchant_id: str, api_key: str, blockchain: str = "Ethereum"):
        super().__init__(merchant_id, api_key, processing_fee_pct=0.01) # Lower fee
        self.blockchain = blockchain
        self.gas_fee_usd = 4.50

    def compute_fee(self, amount: float) -> float:
        """Overrides base fee with on-chain gas fee calculation."""
        return (amount * self.processing_fee_pct) + self.gas_fee_usd

    def process_payment(self, txn_id: str, amount: float, country: str = "US") -> tuple[bool, float, str]:
        fee = self.compute_fee(amount)
        net_payout = amount - fee
        self.log_transaction(txn_id, "MINED", amount)
        return True, net_payout, f"Confirmed on-chain on {self.blockchain} network."


# Polymorphic Settlement Engine
def execute_merchant_batch(transactions: list[dict], processors: dict[str, PaymentGateway]) -> None:
    print("=" * 80)
    print(f"{'MERCHANT MULTI-CHANNEL SETTLEMENT RUN':^80}")
    print("=" * 80)

    total_gross = 0.0
    total_net = 0.0

    for txn in transactions:
        method = txn["method"]
        processor = processors.get(method)
        if not processor:
            print(f"❌ Unsupported payment method: {method}")
            continue

        # Polymorphic invocation: every processor responds to process_payment()
        success, net_amt, message = processor.process_payment(
            txn["id"], txn["amount"], txn.get("country", "US")
        )

        if success:
            total_gross += txn["amount"]
            total_net += net_amt
            print(f"  ✓ Txn {txn['id']:<10} | Method: {method:<10} | Gross: ${txn['amount']:>8.2f} | Net Payout: ${net_amt:>8.2f}")
        else:
            print(f"  ✗ Txn {txn['id']:<10} | Method: {method:<10} | FAILED: {message}")

    print("-" * 80)
    print(f"{'BATCH SETTLEMENT TOTALS:':<35} Gross: ${total_gross:,.2f} | Net Disbursed: ${total_net:,.2f}")
    print("=" * 80)


# System Execution Run
gateway_directory = {
    "CREDIT_CARD": CreditCardProcessor("MERCH-100", "sk_live_card_902"),
    "CRYPTO": CryptoPaymentProcessor("MERCH-100", "sk_live_eth_441", blockchain="Ethereum")
}

batch_queue = [
    {"id": "TXN-801", "method": "CREDIT_CARD", "amount": 149.99, "country": "US"},
    {"id": "TXN-802", "method": "CRYPTO", "amount": 500.00, "country": "DE"},
    {"id": "TXN-803", "method": "CREDIT_CARD", "amount": 18_500.00, "country": "US"}, # High fraud amount
]

execute_merchant_batch(batch_queue, gateway_directory)
```

### 🔍 Code Explanation:
- **`super().__init__()` Delegation**: `CreditCardProcessor` and `CryptoPaymentProcessor` call `super().__init__()` to configure merchant attributes and customized fee percentages.
- **Mixins**: `AuditLoggerMixin` and `FraudDetectionMixin` provide reusable features to `CreditCardProcessor` without code duplication.
- **Polymorphism**: `execute_merchant_batch()` accepts any `PaymentGateway` subclass and invokes `.process_payment()` uniformly.
- **Method Overriding**: `CryptoPaymentProcessor.compute_fee` replaces the flat credit card surcharge with on-chain blockchain gas fees.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master class hierarchies, constructor chaining with `super()`, polymorphic dispatch, mixins, and diamond MRO linearization:

---

### 🟢 Tier 1: Single Inheritance & Method Overriding (Exercises 1–3)

#### 🔹 Exercise 1: Vehicle & Electric Car Extension
* **Goal**: Create `class Vehicle(make: str, model: str, base_price: float)`. Subclass `ElectricVehicle` that adds `battery_kwh: float` in `__init__` via `super()` and overrides `get_specs()` to include battery capacity.

#### 🔹 Exercise 2: Employee Compensation Specialization
* **Goal**: Base class `Employee` with `calculate_bonus() -> float` returning `0.05 * salary`.
* **Subclasses**: `SalesManager` (returns `0.15 * salary + commission`) and `Executive` (returns `0.30 * salary + equity_value`).

#### 🔹 Exercise 3: Geometric Shape Polymorphic Renderer
* **Goal**: Base class `Shape` with `area()` and `perimeter()`.
* **Subclasses**: `Circle(radius)` and `Rectangle(width, height)`. Write a polymorphic function `print_shape_metrics(shapes: list[Shape])`.

---

### 🟡 Tier 2: Mixin Architecture & Orthogonal Capabilities (Exercises 4–6)

#### 🔹 Exercise 4: JSON Serializable Mixin
* **Goal**: Define `class JSONSerializableMixin` with method `to_json() -> str` that returns `json.dumps(self.__dict__)`.
* **Requirement**: Inherit this mixin into a `UserAccount` class and verify serialized string.

#### 🔹 Exercise 5: Timestamp Audit Log Mixin
* **Goal**: Define `class AuditMixin` with `log_mutation(action: str)`.
* **Requirement**: Apply to `DatabaseRecord` and demonstrate audit outputs when saving and deleting.

#### 🔹 Exercise 6: Role Permission Guard Mixin
* **Goal**: Define `class PermissionGuardMixin` with `require_permission(perm: str)`. If user lacks permission in `self.permissions`, raise `PermissionError`.

---

### 🟠 Tier 3: Multiple Inheritance & Diamond MRO (Exercises 7–9)

#### 🔹 Exercise 7: Diamond Problem MRO Inspector
* **Goal**: Create diamond hierarchy: `A` $\rightarrow$ `B(A)`, `C(A)` $\rightarrow$ `D(B, C)`.
* **Requirement**: In each class `ping()`, call `super().ping()`. Trace the exact print order and verify with `D.mro()`.

#### 🔹 Exercise 8: Cooperative `super().__init__(**kwargs)` Initializer
* **Goal**: Implement multi-base initialization where each class strips its known keyword arguments and forwards `**kwargs` up the cooperative MRO chain to `object`.

#### 🔹 Exercise 9: Polymorphic Plugin Dispatch Engine
* **Goal**: Create `BasePlugin` and subclasses `AuthPlugin`, `CompressionPlugin`, `RateLimitPlugin`.
* **Requirement**: Write an orchestrator pipeline that runs `.execute(payload)` across all registered plugins in priority order.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Multi-Cloud Infrastructure Resource Provisioner
* **Goal**: Model diverse cloud assets (`VirtualMachine`, `StorageBucket`) using inheritance and mixins, enforce audit trails, and calculate polymorphic infrastructure invoices.

---

## 📝 Quick Exercise: Multi-Cloud Infrastructure Resource Provisioner

### 🏢 Real-Life Scenario
You are developing a unified Multi-Cloud infrastructure orchestrator (such as Terraform or Pulumi) that provisions computing assets across Amazon Web Services (AWS), Google Cloud (GCP), and Azure. The orchestrator must model diverse cloud assets (`VirtualMachine`, `StorageBucket`, `DatabaseCluster`) using inheritance, enforce audit logging via a Mixin, calculate monthly running costs polymorphically, and support resource scaling.

### 📋 Requirements
1. **Define `AuditTelemetryMixin`**:
   - Method: `log_event(self, action: str) -> None`: Prints `f"[CLOUD AUDIT] {self.__class__.__name__} ({self.resource_id}): {action}"`.
2. **Define Base Class `CloudResource`**:
   - Attributes: `resource_id: str`, `name: str`, `region: str`, `is_running: bool = False`.
   - Methods:
     - `start(self) -> None`: Sets `is_running = True`.
     - `stop(self) -> None`: Sets `is_running = False`.
     - `calculate_monthly_cost(self) -> float`: Returns `0.0`.
3. **Define Subclass `VirtualMachine(CloudResource, AuditTelemetryMixin)`**:
   - Constructor: Accepts `resource_id`, `name`, `region`, `cpu_cores: int`, `hourly_rate: float`.
   - Overrides:
     - `start()`: Calls `super().start()`, and invokes `self.log_event("Started VM instance and initialized hypervisor")`.
     - `calculate_monthly_cost()`: Returns `730.0 * self.hourly_rate if self.is_running else 5.00` (storage reserve when stopped).
4. **Define Subclass `StorageBucket(CloudResource, AuditTelemetryMixin)`**:
   - Constructor: Accepts `resource_id`, `name`, `region`, `stored_gigabytes: float`, `cost_per_gb: float = 0.023`.
   - Overrides:
     - `calculate_monthly_cost()`: Returns `self.stored_gigabytes * self.cost_per_gb`.
5. Store resources in a list, start all resources, and print a consolidated cloud infrastructure invoice.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 inheritance, polymorphism, `super()`, and mixins with Level 1 foundational types, loops, lists, and f-string formatting.

### 🎯 Expected Output
```text
[CLOUD AUDIT] VirtualMachine (vm-aws-prod-01): Started VM instance and initialized hypervisor
[CLOUD AUDIT] VirtualMachine (vm-gcp-ml-02): Started VM instance and initialized hypervisor
======================================================================
               MULTI-CLOUD INFRASTRUCTURE INVOICE                     
======================================================================
Resource ID          | Type            | Region       | Monthly Cost  
----------------------------------------------------------------------
vm-aws-prod-01       | VirtualMachine  | us-east-1    |        $146.00
vm-gcp-ml-02         | VirtualMachine  | europe-west1 |        $365.00
s3-archive-01        | StorageBucket   | us-west-2    |        $115.00
----------------------------------------------------------------------
TOTAL PROJECTED MONTHLY CLOUD SPEND:                           $626.00
======================================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Multi-Cloud & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Multi-Cloud Infrastructure Engine
# =====================================================================
class AuditTelemetryMixin:
    def log_event(self, action: str) -> None:
        print(f"[CLOUD AUDIT] {self.__class__.__name__} ({self.resource_id}): {action}")


class CloudResource:
    def __init__(self, resource_id: str, name: str, region: str):
        self.resource_id = resource_id
        self.name = name
        self.region = region
        self.is_running = False

    def start(self) -> None:
        self.is_running = True

    def stop(self) -> None:
        self.is_running = False

    def calculate_monthly_cost(self) -> float:
        return 0.0


class VirtualMachine(CloudResource, AuditTelemetryMixin):
    def __init__(self, resource_id: str, name: str, region: str, cpu_cores: int, hourly_rate: float):
        super().__init__(resource_id, name, region)
        self.cpu_cores = cpu_cores
        self.hourly_rate = hourly_rate

    def start(self) -> None:
        super().start()
        self.log_event("Started VM instance and initialized hypervisor")

    def calculate_monthly_cost(self) -> float:
        return (730.0 * self.hourly_rate) if self.is_running else 5.00


class StorageBucket(CloudResource, AuditTelemetryMixin):
    def __init__(self, resource_id: str, name: str, region: str, stored_gigabytes: float, cost_per_gb: float = 0.023):
        super().__init__(resource_id, name, region)
        self.stored_gigabytes = stored_gigabytes
        self.cost_per_gb = cost_per_gb

    def calculate_monthly_cost(self) -> float:
        return self.stored_gigabytes * self.cost_per_gb


infrastructure: list[CloudResource] = [
    VirtualMachine("vm-aws-prod-01", "Web API Node", "us-east-1", cpu_cores=4, hourly_rate=0.20),
    VirtualMachine("vm-gcp-ml-02", "AI Model Server", "europe-west1", cpu_cores=16, hourly_rate=0.50),
    StorageBucket("s3-archive-01", "Customer Data Lake", "us-west-2", stored_gigabytes=5000.0),
]

for res in infrastructure:
    if isinstance(res, VirtualMachine):
        res.start()

print("=" * 70)
print(f"{'MULTI-CLOUD INFRASTRUCTURE INVOICE':^70}")
print("=" * 70)
print(f"{'Resource ID':<20} | {'Type':<15} | {'Region':<12} | {'Monthly Cost':>14}")
print("-" * 70)

total_spend = 0.0
for res in infrastructure:
    cost = res.calculate_monthly_cost()
    total_spend += cost
    print(f"{res.resource_id:<20} | {res.__class__.__name__:<15} | {res.region:<12} | {f'${cost:,.2f}':>14}")

print("-" * 70)
print(f"{'TOTAL PROJECTED MONTHLY CLOUD SPEND:':<50} {f'${total_spend:,.2f}':>17}")
print("=" * 70)

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
class Vehicle:
    def __init__(self, make: str, model: str, price: float):
        self.make, self.model, self.price = make, model, price
    def get_specs(self): return f"{self.make} {self.model} (${self.price:,.2f})"

class ElectricVehicle(Vehicle):
    def __init__(self, make: str, model: str, price: float, battery_kwh: float):
        super().__init__(make, model, price)
        self.battery_kwh = battery_kwh
    def get_specs(self): return f"{super().get_specs()} [{self.battery_kwh} kWh Battery]"

# Ex 2:
class Employee:
    def __init__(self, name: str, salary: float): self.name, self.salary = name, salary
    def calculate_bonus(self): return self.salary * 0.05

class SalesManager(Employee):
    def __init__(self, name: str, salary: float, commission: float):
        super().__init__(name, salary); self.commission = commission
    def calculate_bonus(self): return (self.salary * 0.15) + self.commission

# Ex 3:
import math
class Shape:
    def area(self): return 0.0
class Circle(Shape):
    def __init__(self, r: float): self.r = r
    def area(self): return math.pi * (self.r ** 2)

# Ex 4:
import json
class JSONSerializableMixin:
    def to_json(self): return json.dumps(self.__dict__)

# Ex 5:
import datetime
class AuditMixin:
    def log_mutation(self, act: str):
        print(f"[{datetime.datetime.now().isoformat()}] {self.__class__.__name__}: {act}")

# Ex 6:
class PermissionGuardMixin:
    def require_permission(self, perm: str):
        if perm not in getattr(self, "permissions", set()):
            raise PermissionError(f"Missing required permission: {perm}")

# Ex 7:
class A:
    def ping(self): print("A", end=" ")
class B(A):
    def ping(self): print("B", end=" "); super().ping()
class C(A):
    def ping(self): print("C", end=" "); super().ping()
class D(B, C):
    def ping(self): print("D", end=" "); super().ping()

# Ex 8:
class BaseComp:
    def __init__(self, **kw): super().__init__()
class Alpha(BaseComp):
    def __init__(self, a=1, **kw): self.a = a; super().__init__(**kw)
class Beta(BaseComp):
    def __init__(self, b=2, **kw): self.b = b; super().__init__(**kw)
class Combined(Alpha, Beta): pass

# Ex 9:
class BasePlugin:
    def run(self, payload: dict) -> dict: return payload
class CompressionPlugin(BasePlugin):
    def run(self, payload: dict):
        payload["compressed"] = True; return payload
```
</details>

