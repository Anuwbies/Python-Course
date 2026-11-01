# Lesson 6: Standard Library & Reusable Interfaces

**Prerequisites:** Levels 1–2 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Standard_Library_And_Reusable_Interfaces.py`.

Use existing library functions without hiding their assumptions. The standard library extends the language with reusable operations; your responsibility is to choose the appropriate function and give it a stable interface.

## 1. Find a module for the operation

An import makes a library module available; it does not install a package from the internet. Modules such as math and statistics ship with Python. Third-party dependency installation is a separate development skill introduced in Level 5.

```python
from statistics import mean

amounts = [10, 20, 30]
print(f"Average: {mean(amounts):.2f}")
```

`mean` calculates an arithmetic average. It requires data: an empty sequence has no mean under this API and raises an error. A wrapper can deliberately define an empty-input result while preserving the library's behavior for populated data.

## 2. Put assumptions at the boundary

A function that accepts a collection of numeric amounts should not ask for terminal input internally. Let its caller decide where the data comes from. When the same helper later receives file data, its interface can remain unchanged.

```python
from statistics import mean

def average_or_none(amounts):
    if not amounts:
        return None
    return mean(amounts)

print(average_or_none([]))  # None
```

Here None means no average, rather than claiming an empty list has an average of zero. Another problem could intentionally choose zero, but that would be a different documented contract. Libraries do not remove the need to make those domain choices.

## 3. Separate computation, formatting, and orchestration

A calculation helper returns numeric values. A formatting helper can return a string; `"\n".join(lines)` combines a list of strings using newline separators. A launcher decides when to print that string or save it.

This separation is useful even without sophisticated architecture. One helper can be called by several launchers, and a display change need not alter the underlying calculation. Too many tiny modules can also add friction; split where a responsibility is reusable or independently understandable.

## 4. Inspect documentation with a concrete question

Look for accepted input types, empty-input behavior, returned values, exceptions, and version notes. A function's name alone does not establish its complete behavior. Experiment with one normal and one boundary case before building a larger interface around it.

For floating-point results, exact equality may not express the intended numeric tolerance. The standard library's math.isclose can express a relative/absolute closeness rule when needed. Integer whole-peso totals remain exact in this level, so do not add approximate comparisons to those totals unnecessarily.

References: [Statistics module](https://docs.python.org/3.13/library/statistics.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict average_or_none for an empty list and a one-element list.
2. **Explain:** Explain why no average and a zero average are different results.
3. **Modify:** Return a formatted string from one helper while leaving printing to the launcher.
4. **Debug:** Identify a wrapper that accidentally reads input on every calculation call.

<details>
<summary>Hints</summary>

Guard the empty case before calling the library function.

</details>

## Independent task: standard library & reusable interfaces

In `Practice/06_Standard_Library_And_Reusable_Interfaces.py`, complete this task:

Import `mean` from statistics. Define `average_or_none(amounts)` to return None for an empty list and the arithmetic mean otherwise. Print the average of `[10, 20, 30]` with two decimal places, then print the result for `[]`. Do not modify the input.

Expected output:

```text
20.00
None
```
