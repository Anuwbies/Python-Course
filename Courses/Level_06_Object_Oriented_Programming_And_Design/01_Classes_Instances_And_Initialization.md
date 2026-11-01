# Lesson 1: Classes, Instances & Initialization

**Prerequisites:** Levels 1–5. **Practice file:** `Practice/01_Classes_Instances_And_Initialization.py`.

Group state and the operations that give it meaning. A class describes a kind of object; each instance represents a particular object with its own state.

## 1. Create a small instance model

A class body defines methods and class-level names. Calling the class creates an instance and invokes its initializer. `__init__` initializes an already created object; object allocation itself is a separate mechanism studied in the expert level.

```python
class Tracker:
    def __init__(self, owner):
        self.owner = owner
        self.amounts = []

first = Tracker("Mika")
second = Tracker("José")
print(first.owner)
print(second.owner)
```

`self` refers to the instance receiving a method call. It is an ordinary parameter name used by convention. `first.method(...)` supplies first as that parameter automatically. An attribute assignment such as self.owner stores state on that instance, rather than creating only a local name.

## 2. Distinguish instance and class attributes

An assignment inside __init__ to self.amounts creates instance state. A mutable list placed directly in the class body can be shared by instances unless shadowed. Shared constants may be intentional; a user's expense history normally is not.

Draw two instances and label their amount lists separately. If an addition to the first appears in the second, inspect where the list was created. Recreating the whole object to hide the leak does not fix the underlying model.

## 3. Keep local parameters and attributes distinct

The parameter owner exists during initialization; self.owner persists on the object afterward. Writing only `owner = owner` reassigns a local name and does not initialize the object's field. A later method reading self.owner would then fail.

Attributes can refer to mutable objects, so the same copying questions from Level 3 still apply. If initialization accepts a caller's list, decide whether to retain that exact list or copy it. Classes do not automatically provide isolation.

## 4. Model a coherent responsibility

A class is useful when several operations depend on the same state and invariants. It is not required for a pure arithmetic function with no persistent state. Start with a small model whose fields have clear units and ownership.

Avoid unrelated global counters or network setup in a beginner initializer. A caller should understand what creating the object means. Later lessons introduce composition when storage or another service needs its own responsibility.

References: [Python classes](https://docs.python.org/3.13/tutorial/classes.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether two initializer-created lists share additions.
2. **Explain:** Explain why self.owner persists but a local owner parameter does not.
3. **Modify:** Accept an initial list and copy it according to an explicit ownership rule.
4. **Debug:** Move an accidentally shared class-level expense list into the initializer.

<details>
<summary>Hints</summary>

Create the mutable collection during each initialization.

</details>

## Independent task: classes, instances & initialization

In `Practice/01_Classes_Instances_And_Initialization.py`, complete this task:

Define `Tracker(owner)` with instance attributes owner and an independent empty amounts list. Create trackers for Mika and José, append 10 to the first list, and print each owner's name and list as shown. Do not use a shared class-level list.

Expected output:

```text
Mika [10]
José []
```
