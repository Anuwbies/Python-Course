"""
================================================================================
Level 2: Intermediate Python
Lesson 2: Encapsulation, Properties & Magic Dunder Methods
================================================================================
📝 Quick Exercise Prompt:

Create a `Money` class:
1. Attributes: `amount` (float), `currency` (str, e.g. `"USD"`).
2. Validate with `@property` that `amount >= 0`.
3. Implement `__add__` so that `Money(10, "USD") + Money(25, "USD")` returns `Money(35, "USD")`. Raise a `ValueError` if currencies don't match.
4. Implement `__repr__` returning `f"Money({self.amount}, '{self.currency}')"`.
================================================================================
"""

# Write your solution below:

