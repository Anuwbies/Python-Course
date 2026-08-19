"""
================================================================================
Level 2: Intermediate Python
Lesson 3: Abstract Base Classes (ABCs) & Composition
================================================================================
📝 Quick Exercise Prompt:

1. Create an abstract class `NotificationSender(ABC)` with `@abstractmethod def send(self, recipient: str, message: str) -> None:`.
2. Create concrete classes `EmailSender` and `SMSSender`.
3. Create an `AlertManager` class that takes a `NotificationSender` via its constructor (Dependency Injection) and has a method `notify_all(users, alert_text)`.
================================================================================
"""

# Write your solution below:

