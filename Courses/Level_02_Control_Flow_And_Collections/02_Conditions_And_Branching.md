# Lesson 2: Conditions & Branching

**Prerequisites:** Level 1 and Lesson 1 of this level. **Practice file:** `Practice/02_Conditions_And_Branching.py`.

Use a Boolean expression to select which statements execute. The important skill is making branches mutually appropriate and understanding the path taken for every boundary.

## 1. Follow a branch

An `if` statement evaluates its condition. If that result is truthy, Python executes its indented body. An `else` body executes when the condition is false. The colon starts a block; consistent indentation determines which statements belong to it.

```python
balance = -20
if balance < 0:
    print("Over budget")
else:
    print("Within budget")
print("Report complete")
```

The final print is outside both branches, so it executes after either path. Indenting it under `else` would change the behavior: an overspending report would omit the completion line. Indentation is part of Python's syntax, not simply decoration.

## 2. Order several cases deliberately

`elif` adds another condition that is tested only when the preceding branches were not selected. A single `if`/`elif`/`else` chain chooses at most one body. Two separate `if` statements are independent and can both run.

```python
balance = 0
if balance < 0:
    status = "Over budget"
elif balance == 0:
    status = "Exactly used"
else:
    status = "Money remaining"
print(status)
```

Trace the values -1, 0, and 1. These form three nonoverlapping cases. For threshold discounts, test the highest threshold first; otherwise a broad low-threshold condition can capture a value before the higher discount is considered.

## 3. Keep input assumptions visible

For numeric input, conversion still happens before comparison. Without exception handling, text such as `five` cannot be safely interpreted by copying more branches around an `int()` call. At this stage, assume valid numeric text and use conditions to check numeric ranges after conversion.

A combined condition such as `amount >= 0 and days > 0` expresses numeric admissibility. A branch can display a rejection message for invalid limits without performing a division. This is different from replacing a bad calculation with an invented successful result.

## 4. Separate the rule and the report

Store an appropriate result inside each branch, then display the result afterward when the formatting is shared. This prevents labels and calculations from being duplicated across several bodies. Conversely, a branch that needs to perform a distinct action can keep that action in its own body.

When debugging, write a small path table: input value, conditions evaluated, body selected, result produced. If two messages appear unexpectedly, inspect whether you used independent `if` statements. If no message appears, inspect whether the intended cases cover the full allowed range.

## Truthiness in a branch

A condition can use a value directly. Numeric zero and empty text are false in a condition; nonzero numbers and nonempty text are true. Thus `if name.strip():` selects a nonblank name, while `if not name.strip():` selects a blank one. The text `"0"` is nonempty and therefore true even though the number `0` is false. Keep conversion separate from this decision. The same empty/nonempty rule will apply to the collections introduced below.

References: [Python control flow](https://docs.python.org/3.13/tutorial/controlflow.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which body handles balances -1, 0, and 1.
2. **Explain:** Explain why two independent if statements can both execute.
3. **Modify:** Add a separate zero-balance label without changing the negative case.
4. **Debug:** Fix a discount chain where a broad low threshold hides the highest tier.

<details>
<summary>Hints</summary>

Include exactly 1000 in the free-shipping branch and calculate the final total after choosing shipping.

</details>

## Independent task: conditions & branching

In `Practice/02_Conditions_And_Branching.py`, complete this task:

Use `subtotal = 1200`. Shipping costs 0 when the subtotal is at least 1000; otherwise shipping costs 80. Calculate the shipping and final total using a condition. Display exactly the two labeled lines below.

Expected output:

```text
Shipping: PHP 0
Total: PHP 1200
```
