# Lesson 3: Composition & Dependency Injection

**Prerequisites:** Levels 1–5 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Composition_And_Dependency_Injection.py`.

Give a collaborator its own responsibility and pass it to the object that needs it. Composition creates a has-a relationship without claiming that one service is a subtype of another.

## 1. Separate storage from use

An expense service needs to save and load records; a memory store knows how to retain them in this process. The service can receive a store in its initializer rather than create a hidden global store internally.

```python
class MemoryStore:
    def __init__(self):
        self.records = []

    def load(self):
        return self.records.copy()

class Service:
    def __init__(self, store):
        self.store = store

    def count(self):
        return len(self.store.load())
```

Passing the collaborator is dependency injection. The term describes a simple explicit parameter, not a requirement to install a framework. A test can pass an isolated memory store; a later application can pass a file-backed implementation with the same contract.

## 2. Define the collaborator's behavior

Agree on accepted inputs, returned records, ownership, and errors. Two objects having a method called load does not establish compatible behavior if one returns live internal state and the other returns independent records.

For a flat list of immutable integers, outer copies provide independence. For dictionaries, decide whether the store copies each record. Do not let a test fake succeed under a weaker contract than the real implementation.

## 3. Prefer explicit construction

A launcher can assemble the store and service together. This makes their lifetime and sharing visible. Passing the same store to two services intentionally shares persistence; passing two stores isolates them. Both designs can be correct for different use cases.

A default argument containing a store instance would be created at definition time and could unintentionally share state, like the mutable-default problem in Level 3. Use None and construct a fresh collaborator inside the call when that is the intended default.

## 4. Avoid inheritance for mere reuse

A service is not a kind of memory store simply because it uses one. Inheriting storage methods into the service can expose operations that violate the service's rules. Composition allows the service to present only its intended API.

Inheritance becomes useful when callers should substitute one implementation for a documented base interface. The next lesson develops that relationship. Choosing between them should follow behavioral meaning rather than a desire to reduce a few lines.

References: [Python classes](https://docs.python.org/3.13/tutorial/classes.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether two services share state when given the same store.
2. **Explain:** Explain why dependency injection can be a constructor argument.
3. **Modify:** Replace one memory store with an isolated second instance.
4. **Debug:** Repair a service that creates a hidden shared default collaborator.

<details>
<summary>Hints</summary>

Copy on both save and load so neither caller direction leaks mutable state.

</details>

## Independent task: composition & dependency injection

In `Practice/03_Composition_And_Dependency_Injection.py`, complete this task:

Define `MemoryStore` with save/load methods for lists of integers; both boundaries must copy the outer list. Define `ExpenseService(store)` with total() using store.load(). Save `[120, 80]`, create the service, and print its total. Modify a loaded copy by appending 999 and print the total again; it must remain unchanged.

Expected output:

```text
200
200
```
