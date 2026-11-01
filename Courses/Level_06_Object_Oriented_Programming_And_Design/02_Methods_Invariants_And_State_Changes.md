# Lesson 2: Methods, Invariants & State Changes

**Prerequisites:** Levels 1–5 and Lesson 1 of this level. **Practice file:** `Practice/02_Methods_Invariants_And_State_Changes.py`.

Keep an object valid before and after every public operation. A method is a state transition whose accepted inputs, returned result, and failure effects should be explicit.

## 1. State an invariant

An invariant is a rule that should remain true whenever callers observe the object. For an account, a nonnegative whole-unit balance is one possible invariant. A withdrawal must reject an invalid amount or an overdraft before changing that balance.

```python
class Account:
    def __init__(self, balance):
        if type(balance) is not int or balance < 0:
            raise ValueError("Invalid balance")
        self.balance = balance

    def withdraw(self, amount):
        if type(amount) is not int or amount <= 0 or amount > self.balance:
            raise ValueError("Invalid withdrawal")
        self.balance -= amount
        return self.balance
```

`-=` updates the current attribute by subtracting the supplied value. It is concise, but the validation order remains the important part. If a rejected operation had already deducted an amount, catching its exception would not undo that mutation automatically.

## 2. Expose intended operations

A method name such as withdraw describes a valid operation on the model. Directly assigning an arbitrary balance can bypass its invariant, so callers should use the documented interface. A leading underscore signals an implementation detail; Python does not turn that convention into enforced privacy.

Double-underscore names trigger name mangling to reduce accidental collisions in subclasses. They do not provide a security boundary against a determined caller. Use access conventions to communicate API design rather than claim secret storage.

## 3. Protect snapshots from external mutation

A method returning an internal list gives the caller the same mutable object. Return an appropriate copy when the contract promises a snapshot. An outer copy still shares nested mutable objects, so either copy those records too or use immutable records when that fits.

A snapshot should describe one point in time. It should not be called a snapshot if later internal changes unexpectedly alter it. State these effects in the method docstring so callers can rely on them.

## 4. Separate state and presentation

Methods that change balances should return useful results or raise documented errors; they need not print user messages. A caller can convert those outcomes into a terminal report, API response, or log. This keeps the object model reusable and makes rejection behavior easier to test.

Test the unchanged state after a failed operation, not merely that an exception occurred. A failing operation that corrupts the model can be more damaging than one that returns a wrong display string.

References: [Python classes](https://docs.python.org/3.13/tutorial/classes.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Trace the balance before and after an overdraft attempt.
2. **Explain:** Explain why catching an exception does not automatically roll back earlier mutations.
3. **Modify:** Return a copy of a history list and change it outside the object.
4. **Debug:** Move an attribute update after all rejection checks.

<details>
<summary>Hints</summary>

Validate both the amount and its relationship to current state before assignment.

</details>

## Independent task: methods, invariants & state changes

In `Practice/02_Methods_Invariants_And_State_Changes.py`, complete this task:

Define `Account(balance)` requiring a nonnegative plain-integer starting balance. Define `withdraw(amount)` requiring a positive plain integer no greater than the current balance. Raise ValueError before changing state for any invalid value; otherwise subtract the amount and return the new balance. Start at 100, withdraw 30, then attempt to withdraw 80. Print the balance after success, `Rejected` for ValueError, and the actual balance afterward. A rejected withdrawal must leave state unchanged.

Expected output:

```text
70
Rejected
70
```
