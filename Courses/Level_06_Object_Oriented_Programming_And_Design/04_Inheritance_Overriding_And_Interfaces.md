# Lesson 4: Inheritance, Overriding & Interfaces

**Prerequisites:** Levels 1–5 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Inheritance_Overriding_And_Interfaces.py`.

Design a subtype that preserves the behavior callers expect from an interface. Inheritance describes substitutability; copying a method name or sharing code is not enough.

## 1. Override an intended operation

A subclass names its base class in parentheses. It inherits accessible behavior and can override a method by defining the same name. `super()` delegates through the method resolution order, allowing a subclass to reuse initialization without referring directly to a particular parent implementation.

```python
class Task:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return self.name

class NamedTask(Task):
    def describe(self):
        return "Task: " + super().describe()

print(NamedTask("report").describe())
```

Do not call super merely by habit: understand which shared behavior needs to run and what state it establishes. Multiple inheritance adds an ordered method search and cooperation rules; it is an extension to investigate when needed, not a requirement for every application.

## 2. Express a required method

The abc module provides ABC and abstractmethod. A class with unimplemented abstract methods cannot be instantiated. The decorator marks a required interface method for this runtime construction rule; it does not supply the missing behavior.

```python
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError
```

A concrete subclass implements read. An abstract method can include shared code, but the simple interface here deliberately has no usable default. Raising NotImplementedError is an explicit unsupported operation, not a successful empty result.

## 3. Preserve the contract

If the interface promises a fresh list of amounts, a subclass should not return a live internal collection or sometimes return a string instead. An override that introduces surprising extra preconditions can also break a caller that only knows the base contract.

Use a test through the interface operation rather than through unrelated implementation details. An identical method signature is useful but does not establish semantic substitutability. Error behavior and side effects belong to the same contract as result types.

## 4. Compare with composition

A file reader and memory reader can implement one reading interface. A report service can hold either reader through composition. This combines polymorphism with explicit dependencies instead of forcing all responsibilities into one inheritance tree.

Prefer a small interface defined by actual callers. A large base class with dozens of methods often creates irrelevant obligations and fake implementations. The goal is predictable behavior at the boundary, not the maximum number of abstraction layers.

References: [Abstract base classes](https://docs.python.org/3.13/library/abc.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the effect of constructing a class that still has an abstract method.
2. **Explain:** Explain the behavioral promise needed for two readers to be interchangeable.
3. **Modify:** Use a reader through a composed report service.
4. **Debug:** Find an override that changes a fresh-list promise into a live-state return.

<details>
<summary>Hints</summary>

The base states the contract; the concrete implementation must actually supply it.

</details>

## Independent task: inheritance, overriding & interfaces

In `Practice/04_Inheritance_Overriding_And_Interfaces.py`, complete this task:

Define an abstract `AmountReader.read()` contract returning a fresh list of integers. Implement `MemoryReader(values)` that copies incoming and outgoing lists. Instantiate it for `[120, 80]`, call read through a variable named reader, and print the returned list and total.

Expected output:

```text
[120, 80]
200
```
