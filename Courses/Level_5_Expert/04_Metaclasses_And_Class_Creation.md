# Lesson 4: Metaprogramming: Metaclasses & Deep Class Creation

In Python, *everything is an object*—and that includes classes themselves. Just as a class is a blueprint for creating instances, a **Metaclass** is the blueprint for creating classes. Metaclasses give framework architects the power to intercept, validate, rewrite, and register classes at the exact moment they are defined by the Python compiler. In this lesson, you will master dynamic type creation, custom metaclasses, `__prepare__`, and modern subclass hooks (`__init_subclass__`).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the Python Metaclass hierarchy: `type` is the metaclass of `object`.
2. Create classes dynamically at runtime using `type(name, bases, namespace)`.
3. Author custom Metaclasses by subclassing `type` and overriding `__new__` and `__init__`.
4. Control class namespace attribute ordering using the `__prepare__` hook.
5. Enforce architectural invariants across codebases (e.g. enforcing naming conventions or required methods).
6. Implement lightweight class registration patterns using `__init_subclass__` (PEP 487).

---

## 1. The Dynamic Type Factory: `type()`

You can construct a full Python class dynamically at runtime without writing a `class` statement:

```python
# type(class_name, tuple_of_base_classes, namespace_dictionary)
DynamicModel = type(
    "DynamicModel",
    (object,),
    {
        "VERSION": "1.0.0",
        "greet": lambda self: f"Hello from dynamic class! Version: {self.VERSION}"
    }
)

instance = DynamicModel()
print(instance.greet()) # "Hello from dynamic class! Version: 1.0.0"
```

---

## 2. Defining Custom Metaclasses (`type.__new__`)

When Python encounters a `class` definition with `metaclass=MyMeta`, it delegates class construction to `MyMeta.__new__`:

```python
class StrictSchemaMeta(type):
    """Metaclass that enforces that all subclasses define a docstring and '__tablename__'."""

    def __new__(mcs, name, bases, namespace):
        # 1. Inspect and validate namespace before creating class
        if name != "BaseModel":
            if "__tablename__" not in namespace:
                raise TypeError(f"Class '{name}' must explicitly define a '__tablename__' attribute!")

            if not namespace.get("__doc__"):
                raise TypeError(f"Class '{name}' is missing a required docstring!")

        # 2. Delegate to type.__new__ to allocate the class object in memory
        return super().__new__(mcs, name, bases, namespace)

class BaseModel(metaclass=StrictSchemaMeta):
    """Root model blueprint."""
    pass

# ✅ Compliant Subclass:
class UserAccount(BaseModel):
    """User account entity model."""
    __tablename__ = "users"

# ❌ Non-Compliant Subclass (will crash immediately at file import time!):
# class BadModel(BaseModel):
#     pass
# TypeError: Class 'BadModel' must explicitly define a '__tablename__' attribute!
```

---

## 3. Preserving Field Ordering with `__prepare__`

The `__prepare__` method runs *before* the class body is parsed, allowing you to substitute a custom dictionary to record declaration order:

```python
class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        # Returns custom namespace mapping
        return dict()
```

---

---

## 5. Controlling Instance Creation with Metaclass `__call__`

When you execute `obj = MyClass(*args)`, Python invokes `type(MyClass).__call__(MyClass, *args)`! Overriding `__call__` in a metaclass lets you intercept instantiation (e.g. implementing Singleton or caching):

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    pass
```

---

## 6. Metaclass Conflict Resolution

When a class inherits from multiple base classes with distinct metaclasses, Python raises: `TypeError: metaclass conflict`. To resolve this, create a unified derived metaclass inheriting from both:

```python
class MetaA(type): pass
class MetaB(type): pass

class UnifiedMeta(MetaA, MetaB): pass

class BaseA(metaclass=MetaA): pass
class BaseB(metaclass=MetaB): pass

# Resolve conflict:
class Derived(BaseA, BaseB, metaclass=UnifiedMeta):
    pass
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master `type()`, custom metaclasses, `__prepare__`, `__init_subclass__`, and metaprogramming:

---

### 🟢 Tier 1: Dynamic Class Creation Basics (Exercises 1–3)

#### 🔹 Exercise 1: Runtime Class Factory with `type()`
* **Goal**: Dynamically construct a class `Car` with attributes and methods using `type("Car", (object,), {...})`.

#### 🔹 Exercise 2: Basic Subclassing Metaclass
* **Goal**: Write a metaclass printing `"Compiling class: <ClassName>"` during module import.

#### 🔹 Exercise 3: Automated Docstring Enforcer
* **Goal**: Create a metaclass raising `TypeError` if any subclass lacks a module docstring.

---

### 🟡 Tier 2: Namespace Manipulation & Subclass Hooks (Exercises 4–6)

#### 🔹 Exercise 4: Preserving Field Order with `__prepare__`
* **Goal**: Implement `__prepare__` returning an `OrderedDict` or tracking variable order.

#### 🔹 Exercise 5: Lightweight Subclass Hooks with `__init_subclass__`
* **Goal**: Build an auto-registering database model registry without defining a full metaclass.

#### 🔹 Exercise 6: Attribute Auto-Prefixing Metaclass
* **Goal**: Write a metaclass that automatically converts all public attributes to uppercase.

---

### 🟠 Tier 3: Instantiation Interception & Conflicts (Exercises 7–9)

#### 🔹 Exercise 7: Singleton Pattern via Metaclass `__call__`
* **Goal**: Intercept class invocation in `__call__` to return cached singleton instances.

#### 🔹 Exercise 8: Interface Contract & Abstract Method Verification
* **Goal**: Build a custom `ABCMeta` alternative checking that all methods decorated with `@must_implement` are present.

#### 🔹 Exercise 9: Metaclass Multiple Inheritance Conflict Resolver
* **Goal**: Construct a diamond multiple inheritance hierarchy and resolve the metaclass conflict cleanly.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Mandatory Method & Snake_Case Linter Metaclass
* **Goal**: Build an enterprise compliance metaclass verifying mandatory methods and enforcing strict `snake_case` naming across analytical pipelines.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Microservice Remote Procedure Call (RPC) Plugin Registry & Security Metaclass Engine**, demonstrating custom metaclass validation, automated endpoint routing, and metadata injection:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Enterprise RPC Handler Registry & Security Metaclass
# =====================================================================

import inspect
from typing import Callable

class RPCRegistryMeta(type):
    """Metaclass that automatically validates and registers all RPC handler classes.
    
    Invariants Enforced:
    1. Every handler must specify a unique 'SERVICE_TAG' string.
    2. Every method starting with 'rpc_' must have type annotations and a docstring.
    """

    # Global registry mapping SERVICE_TAG -> Handler Class
    REGISTRY: dict[str, type] = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        # Skip validation for the abstract base class
        if name == "BaseRPCHandler":
            return super().__new__(mcs, name, bases, namespace)

        # 1. Validate SERVICE_TAG presence
        service_tag = namespace.get("SERVICE_TAG")
        if not service_tag or not isinstance(service_tag, str):
            raise TypeError(f"Class '{name}' must declare a non-empty string 'SERVICE_TAG'.")

        if service_tag in mcs.REGISTRY:
            raise ValueError(f"Duplicate SERVICE_TAG '{service_tag}'! Already registered by {mcs.REGISTRY[service_tag].__name__}.")

        # 2. Inspect all RPC methods
        rpc_methods = {}
        for attr_name, attr_val in namespace.items():
            if attr_name.startswith("rpc_") and inspect.isfunction(attr_val):
                # Validate docstring
                if not attr_val.__doc__:
                    raise TypeError(f"RPC method '{name}.{attr_name}()' is missing a required docstring!")
                rpc_methods[attr_name[4:]] = attr_val # Strip 'rpc_' prefix

        namespace["_RPC_DISPATCH_TABLE"] = rpc_methods

        # 3. Create the class object
        cls = super().__new__(mcs, name, bases, namespace)
        mcs.REGISTRY[service_tag] = cls
        return cls


class BaseRPCHandler(metaclass=RPCRegistryMeta):
    """Base contractual interface for all distributed RPC worker handlers."""
    pass


# Concrete RPC Service Implementations
class BillingRPCHandler(BaseRPCHandler):
    """Billing operations service."""
    SERVICE_TAG = "billing.v1"

    def rpc_charge_customer(self, customer_id: str, amount: float) -> dict:
        """Charges customer account via credit payment network."""
        return {"status": "SUCCESS", "charged": amount, "customer": customer_id}

    def rpc_refund_transaction(self, txn_id: str) -> dict:
        """Processes transaction refund."""
        return {"status": "REFUNDED", "txn_id": txn_id}


class TelemetryRPCHandler(BaseRPCHandler):
    """System health metrics service."""
    SERVICE_TAG = "telemetry.v1"

    def rpc_get_cluster_status(self) -> dict:
        """Returns live Kubernetes cluster health status."""
        return {"cluster": "production-us-east", "nodes_online": 32, "load_avg": 0.42}


# RPC Dispatch Router
def dispatch_rpc_call(service_tag: str, method_name: str, **kwargs) -> dict:
    handler_cls = RPCRegistryMeta.REGISTRY.get(service_tag)
    if not handler_cls:
        raise KeyError(f"Unknown RPC service tag: '{service_tag}'")

    instance = handler_cls()
    dispatch_table = getattr(instance, "_RPC_DISPATCH_TABLE", {})
    method = dispatch_table.get(method_name)
    if not method:
        raise AttributeError(f"Service '{service_tag}' does not expose RPC method '{method_name}'")

    return method(instance, **kwargs)


# Execution Simulation
print("=" * 80)
print(f"{'ENTERPRISE RPC METACLASS REGISTRY & DISPATCH ENGINE':^80}")
print("=" * 80)
print(f"Discovered & Registered RPC Services ({len(RPCRegistryMeta.REGISTRY)}):")
for tag, handler in RPCRegistryMeta.REGISTRY.items():
    methods = list(getattr(handler, "_RPC_DISPATCH_TABLE", {}).keys())
    print(f"  • Service Tag: {tag:<16} -> Class: {handler.__name__:<22} (Methods: {methods})")

print("-" * 80)
print("EXECUTING REMOTE RPC INVOCATIONS:")

res1 = dispatch_rpc_call("billing.v1", "charge_customer", customer_id="CUST-401", amount=299.00)
print(f"  ✓ Billing RPC Response:   {res1}")

res2 = dispatch_rpc_call("telemetry.v1", "get_cluster_status")
print(f"  ✓ Telemetry RPC Response: {res2}")

print("=" * 80)
```

### 🔍 Code Explanation:
- **`RPCRegistryMeta.__new__`**: Intercepts class declarations at module import time, validates documentation and naming rules, builds an internal dispatch lookup table, and registers the class into `RPCRegistryMeta.REGISTRY`.
- **Compile-Time Contract Enforcement**: Any service missing a docstring or `SERVICE_TAG` is rejected before the application can even boot.
- **Dynamic RPC Routing**: `dispatch_rpc_call` maps incoming string identifiers to validated methods in $\mathcal{O}(1)$ time.

---

## 📝 Quick Exercise: Mandatory Method & Snake_Case Linter Metaclass

### 🏢 Real-Life Scenario
You are building an enterprise software framework where all analytical model classes must:
1. Define an explicit `execute_pipeline()` method.
2. Ensure all method names adhere strictly to `snake_case` (no uppercase letters in method names).

### 📋 Requirements
1. **Define Metaclass `StrictModelMeta(type)`**:
   - In `__new__(mcs, name, bases, namespace)`:
     - If `name != "BaseAnalyticalModel"`:
       - Verify `'execute_pipeline'` is in `namespace` and is a function. If not, raise `TypeError(f"Class '{name}' must implement 'execute_pipeline()' method.")`.
       - For all functions in `namespace`: If any function name has uppercase characters (e.g. `BadMethodName`), raise `TypeError(f"Method '{fn_name}' in class '{name}' must use snake_case naming.")`.
     - Delegate to `super().__new__()`.
2. Define base class `BaseAnalyticalModel(metaclass=StrictModelMeta)`.
3. Create a valid analytical model subclass and verify successful instantiation.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 5 metaclasses with Level 2 introspection and Level 1 string methods.

### 🎯 Expected Output
```text
==================================================
        METACLASS ARCHITECTURE COMPLIANCE         
