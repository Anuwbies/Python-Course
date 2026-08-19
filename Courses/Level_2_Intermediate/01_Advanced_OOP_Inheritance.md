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

## 3. Multiple Inheritance, Mixins & Method Resolution Order (MRO)

Python supports inheriting from multiple base classes simultaneously. To prevent ambiguity (the "Diamond Problem"), Python resolves method calls using the **C3 Linearization algorithm (MRO)**.

### Mixin Classes
A **Mixin** is a lightweight, focused class designed to inject specific reusable functionality into other classes without defining standalone business entities.

```python
class TimestampAuditMixin:
    """Injects timestamp auditing capabilities."""
    def log_action(self, action: str) -> None:
        print(f"[AUDIT LOG] {self.__class__.__name__} ({getattr(self, 'emp_id', 'N/A')}): {action}")

class EncryptionMixin:
    """Injects payload hashing simulation."""
    def hash_identifier(self) -> str:
        return f"HASH-SHA256:{hash(getattr(self, 'emp_id', ''))}"

# Multiple Inheritance: Inherits from Manager + two orthogonal Mixins
class SecurityLead(Manager, TimestampAuditMixin, EncryptionMixin):
    def authorize_security_override(self) -> None:
        self.log_action("Authorized tier-3 emergency infrastructure bypass")

# Inspecting the C3 Method Resolution Order
print([cls.__name__ for cls in SecurityLead.mro()])
# Output: ['SecurityLead', 'Manager', 'Employee', 'TimestampAuditMixin', 'EncryptionMixin', 'object']
```

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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Audit Telemetry Mixin (Level 2)
class AuditTelemetryMixin:
    def log_event(self, action: str) -> None:
        print(f"[CLOUD AUDIT] {self.__class__.__name__} ({self.resource_id}): {action}")


# 2. Base Cloud Resource Class (Level 2)
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


# 3. Virtual Machine Subclass (Level 2)
class VirtualMachine(CloudResource, AuditTelemetryMixin):
    def __init__(self, resource_id: str, name: str, region: str, cpu_cores: int, hourly_rate: float):
        super().__init__(resource_id, name, region)
        self.cpu_cores = cpu_cores
        self.hourly_rate = hourly_rate

    def start(self) -> None:
        super().start()
        self.log_event("Started VM instance and initialized hypervisor")

    def calculate_monthly_cost(self) -> float:
        # 730 continuous operational hours in an average month
        return (730.0 * self.hourly_rate) if self.is_running else 5.00


# 4. Storage Bucket Subclass (Level 2)
class StorageBucket(CloudResource, AuditTelemetryMixin):
    def __init__(self, resource_id: str, name: str, region: str, stored_gigabytes: float, cost_per_gb: float = 0.023):
        super().__init__(resource_id, name, region)
        self.stored_gigabytes = stored_gigabytes
        self.cost_per_gb = cost_per_gb

    def calculate_monthly_cost(self) -> float:
        return self.stored_gigabytes * self.cost_per_gb


# 5. Infrastructure Deployment and Execution
infrastructure: list[CloudResource] = [
    VirtualMachine("vm-aws-prod-01", "Web API Node", "us-east-1", cpu_cores=4, hourly_rate=0.20),
    VirtualMachine("vm-gcp-ml-02", "AI Model Server", "europe-west1", cpu_cores=16, hourly_rate=0.50),
    StorageBucket("s3-archive-01", "Customer Data Lake", "us-west-2", stored_gigabytes=5000.0),
]

# Start VM assets
for res in infrastructure:
    if isinstance(res, VirtualMachine):
        res.start()

# Print Formatted Multi-Cloud Invoice (Level 1 f-strings)
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
```

**Explanation of the Solution:**
- `CloudResource` defines common properties and the polymorphic contract `.calculate_monthly_cost()`.
- `VirtualMachine` delegates to `super().start()` while using `AuditTelemetryMixin` to log operations.
- The invoice consumer loops over polymorphic objects and sums costs cleanly.
</details>
