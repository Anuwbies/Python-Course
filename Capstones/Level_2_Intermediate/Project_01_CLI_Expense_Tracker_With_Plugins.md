# Capstone Project 2.1: Extensible Expense Tracker & Plugin Engine

## 📌 Project Overview
Design an extensible, enterprise-grade **Personal Finance & Expense Tracker CLI** that features dynamic export plugins, budget threshold monitoring, custom currency converters, decorator-based audit logging, context-managed atomic transactions, and a full `pytest` verification suite.

---

## 🎯 Learning Objectives
- **Abstract Base Classes (`abc.ABC`)**: Define contracts for export plugins (`BaseExporter`) and currency conversion engines.
- **Magic (Dunder) Methods**: Implement `__len__`, `__iter__`, `__getitem__`, `__add__`, `__repr__`, and `__eq__` on transaction containers.
- **Properties & Validation**: Use `@property` and `@setter` to enforce business logic and prevent invalid states.
- **Custom Exceptions**: Build domain-specific exception hierarchies (`FinanceError`, `BudgetExceededError`, `InvalidCurrencyError`).
- **Decorators**: Write execution timers and audit decorators that record all state modifications.
- **Context Managers**: Guarantee thread-safe or atomic file writes using `__enter__` and `__exit__`.

---

## 🏗️ System Architecture

```text
               +-------------------------------------+
               |         Expense Ledger Engine       |
               +-------------------------------------+
                                  |
         +------------------------+------------------------+
         |                        |                        |
+-------------------+   +--------------------+   +-------------------+
|  Expense (Model)  |   |   BaseExporter     |   |   AuditDecorator  |
+-------------------+   |   (Abstract Class) |   +-------------------+
| - id: UUID        |   +--------------------+   | @audit_log        |
| - amount: Decimal |   | + export(ledger)   |   | @timing_tracker   |
| - category: str   |   +---------+----------+   +-------------------+
| - date: datetime  |             |
| @property amount  |   +---------+---------+
+-------------------+   |                   |
               +-----------------+ +-----------------+
               |  JSONExporter   | |   CSVExporter   |
               +-----------------+ +-----------------+
```

---

## 📋 Functional Requirements

### 1. Expense Model with Properties & Dunder Methods
- Attributes: `id` (UUID), `title` (str), `amount` (Decimal or float), `category` (str), `timestamp` (datetime).
- `@property` for `amount`: Must validate that `amount > 0`.
- Magic Methods:
  - `__eq__`: Two expenses are equal if their `id` matches.
  - `__add__`: Adding two `Expense` objects returns total combined cost.
  - `__repr__`: Clear debugging string representation.

### 2. ExpenseLedger Collection Container
- Implements `__len__`, `__iter__`, and `__getitem__`.
- Custom Exception Handling:
  - Adding an expense that pushes a category past its monthly budget limit raises `BudgetExceededError(category, limit, attempted)`.
  - Fetching a non-existent expense raises `ExpenseNotFoundError`.

### 3. Abstract Plugin Architecture
Define an abstract interface for report exporters:
```python
from abc import ABC, abstractmethod

class BaseExporter(ABC):
    @abstractmethod
    def export(self, ledger: 'ExpenseLedger', destination_path: str) -> None:
        """Export ledger contents to destination path."""
        pass
```
Implement at least two concrete plugins:
- `CSVExporter`: Writes tabular data with headers.
- `MarkdownExporter`: Writes formatted GitHub-flavored markdown tables with summary totals.

### 4. Custom Decorators
- `@audit_log`: Appends timestamp, method name, and arguments to an `audit.log` file whenever an expense is created, updated, or deleted.
- `@enforce_budget(limit=1000.0)`: Verifies ledger limits before permitting addition.

### 5. Context Manager for Atomic Persistence
Implement `AtomicLedgerStorage` ensuring that if saving fails midway, the original backup file is preserved untouched.

---

## 📐 Phased Implementation Guide

### Phase 1: Custom Exceptions Hierarchy
```python
class FinanceError(Exception):
    """Base exception for all finance tracker errors."""
    pass

class BudgetExceededError(FinanceError):
    def __init__(self, category: str, limit: float, current_total: float, attempted_amount: float):
        super().__init__(
            f"Budget exceeded for category '{category}'! Limit: ${limit:.2f}, "
            f"Current: ${current_total:.2f}, Attempted: ${attempted_amount:.2f}"
        )
        self.category = category
        self.limit = limit
        self.current_total = current_total
        self.attempted_amount = attempted_amount

class ExpenseNotFoundError(FinanceError):
    pass
```

### Phase 2: Dunder Methods & Properties
```python
from datetime import datetime
import uuid

class Expense:
    def __init__(self, title: str, amount: float, category: str, timestamp: datetime = None):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.category = category
        self._amount = 0.0
        self.amount = amount  # Triggers property setter validation
        self.timestamp = timestamp or datetime.now()

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Expense amount must be strictly positive.")
        self._amount = round(float(value), 2)

    def __repr__(self) -> str:
        return f"Expense(id='{self.id}', title='{self.title}', amount={self.amount}, category='{self.category}')"

    def __add__(self, other: 'Expense') -> float:
        if isinstance(other, Expense):
            return self.amount + other.amount
        elif isinstance(other, (int, float)):
            return self.amount + other
        return NotImplemented
```

### Phase 3: Exporter Plugins & Context Manager
Implement `BaseExporter`, `CSVExporter`, `MarkdownExporter`, and atomic file management.

---

## 🧪 Pytest Test Suite Specifications

Your codebase must include a `test_expense_tracker.py` suite covering:
1. `test_negative_amount_raises_value_error()`
2. `test_ledger_len_and_iteration()`
3. `test_budget_exceeded_raises_custom_exception()`
4. `test_csv_and_markdown_exporters()`
5. `test_atomic_storage_reverts_on_failure()`

---

## 🚀 Bonus Challenges
- **Plugin Auto-Discovery**: Dynamically discover and load new exporter classes placed in a `plugins/` directory using `importlib` and `inspect`.
- **Multi-Currency Converter**: Integrate live exchange rate caching using `urllib` and memoized cache decorators.
