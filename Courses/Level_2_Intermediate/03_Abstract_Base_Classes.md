# Lesson 3: Abstract Base Classes (ABCs) & Interface Contracts

In large-scale enterprise software architectures, development teams rely on strict architectural contracts to ensure that modular components and plugins implement required methods before the application boots. In this lesson, you will master Python's `abc` module, Abstract Base Classes, abstract methods/properties, and interface design patterns.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand why interface contracts are critical in enterprise software architecture.
2. Define Abstract Base Classes using `abc.ABC` and the `@abstractmethod` decorator.
3. Combine abstract properties using `@property` and `@abstractmethod`.
4. Enforce compile-time/instantiation-time contract compliance (preventing incomplete subclasses from instantiating).
5. Compare **Nominal Subtyping (ABCs)** with **Structural Subtyping (`typing.Protocol`)**.

---

## 1. The Need for Interface Contracts

Without ABCs, Python only detects missing subclass methods at runtime when that specific method is finally called:

```python
# ❌ Flawed base class without ABC enforcement:
class BadBaseStorage:
    def save(self, data: dict):
        raise NotImplementedError("Subclass must implement save()")

class S3Storage(BadBaseStorage):
    pass # Forgot to implement save()

# Python allows creating the instance without warning:
storage = S3Storage() 
# ... hours later in production:
# storage.save({"key": "val"}) # 💥 CRASHES at runtime!
```

---

## 2. Defining ABCs with the `abc` Module

By inheriting from `abc.ABC` and marking required interface methods with `@abstractmethod`, Python prevents any incomplete child class from ever being instantiated:

```python
from abc import ABC, abstractmethod

class BaseCacheEngine(ABC):
    """Abstract Interface for caching layers (Redis, Memcached, In-Memory)."""

    @abstractmethod
    def get(self, key: str) -> str | None:
        """Retrieve key value from cache store."""
        pass

    @abstractmethod
    def set(self, key: str, value: str, ttl_seconds: int = 3600) -> bool:
        """Store key-value pair with expiration time."""
        pass

    @property
    @abstractmethod
    def engine_name(self) -> str:
        """Abstract property: must be implemented by subclass."""
        pass

# Attempting to instantiate an incomplete subclass:
class IncompleteCache(BaseCacheEngine):
    def get(self, key: str):
        return None
    # Missing .set() and .engine_name

# cache = IncompleteCache()
# ❌ TypeError: Can't instantiate abstract class IncompleteCache with abstract methods engine_name, set
```

---

## 3. Concrete Implementations of ABCs

When all abstract methods and properties are implemented, instantiation succeeds normally:

```python
class MemoryCache(BaseCacheEngine):
    def __init__(self):
        self._store: dict[str, str] = {}

    @property
    def engine_name(self) -> str:
        return "InMemory-RAM-Cache-v1"

    def get(self, key: str) -> str | None:
        return self._store.get(key)

    def set(self, key: str, value: str, ttl_seconds: int = 3600) -> bool:
        self._store[key] = value
        return True

# ✅ Fully compliant subclass instantiates without error:
cache = MemoryCache()
cache.set("session_101", "user_authenticated")
print(cache.get("session_101")) # "user_authenticated"
```

---

## 4. Nominal ABCs vs. Structural Protocols (`typing.Protocol`)

- **ABCs (Nominal Subtyping)**: Classes must explicitly declare inheritance from `ABC` (`class S3Adapter(BaseAdapter):`).
- **Protocols (Structural / Duck Typing)**: Any class that implements the matching method signatures automatically satisfies the protocol without inheriting from a common base.

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Multi-Target Notification & Dispatcher Engine**, demonstrating Abstract Base Classes, abstract properties, polymorphism, and plugin orchestration:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Multi-Channel Alert & Notification Dispatcher
# =====================================================================

from abc import ABC, abstractmethod
from datetime import datetime

class BaseNotificationService(ABC):
    """Abstract contractual interface for all communication channels."""

    def __init__(self, service_id: str):
        self.service_id = service_id
        self.total_dispatched = 0

    @property
    @abstractmethod
    def channel_type(self) -> str:
        """Returns channel medium (e.g. 'EMAIL', 'SMS', 'SLACK')."""
        pass

    @property
    @abstractmethod
    def cost_per_message_usd(self) -> float:
        """Unit operational dispatch cost."""
        pass

    @abstractmethod
    def send(self, recipient: str, message: str, priority: str = "NORMAL") -> bool:
        """Executes actual network dispatch."""
        pass

    def compute_total_cost(self) -> float:
        """Concrete template method shared by all implementations."""
        return self.total_dispatched * self.cost_per_message_usd


class EmailNotificationService(BaseNotificationService):
    """Production SMTP / SES email dispatch integration."""

    def __init__(self, service_id: str, smtp_host: str = "smtp.enterprise.com"):
        super().__init__(service_id)
        self.smtp_host = smtp_host

    @property
    def channel_type(self) -> str:
        return "EMAIL (SMTP)"

    @property
    def cost_per_message_usd(self) -> float:
        return 0.0001 # Fraction of a cent

    def send(self, recipient: str, message: str, priority: str = "NORMAL") -> bool:
        # Validate email address format (Lesson 4)
        if "@" not in recipient:
            print(f"❌ [EMAIL FAILURE] Invalid recipient address: {recipient}")
            return False
        
        self.total_dispatched += 1
        print(f"📧 [EMAIL DISPATCHED] -> {recipient:<25} | Priority: {priority:<6} | Body: {message}")
        return True


class SlackWebhookNotificationService(BaseNotificationService):
    """Slack channel webhook integration."""

    def __init__(self, service_id: str, webhook_url: str):
        super().__init__(service_id)
        self.webhook_url = webhook_url

    @property
    def channel_type(self) -> str:
        return "SLACK (WEBHOOK)"

    @property
    def cost_per_message_usd(self) -> float:
        return 0.0000 # Free webhook tier

    def send(self, recipient: str, message: str, priority: str = "NORMAL") -> bool:
        if not recipient.startswith("#") and not recipient.startswith("@"):
            print(f"❌ [SLACK FAILURE] Invalid Slack target channel: {recipient}")
            return False
        
        self.total_dispatched += 1
        print(f"💬 [SLACK POSTED]     -> {recipient:<25} | Priority: {priority:<6} | Body: {message}")
        return True


class SMSNotificationService(BaseNotificationService):
    """Twilio / Telecom SMS carrier dispatch integration."""

    def __init__(self, service_id: str, carrier_account_sid: str):
        super().__init__(service_id)
        self.carrier_account_sid = carrier_account_sid

    @property
    def channel_type(self) -> str:
        return "TELECOM (SMS)"

    @property
    def cost_per_message_usd(self) -> float:
        return 0.0150 # $0.015 per SMS segment

    def send(self, recipient: str, message: str, priority: str = "NORMAL") -> bool:
        # Validate phone number digits
        clean_number = recipient.replace("+", "").replace("-", "").strip()
        if not clean_number.isdigit() or len(clean_number) < 10:
            print(f"❌ [SMS FAILURE] Invalid phone number: {recipient}")
            return False
        
        self.total_dispatched += 1
        print(f"📱 [SMS DISPATCHED]   -> {recipient:<25} | Priority: {priority:<6} | Body: {message}")
        return True


# Dispatch Orchestration Manager
class IncidentBroadcastEngine:
    def __init__(self):
        self._services: list[BaseNotificationService] = []

    def register_channel(self, service: BaseNotificationService) -> None:
        if not isinstance(service, BaseNotificationService):
            raise TypeError("Service must conform to BaseNotificationService ABC interface.")
        self._services.append(service)

    def broadcast_critical_incident(self, recipients: dict[str, str], alert_text: str) -> None:
        print("=" * 75)
        print(f"{'🚨 EMERGENCY INFRASTRUCTURE INCIDENT BROADCAST':^75}")
        print("=" * 75)
        
        for service in self._services:
            target = recipients.get(service.channel_type)
            if target:
                service.send(target, alert_text, priority="URGENT")

        print("-" * 75)
        print("BROADCAST COST AUDIT:")
        total_broadcast_cost = sum(s.compute_total_cost() for s in self._services)
        for s in self._services:
            print(f"  - {s.channel_type:<20}: {s.total_dispatched} msgs @ ${s.cost_per_message_usd:.4f}/ea -> ${s.compute_total_cost():.4f}")
        print(f"{'TOTAL OUTBOUND DISPATCH COST:':<45} ${total_broadcast_cost:,.4f}")
        print("=" * 75)


# Execution Run
engine = IncidentBroadcastEngine()
engine.register_channel(EmailNotificationService("SES-01"))
engine.register_channel(SlackWebhookNotificationService("SLACK-01", "https://hooks.slack.com/services/XYZ"))
engine.register_channel(SMSNotificationService("TWILIO-01", "AC998182"))

contacts = {
    "EMAIL (SMTP)": "security-lead@enterprise.com",
    "SLACK (WEBHOOK)": "#devops-oncall-alerts",
    "TELECOM (SMS)": "+1-555-019-2834"
}

engine.broadcast_critical_incident(contacts, "CRITICAL: Database primary replica failover triggered.")
```

### 🔍 Code Explanation:
- **`BaseNotificationService(ABC)`**: Defines an uncompromising contract requiring all subclasses to implement `channel_type`, `cost_per_message_usd`, and `send()`.
- **Abstract Properties**: `@property` stacked on `@abstractmethod` ensures derived classes expose typed attributes rather than plain functions.
- **Contract Enforcement**: If a new communication channel (e.g. `TeamsNotificationService`) fails to implement `send()`, Python refuses instantiation at program startup.

---

## 📝 Quick Exercise: Multi-Database Storage Engine Adapter Interface

### 🏢 Real-Life Scenario
You are developing an enterprise Persistence Data Layer (such as an ORM abstraction) that connects to diverse storage technologies: Relational SQL (`PostgresStorageAdapter`) and In-Memory Key-Value Stores (`RedisStorageAdapter`). You must define an Abstract Base Class `BaseStorageAdapter` that guarantees any storage plugin implements connection management, record retrieval, saving, and deletion.

### 📋 Requirements
1. **Define Abstract Base Class `BaseStorageAdapter(ABC)`**:
   - Constructor: `__init__(self, connection_string: str)`
   - Abstract Property:
     - `@property @abstractmethod def engine_type(self) -> str`
   - Abstract Methods:
     - `@abstractmethod def connect(self) -> bool`
     - `@abstractmethod def save_record(self, record_id: str, data: dict) -> bool`
     - `@abstractmethod def fetch_record(self, record_id: str) -> dict | None`
     - `@abstractmethod def delete_record(self, record_id: str) -> bool`
2. **Define Subclass `PostgresStorageAdapter(BaseStorageAdapter)`**:
   - Implements `engine_type` $\rightarrow$ `"PostgreSQL Relational DB"`
   - Uses an internal dictionary `self._table: dict[str, dict] = {}` to simulate table storage.
   - `save_record`: Stores record into `_table` and returns `True`.
   - `fetch_record`: Returns data dict or `None`.
   - `delete_record`: Removes record if present.
3. **Define Subclass `RedisStorageAdapter(BaseStorageAdapter)`**:
   - Implements `engine_type` $\rightarrow$ `"Redis In-Memory Key-Value"`
   - Implements all abstract methods using an internal `self._cache: dict[str, dict] = {}`.
4. Register both adapters, save a sample user record `{"username": "erostova", "role": "admin"}`, fetch it back, and verify contract compliance.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 ABCs, abstract methods, and properties with Level 1 dictionaries, functions, and string formatting.

### 🎯 Expected Output
```text
==================================================
        STORAGE ADAPTER CONTRACT COMPLIANCE       