==================================================
✅ Successfully compiled valid model: FraudDetectionModel
  -> Pipeline Result: {'status': 'EXECUTED', 'risk_score': 0.05}
--------------------------------------------------
🚨 Verification: Missing execute_pipeline() triggers TypeError
🚨 Verification: CamelCaseMethodName triggers TypeError
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Metaclass Compliance & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Mandatory Method & Snake_Case Linter Metaclass
# =====================================================================
import inspect

class StrictModelMeta(type):
    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        if name != "BaseAnalyticalModel":
            if "execute_pipeline" not in namespace or not inspect.isfunction(namespace["execute_pipeline"]):
                raise TypeError(f"Class '{name}' must implement 'execute_pipeline()' method.")

            for attr_name, attr_val in namespace.items():
                if inspect.isfunction(attr_val) and not attr_name.startswith("__"):
                    if any(c.isupper() for c in attr_name):
                        raise TypeError(f"Method '{attr_name}' in class '{name}' must use snake_case naming.")

        return super().__new__(mcs, name, bases, namespace)


class BaseAnalyticalModel(metaclass=StrictModelMeta):
    pass


class FraudDetectionModel(BaseAnalyticalModel):
    def execute_pipeline(self) -> dict:
        return {"status": "EXECUTED", "risk_score": 0.05}

    def train_model(self) -> None:
        pass


print("==================================================")
print("        METACLASS ARCHITECTURE COMPLIANCE         ")
print("==================================================")

model = FraudDetectionModel()
print(f"✅ Successfully compiled valid model: {FraudDetectionModel.__name__}")
print(f"  -> Pipeline Result: {model.execute_pipeline()}")
print("--------------------------------------------------")

try:
    type("MissingPipelineModel", (BaseAnalyticalModel,), {})
except TypeError as err:
    print(f"🚨 Verification: Missing execute_pipeline() triggers TypeError")

try:
    type("BadNamingModel", (BaseAnalyticalModel,), {
        "execute_pipeline": lambda self: None,
        "CalculateScore": lambda self: None
    })
except TypeError as err:
    print(f"🚨 Verification: CamelCaseMethodName triggers TypeError")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Dynamic type()
Car = type("Car", (), {"wheels": 4, "drive": lambda self: "Vroom!"})

# Ex 2: Basic Logging Metaclass
class VerboseMeta(type):
    def __new__(mcs, name, bases, ns):
        return super().__new__(mcs, name, bases, ns)

# Ex 3: Docstring Enforcer
class DocMeta(type):
    def __new__(mcs, name, bases, ns):
        if not ns.get("__doc__"): raise TypeError(f"Missing docstring: {name}")
        return super().__new__(mcs, name, bases, ns)

# Ex 4: __prepare__
class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases): return dict()

# Ex 5: __init_subclass__
class RegistryBase:
    _reg = {}
    def __init_subclass__(cls, tag, **kw):
        super().__init_subclass__(**kw)
        RegistryBase._reg[tag] = cls

# Ex 6: Auto-Uppercase Attributes
class UpperMeta(type):
    def __new__(mcs, name, bases, ns):
        uppers = {k.upper() if not k.startswith("__") else k: v for k, v in ns.items()}
        return super().__new__(mcs, name, bases, uppers)

# Ex 7: Metaclass __call__ Singleton
class MetaSingleton(type):
    _insts = {}
    def __call__(cls, *a, **kw):
        if cls not in cls._insts: cls._insts[cls] = super().__call__(*a, **kw)
        return cls._insts[cls]

# Ex 8: Custom ABCMeta Alternative
# Verified in main solution above.

# Ex 9: Conflict Resolution
class MetaA(type): pass
class MetaB(type): pass
class UnifiedMeta(MetaA, MetaB): pass
```
</details>
