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

---

## 4. Under the Hood: `ABCMeta` & `__abstractmethods__`

When you inherit from `ABC` (which uses metaclass `abc.ABCMeta`), Python inspects the class definition at load time and populates a special frozenset: `__abstractmethods__`.

```
class Base(ABC):
  @abstractmethod def run(self): pass ──► Base.__abstractmethods__ = {'run'}

class Child(Base):
  pass ──► Child.__abstractmethods__ = {'run'} ──► Instantiation BLOCKED with TypeError!

class CompletedChild(Base):
  def run(self): pass ──► CompletedChild.__abstractmethods__ = set() ──► Instantiation ALLOWED!
```

### ⚡ Virtual Subclasses via `.register()`
You can register external classes as "virtual subclasses" of an ABC without changing their inheritance tree:

```python
from abc import ABC, abstractmethod

class BaseReader(ABC):
    @abstractmethod
    def read_payload(self) -> bytes: pass

class ThirdPartyBlobStream:
    def read_payload(self) -> bytes:
        return b"blob_data"

# Register ThirdPartyBlobStream as a virtual subclass of BaseReader:
BaseReader.register(ThirdPartyBlobStream)

stream = ThirdPartyBlobStream()
print(isinstance(stream, BaseReader)) # True!
print(issubclass(ThirdPartyBlobStream, BaseReader)) # True!
```

---

## 5. Structural Typing with `@runtime_checkable` Protocols

While ABCs use **Nominal Typing** (explicit inheritance), `typing.Protocol` enables **Structural Typing (Duck Typing)** verified at runtime:

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closable(Protocol):
    def close(self) -> None:
        """Any class with a close() method matches this protocol!"""
        ...

class NetworkSocket:
    def close(self) -> None:
        print("Socket closed.")

class DatabasePool:
    def close(self) -> None:
        print("Pool closed.")