==================================================
[POSTGRES] Connected to postgresql://user:pass@localhost:5432/appdb
[REDIS]    Connected to redis://localhost:6379/0
--------------------------------------------------
ADAPTER OPERATIONS TEST:
  ✓ [PostgreSQL Relational DB]: Saved record 'USR-101'
  ✓ [PostgreSQL Relational DB]: Fetched record: {'username': 'erostova', 'role': 'admin'}
  ✓ [Redis In-Memory Key-Value]: Saved record 'SESSION-909'
  ✓ [Redis In-Memory Key-Value]: Fetched record: {'token': 'jwt_secret_xyz'}
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from abc import ABC, abstractmethod

# 1. Abstract Base Class Interface (Level 2)
class BaseStorageAdapter(ABC):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.is_connected = False

    @property
    @abstractmethod
    def engine_type(self) -> str:
        pass

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def save_record(self, record_id: str, data: dict) -> bool:
        pass

    @abstractmethod
    def fetch_record(self, record_id: str) -> dict | None:
        pass

    @abstractmethod
    def delete_record(self, record_id: str) -> bool:
        pass


# 2. PostgreSQL Concrete Adapter (Level 2)
class PostgresStorageAdapter(BaseStorageAdapter):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self._table: dict[str, dict] = {}

    @property
    def engine_type(self) -> str:
        return "PostgreSQL Relational DB"

    def connect(self) -> bool:
        self.is_connected = True
        print(f"[POSTGRES] Connected to {self.connection_string}")
        return True

    def save_record(self, record_id: str, data: dict) -> bool:
        self._table[record_id] = data.copy()
        return True

    def fetch_record(self, record_id: str) -> dict | None:
        return self._table.get(record_id)

    def delete_record(self, record_id: str) -> bool:
        if record_id in self._table:
            del self._table[record_id]
            return True
        return False


# 3. Redis Concrete Adapter (Level 2)
class RedisStorageAdapter(BaseStorageAdapter):
    def __init__(self, connection_string: str):
        super().__init__(connection_string)
        self._cache: dict[str, dict] = {}

    @property
    def engine_type(self) -> str:
        return "Redis In-Memory Key-Value"

    def connect(self) -> bool:
        self.is_connected = True
        print(f"[REDIS]    Connected to {self.connection_string}")
        return True

    def save_record(self, record_id: str, data: dict) -> bool:
        self._cache[record_id] = data.copy()
        return True

    def fetch_record(self, record_id: str) -> dict | None:
        return self._cache.get(record_id)

    def delete_record(self, record_id: str) -> bool:
        return self._cache.pop(record_id, None) is not None


# 4. Verification and Execution
pg_adapter = PostgresStorageAdapter("postgresql://user:pass@localhost:5432/appdb")
redis_adapter = RedisStorageAdapter("redis://localhost:6379/0")

print("==================================================")
print("        STORAGE ADAPTER CONTRACT COMPLIANCE       ")
print("==================================================")
pg_adapter.connect()
redis_adapter.connect()
print("--------------------------------------------------")
print("ADAPTER OPERATIONS TEST:")

# Test Postgres
pg_adapter.save_record("USR-101", {"username": "erostova", "role": "admin"})
pg_rec = pg_adapter.fetch_record("USR-101")
print(f"  ✓ [{pg_adapter.engine_type}]: Saved record 'USR-101'")
print(f"  ✓ [{pg_adapter.engine_type}]: Fetched record: {pg_rec}")

# Test Redis
redis_adapter.save_record("SESSION-909", {"token": "jwt_secret_xyz"})
rd_rec = redis_adapter.fetch_record("SESSION-909")
print(f"  ✓ [{redis_adapter.engine_type}]: Saved record 'SESSION-909'")
print(f"  ✓ [{redis_adapter.engine_type}]: Fetched record: {rd_rec}")
print("==================================================")
```

**Explanation of the Solution:**
- `BaseStorageAdapter` defines the abstract interface that all persistence plugins must follow.
- Subclasses implement the full lifecycle (`connect`, `save_record`, `fetch_record`, `delete_record`) and abstract property `engine_type`.
</details>
