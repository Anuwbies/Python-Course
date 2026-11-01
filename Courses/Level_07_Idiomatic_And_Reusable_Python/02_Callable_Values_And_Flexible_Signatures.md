# Lesson 2: Callable Values & Flexible Signatures

**Prerequisites:** Levels 1–6 and Lesson 1 of this level. **Practice file:** `Practice/02_Callable_Values_And_Flexible_Signatures.py`.

Pass behavior as an explicit input and use flexible signatures only where the interface truly needs them. A function is an object that can be stored, passed, and called later.

## 1. Pass a function without calling it

A name such as normalize refers to a function object; normalize(value) invokes it immediately. A higher-order function receives a callable and decides when to call it for each input value.

```python
def double(value):
    return value * 2

def transform(values, operation):
    return [operation(value) for value in values]

print(transform([1, 2], double))
```

Passing double() would call it with no argument before transform runs. The resulting error belongs to that premature call, not the intended per-element transformation. Callable annotations can describe expected argument/result types, but runtime behavior still needs a coherent contract.

## 2. Supply a sorting rule

`sorted(records, key=operation)` calls the key function to derive sortable values while returning a new ordered list. A lambda is a small anonymous function expression, such as `lambda record: record["amount"]`. It contains an expression rather than a statement body and returns that expression's value.

Use a named function when the rule needs documentation, validation, or several steps. A short lambda can make a local field-selection rule clear; a dense nested lambda often hides the very behavior the interface is meant to expose.

## 3. Collect positional and keyword arguments

A parameter written `*amounts` collects extra positional arguments into a tuple. `**options` collects extra keyword arguments into a dictionary. The names args and kwargs are conventions; the stars provide the mechanism.

At a call site, `*values` and `**mapping` expand existing collections. Missing required arguments, duplicate named values, and unexpected keywords can still raise TypeError. Flexible syntax does not mean the callee accepts arbitrary meaningful data.

## 4. Require selected options by keyword

A bare star in a signature makes following parameters keyword-only. For `def select(values, operation, *, minimum=0)`, the minimum option must be named in a call. This avoids confusing several optional numeric values with positional data.

Prefer explicit parameters for known options so misspellings are caught. An unrestricted options dictionary can accidentally accept a misspelled flag and silently ignore it. Use flexible signatures when forwarding a documented interface or accepting a genuinely variable collection of values.

References: [Function parameters](https://docs.python.org/3.13/tutorial/controlflow.html#more-on-defining-functions).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the difference between passing double and calling double before the receiving function.
2. **Explain:** Explain how a key function differs from changing the records themselves.
3. **Modify:** Rewrite a short field key as a named helper.
4. **Debug:** Find an unexpected keyword silently hidden inside an unused options dictionary.

<details>
<summary>Hints</summary>

Filter by the original value, then invoke the supplied callable.

</details>

## Independent task: callable values & flexible signatures

In `Practice/02_Callable_Values_And_Flexible_Signatures.py`, complete this task:

Define `transform_at_least(values, operation, *, minimum=0)` to return transformed values whose original numeric value is at least minimum. Preserve input order and do not mutate the source. Define double(value), then call the function for `[-1, 0, 2]` with minimum=0. Print the returned list and original list.

Expected output:

```text
[0, 4]
[-1, 0, 2]
```