# Neither class inherits from Closable, but both satisfy the structural protocol:
sock = NetworkSocket()
print(isinstance(sock, Closable)) # True!
```

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

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master Abstract Base Classes, abstract methods, abstract properties, ABCMeta, virtual subclasses, and Protocols:

---

### 🟢 Tier 1: ABC Contracts & Instantiation Guards (Exercises 1–3)

#### 🔹 Exercise 1: Base Shape ABC & Contract Enforcement
* **Goal**: Define `class BaseShape(ABC)` with `@abstractmethod def area(self) -> float`.
* **Requirement**: Show that instantiating `BaseShape()` raises `TypeError`. Implement `Square(side)` to satisfy contract.

#### 🔹 Exercise 2: Abstract Property Requirement
* **Goal**: Define `class CloudClient(ABC)` with `@property @abstractmethod def provider_name(self) -> str`.
* **Requirement**: Subclass `AWSClient` and verify `provider_name` works as a property.

#### 🔹 Exercise 3: File Parser Interface
* **Goal**: Define `class BaseFileParser(ABC)` with `@abstractmethod def parse(self, raw_data: str) -> list[dict]`.
* **Requirement**: Implement `CSVFileParser` and test parsing a comma-separated string.

---

### 🟡 Tier 2: Template Method Pattern & Multi-Method Contracts (Exercises 4–6)

#### 🔹 Exercise 4: Data Pipeline Template Method
* **Goal**: In `BaseETL(ABC)`, implement concrete method `run_pipeline()` that calls abstract methods `extract()`, `transform(data)`, and `load(data)` in order.

#### 🔹 Exercise 5: Cache Engine Lifecycle Contract
* **Goal**: Define `class CacheEngine(ABC)` with `get(k)`, `set(k, v, ttl)`, and `clear()`. Implement `InMemoryCache`.

#### 🔹 Exercise 6: Payment Gateway Refund Interface
* **Goal**: Define `class BasePaymentGateway(ABC)` with `charge(amt)` and `refund(txn_id, amt)`. Subclass `StripeGateway`.

---

### 🟠 Tier 3: Virtual Subclasses & Protocols (Exercises 7–9)

#### 🔹 Exercise 7: Virtual Subclass Registration (`.register()`)
* **Goal**: Define `class Streamable(ABC)` with abstract `stream_bytes()`.
* **Requirement**: Take a third-party class `ExternalAudioStream` and register it with `Streamable.register(ExternalAudioStream)`. Verify `isinstance()` returns `True`.

#### 🔹 Exercise 8: Structural Duck Typing with `@runtime_checkable` Protocol
* **Goal**: Define `@runtime_checkable class Serializable(Protocol)` with `serialize() -> bytes`.
* **Requirement**: Create two unrelated classes that implement `serialize()`, and verify `isinstance(obj, Serializable)` evaluates to `True`.

#### 🔹 Exercise 9: Pluggable Serialization Dispatcher
* **Goal**: Build a registry system accepting any `BaseSerializer(ABC)` (e.g. `JSONSerializer`, `XMLSerializer`) and dynamically selecting the correct serializer based on MIME type.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Multi-Database Storage Engine Adapter Interface
* **Goal**: Build an abstract persistence layer (`BaseStorageAdapter`) with relational SQL and in-memory key-value adapters satisfying complete contract lifecycles.

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
<summary><b>🔍 View Exercise Solutions (Storage Adapters & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Multi-Database Storage Engine Adapters
# =====================================================================
from abc import ABC, abstractmethod

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
        return self._table.pop(record_id, None) is not None


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


pg_adapter = PostgresStorageAdapter("postgresql://user:pass@localhost:5432/appdb")
redis_adapter = RedisStorageAdapter("redis://localhost:6379/0")

print("==================================================")
print("        STORAGE ADAPTER CONTRACT COMPLIANCE       ")
print("==================================================")
pg_adapter.connect()
redis_adapter.connect()
print("--------------------------------------------------")
print("ADAPTER OPERATIONS TEST:")

pg_adapter.save_record("USR-101", {"username": "erostova", "role": "admin"})
pg_rec = pg_adapter.fetch_record("USR-101")
print(f"  ✓ [{pg_adapter.engine_type}]: Saved record 'USR-101'")
print(f"  ✓ [{pg_adapter.engine_type}]: Fetched record: {pg_rec}")

redis_adapter.save_record("SESSION-909", {"token": "jwt_secret_xyz"})
rd_rec = redis_adapter.fetch_record("SESSION-909")
print(f"  ✓ [{redis_adapter.engine_type}]: Saved record 'SESSION-909'")
print(f"  ✓ [{redis_adapter.engine_type}]: Fetched record: {rd_rec}")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
class BaseShape(ABC):
    @abstractmethod
    def area(self) -> float: pass
class Square(BaseShape):
    def __init__(self, s: float): self.s = s
    def area(self): return self.s ** 2

# Ex 2:
class CloudClient(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str: pass
class AWSClient(CloudClient):
    @property
    def provider_name(self): return "Amazon Web Services"

# Ex 3:
class BaseFileParser(ABC):
    @abstractmethod
    def parse(self, raw: str) -> list[dict]: pass
class CSVFileParser(BaseFileParser):
    def parse(self, raw): return [{"val": line} for line in raw.strip().split("\n")]

# Ex 4:
class BaseETL(ABC):
    @abstractmethod
    def extract(self): pass
    @abstractmethod
    def transform(self, d): pass
    @abstractmethod
    def load(self, d): pass
    def run_pipeline(self):
        d = self.extract()
        t = self.transform(d)
        return self.load(t)

# Ex 5:
class CacheEngine(ABC):
    @abstractmethod
    def get(self, k): pass
    @abstractmethod
    def set(self, k, v, ttl=0): pass
    @abstractmethod
    def clear(self): pass
class InMemoryCache(CacheEngine):
    def __init__(self): self.d = {}
    def get(self, k): return self.d.get(k)
    def set(self, k, v, ttl=0): self.d[k] = v
    def clear(self): self.d.clear()

# Ex 6:
class BasePaymentGateway(ABC):
    @abstractmethod
    def charge(self, amt: float) -> bool: pass
    @abstractmethod
    def refund(self, txn_id: str, amt: float) -> bool: pass

# Ex 7:
class Streamable(ABC):
    @abstractmethod
    def stream_bytes(self) -> bytes: pass
class ExternalAudioStream:
    def stream_bytes(self): return b"\x00\x01"
Streamable.register(ExternalAudioStream)

# Ex 8:
from typing import Protocol, runtime_checkable
@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes: ...
class XMLDoc:
    def serialize(self): return b"<xml></xml>"
class JSONDoc:
    def serialize(self): return b"{}"

# Ex 9:
class BaseSerializer(ABC):
    @abstractmethod
    def dump(self, obj) -> str: pass
```
</details>

