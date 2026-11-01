# Lesson 4: Descriptors & Class Creation

**Prerequisites:** Levels 1–9 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Descriptors_And_Class_Creation.py`.

Understand the mechanisms behind managed attributes and declarative classes before extending them. Use a small inspectable example and keep attribute lookup, instance initialization, and class construction distinct.

## 1. Intercept an attribute operation

A descriptor is an object stored on a class that defines methods such as __get__, __set__, or __delete__. A data descriptor with assignment behavior can take precedence over an instance dictionary entry during ordinary attribute lookup. A non-data descriptor follows different precedence rules.

Properties are a familiar managed-attribute form. Functions stored on classes also participate in descriptor binding, which explains how accessing an instance method produces a callable associated with that instance. This is a language object-model mechanism, not a special case for one application framework.

## 2. Learn the declared field name

`__set_name__(owner, name)` is called during normal class creation for attributes implementing that hook. A descriptor can derive an internal storage name from its public name. When accessed through the class with instance None, returning the descriptor itself is a common useful interface.

For an uninitialized instance field, raise AttributeError rather than exposing an internal dictionary KeyError. For assignment, validate before writing the backing value so a rejected update preserves prior valid state. Reusing one descriptor instance under several names requires an explicit naming policy.

## 3. Distinguish __new__ and __init__

An instance's __new__ creates or returns the instance object; __init__ initializes it when applicable. Immutable-type customization often needs creation-time logic rather than a later attribute assignment. Do not override these methods merely to print lifecycle messages in otherwise ordinary models.

The metaclass is the class of a class object. A custom type subclass can inspect a class namespace in its __new__, delegate to type's construction, and attach derived metadata. Returning a class object is different from constructing an instance of the resulting class.

## 4. Inspect a declaration deliberately

A metaclass can collect descriptor-valued attributes declared in its namespace. State whether inherited declarations are included; the task collects only fields declared directly on the class. Silently overwriting inherited metadata would otherwise create a subtle schema inconsistency.

Class decorators and __init_subclass__ can solve many simpler registration problems without a custom metaclass. A metaclass can also conflict with another base's class-construction requirements. Choose the least complex hook that expresses the actual needed behavior.

## 5. Keep effects bounded

A descriptor should not hide an unexpected network call behind a cheap-looking attribute read. A class-construction hook should not contact external services merely because a module is imported. Explicit lifetime and error contracts remain important even at these advanced boundaries.

The exercise combines one validated descriptor and one small metadata collector so the mechanism can be traced. It is not a complete ORM, and it does not claim to implement every edge case of Python attribute resolution.

## Trace a minimal descriptor and metaclass

`instance.__dict__` is the ordinary per-instance attribute dictionary for these unslotted objects. A descriptor can store its validated value there under a distinct key. Its `__get__(self, instance, owner)` receives None as instance for class access, so return self on that path rather than trying to read instance state.

```python
class TextField:
    def __set_name__(self, owner, name):
        self.storage = "_" + name
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        if self.storage not in instance.__dict__:
            raise AttributeError(self.storage)
        return instance.__dict__[self.storage]
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("Expected text")
        instance.__dict__[self.storage] = value

class LabelMeta(type):
    def __new__(metaclass, name, bases, namespace):
        cls = super().__new__(metaclass, name, bases, namespace)
        cls.label = name.lower()
        return cls

class Message(metaclass=LabelMeta):
    text = TextField()

message = Message()
message.text = "hello"
print(Message.label, message.text)  # message hello
```

The namespace is the dictionary populated by the class body; bases is the tuple of base classes. super().__new__ builds the class and invokes its descriptor naming hooks. To collect fields, iterate namespace.items(), retain values that are instances of the desired descriptor, and build a tuple of their names. `metaclass=...` selects class construction; it does not pass an argument to an instance initializer.

References: [Descriptor guide](https://docs.python.org/3.13/howto/descriptor.html), [Class creation](https://docs.python.org/3.13/reference/datamodel.html#customizing-class-creation).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the difference between reading the descriptor through the class and an initialized instance.
2. **Explain:** Explain why validation precedes writing the backing attribute.
3. **Modify:** Collect only directly declared fields and describe the inherited-field limitation.
4. **Debug:** Replace a metaclass with a simpler hook when only basic registration is needed.

<details>
<summary>Hints</summary>

The metaclass inspects declarations; the descriptor manages each instance's value.

</details>

## Independent task: descriptors & class creation

In `Practice/04_Descriptors_And_Class_Creation.py`, complete this task:

Implement Nonnegative with set_name/get/set, requiring a plain nonnegative integer and preserving the old value on rejection. Class access returns the descriptor; an uninitialized instance read raises AttributeError. Implement FieldMeta(type) collecting directly declared Nonnegative attribute names into field_names. Define Account(metaclass=FieldMeta) with balance and an initializer assigning it. Print Account.field_names, a starting balance of 100, Rejected after assigning -1, and the unchanged balance.

Expected output:

```text
('balance',)
100
Rejected
100
```
