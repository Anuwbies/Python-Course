# Lesson 3: Abstract Base Classes (ABCs) & Composition

In scalable software architecture, we often need to define rigid interface contracts without providing concrete implementations. We also need to decide when to use **Inheritance** ("is-a") versus **Composition** ("has-a").

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Enforce interface contracts using Python's `abc` module (`ABC`, `@abstractmethod`).
2. Understand why abstract classes cannot be instantiated directly.
3. Understand the design principle: *"Favor object composition over class inheritance"*.
4. Implement Dependency Injection and pluggable components.

---

## 1. Abstract Base Classes with `abc.ABC`

An **Abstract Base Class (ABC)** defines methods that all subclasses **must** implement. If a subclass fails to implement even one `@abstractmethod`, Python prevents it from being instantiated.

```python
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    """Abstract interface for all payment providers."""

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Subclasses must implement actual processing logic."""
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        """Subclasses must implement refund logic."""
        pass

# Concrete Implementation 1: Stripe
class StripeGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"💳 Charged ${amount:.2f} via Stripe API token.")
        return True

    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        print(f"↩️ Refunded ${amount:.2f} for tx {transaction_id} via Stripe.")
        return True

# Concrete Implementation 2: PayPal
class PayPalGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"🅿️ Charged ${amount:.2f} via PayPal Express Checkout.")
        return True

    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        print(f"↩️ Refunded ${amount:.2f} for tx {transaction_id} via PayPal.")
        return True
```

> [!CAUTION]
> Trying to do `gateway = PaymentGateway()` will raise `TypeError: Can't instantiate abstract class PaymentGateway with abstract methods`.

---

## 2. Composition vs Inheritance ("Has-A" vs "Is-A")

Inheritance tightly couples classes. **Composition** builds complex functionality by combining simple, swappable objects ("has-a").

```python
class Engine:
    def start(self) -> str:
        return "Engine ignition active."

class GPS:
    def locate(self) -> str:
        return "Coordinates: 37.7749° N, 122.4194° W"

# Car HAS-AN engine and HAS-A gps (Composition)
class Car:
    def __init__(self, engine: Engine, gps: GPS):
        self.engine = engine # Injected dependency
        self.gps = gps       # Injected dependency

    def drive(self) -> None:
        print(self.engine.start())
        print(f"Navigation: {self.gps.locate()}")

car = Car(Engine(), GPS())
car.drive()
```

---

## 📝 Quick Exercise

**Prompt**:
1. Create an abstract class `NotificationSender(ABC)` with `@abstractmethod def send(self, recipient: str, message: str) -> None:`.
2. Create concrete classes `EmailSender` and `SMSSender`.
3. Create an `AlertManager` class that takes a `NotificationSender` via its constructor (Dependency Injection) and has a method `notify_all(users, alert_text)`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from abc import ABC, abstractmethod

class NotificationSender(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        pass

class EmailSender(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"📧 Email to [{recipient}]: {message}")

class SMSSender(NotificationSender):
    def send(self, recipient: str, message: str) -> None:
        print(f"📱 SMS to [{recipient}]: {message}")

class AlertManager:
    def __init__(self, sender: NotificationSender):
        self.sender = sender # Dependency Injection

    def notify_all(self, users: list[str], alert_text: str) -> None:
        for user in users:
            self.sender.send(user, alert_text)

# Easily swap email vs SMS at runtime!
alerts = AlertManager(EmailSender())
alerts.notify_all(["alice@domain.com", "bob@domain.com"], "System reboot in 5 minutes.")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What error is raised if a subclass forgets to implement an `@abstractmethod` when instantiated?**
   - A) `NotImplementedError`
   - B) `TypeError`
   - C) `AttributeError`
   - D) `SyntaxError`
   *(Answer: B)*

2. **Why is composition often preferred over deep inheritance hierarchies?**
   - A) It provides greater flexibility, lower coupling, and allows swapping behaviors at runtime
   - B) It uses 90% less RAM
   - C) Python prohibits inheritance beyond 2 levels
   - D) Composition automatically compiles to C
   *(Answer: A)*
