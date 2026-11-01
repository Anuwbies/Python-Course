# Lesson 5: Properties & Object Representations

**Prerequisites:** Levels 1–5 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Properties_And_Object_Representations.py`.

Expose a stable object interface while retaining validation and useful diagnostics. Attribute-like access and string representations are protocols with specific expectations, not places to hide surprising work.

## 1. Validate through a property

A property exposes method-controlled access using attribute syntax. `@property` registers the getter; `@name.setter` registers assignment behavior for the same property. These decorators are library-supported class-definition mechanisms; custom decorator construction follows in Level 7.

```python
class Budget:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if type(value) is not int or value < 0:
            raise ValueError("Invalid amount")
        self._amount = value
```

The initializer uses the public property so it follows the same validation as later assignment. The setter updates a different backing attribute, avoiding recursive assignment to itself. Failed validation leaves the old backing value untouched.

## 2. Represent objects for people and debugging

`__str__` supplies a readable text form for str() and ordinary display. `__repr__` supplies a diagnostic representation that helps identify the object and important state. Both must return strings. A repr need not always be executable code, but should avoid concealing the state relevant to debugging.

Do not expose credentials in either representation. These methods can be called implicitly by containers, logs, debuggers, or exceptions. A convenient representation can therefore become an unexpected data leak if it includes secrets.

## 3. Implement only meaningful protocols

A collection-like object can implement `__len__` when its count has a clear meaning. Dunder methods connect an object to existing operations; they do not make every operator appropriate for every model.

For equality with an unsupported other type, returning NotImplemented allows Python's comparison machinery to try the corresponding fallback. This sentinel differs from raising NotImplementedError. Avoid implementing equality casually when identity and value semantics have not been decided.

## 4. Keep properties cheap and unsurprising

Callers usually expect reading an attribute to be inexpensive and free of major side effects. A property that performs a network request or saves a file can violate that expectation. Use an explicit method for an operation whose cost or effect should be visible.

Properties can preserve a public interface when internal representation changes. They are not a requirement to wrap every field. Introduce one when access needs a rule or computed value, and document the exceptions assignment can raise.

References: [Data model](https://docs.python.org/3.13/reference/datamodel.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether assigning a negative amount changes the previous valid backing value.
2. **Explain:** Explain why a property setter needs a different backing attribute name.
3. **Modify:** Add a concise diagnostic repr without unrelated state.
4. **Debug:** Repair a setter that calls itself recursively.

<details>
<summary>Hints</summary>

Validate first, then assign the backing field.

</details>

## Independent task: properties & object representations

In `Practice/05_Properties_And_Object_Representations.py`, complete this task:

Implement Budget with a validated nonnegative plain-integer amount property and `__str__` returning `PHP <amount>`. Start at 500, print the object, attempt assignment of -1 and print Rejected for ValueError, then print the object again. The last amount must still be 500.

Expected output:

```text
PHP 500
Rejected
PHP 500
```
