# Lesson 3: Scope, Mutation & Copying

**Prerequisites:** Levels 1–2 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Scope_Mutation_And_Copying.py`.

Explain which state a function can change and which result the caller must save. A local parameter name does not imply that the object it refers to is an independent copy.

## 1. Reassignment is local

Names assigned inside an ordinary function belong to that call's local scope unless declared otherwise. Passing an integer does not grant the function permission to reassign the caller's variable by name.

```python
def spend(balance, amount):
    balance = balance - amount
    return balance

balance = 500
new_balance = spend(balance, 120)
print(balance)      # 500
print(new_balance)  # 380
```

The returned result must be saved explicitly if the caller wants its own balance updated. A local variable also cannot normally be read from outside the function that created it. Use inputs and returns to expose dependencies instead of relying on changing module globals.

## 2. A shared list can be mutated

The parameter and caller can refer to the same mutable list. Calling append changes that object, while assigning a new list to the parameter changes only the local binding.

```python
def appended_copy(values, amount):
    updated = values.copy()
    updated.append(amount)
    return updated

original = [120]
updated = appended_copy(original, 80)
print(original)  # [120]
print(updated)   # [120, 80]
```

The copy makes the outer lists independent. Nested dictionaries or lists would still be shared through a shallow copy. This function only appends a new integer, so copying the outer collection is sufficient for its stated behavior.

## 3. Do not share an accidental default

A default list such as `def collect(value, values=[])` is created once when the definition runs. Omitted-argument calls can unexpectedly accumulate into that same list. Use None to mean no collection was supplied, then create a new collection in the call.

`is None` checks specifically for the absence marker. An explicitly supplied empty list is still a real list; `if not values` would conflate that valid input with omission. The same distinction applies to a valid numeric zero versus a failure result of None.

## 4. Make effects intentional

Mutation is not always wrong. An in-place function can be useful when its name and documentation promise the change. The problem is an unexpected effect that the caller cannot see from the interface.

For this course's tracker helpers, return updated values and preserve incoming collections unless the task explicitly requests mutation. That makes repeated calls easier to reason about and allows the original version to remain available for comparison.

References: [Defining functions](https://docs.python.org/3.13/tutorial/controlflow.html#defining-functions).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict original and updated after appending to an outer copy.
2. **Explain:** Explain why local reassignment differs from append on a shared object.
3. **Modify:** Allow an omitted list with a None default while retaining an explicitly supplied empty list.
4. **Debug:** Repair a default list that leaks one call's data into the next call.

<details>
<summary>Hints</summary>

The None default and the defensive copy solve two different sharing problems.

</details>

## Independent task: scope, mutation & copying

In `Practice/03_Scope_Mutation_And_Copying.py`, complete this task:

Define `add_amount(amount, amounts=None)` to return a new list with amount appended. Assume a nonnegative integer amount and a supplied list of nonnegative integers. When the list is omitted, start a fresh list on every call. Do not change a supplied list. Print `add_amount(10)`, `add_amount(20)`, the result of adding 50 to `[120, 80]`, and that original list afterward.

Expected output:

```text
[10]
[20]
[120, 80, 50]
[120, 80]
```
