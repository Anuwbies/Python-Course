# Lesson 5: Type Hints & Static Checking

**Prerequisites:** Levels 1–4 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Type_Hints_And_Static_Checking.py`.

Describe expected interfaces so readers and static tools can find inconsistencies before a path is executed. An annotation documents a contract; it does not automatically enforce input validation at runtime.

## 1. Annotate inputs and results

A parameter annotation follows a colon, and a return annotation follows an arrow. Built-in collection annotations such as list[int] describe an element type. They help a reader distinguish a list of amounts from arbitrary text.

```python
def total_amounts(amounts: list[int]) -> int:
    return sum(amounts)

print(total_amounts([10, 20]))
```

Python still executes the function normally. Passing a wrong type can fail later or sometimes appear to work; annotations do not insert conversion or guards. Keep runtime validation at untrusted input boundaries when the application requires it.

## 2. Represent a real alternative

`int | None` describes a result that can be an integer or an absence marker. A caller must consider both alternatives. A check such as `if result is None` narrows the remaining path so a static checker can understand that the later value is an integer.

Using Any everywhere removes much of the checking value. Start with concrete interfaces and introduce flexibility only where the problem needs it. A dynamic boundary can load unknown JSON, validate it, then expose a narrower internal type.

## 3. Run a checker on a bounded file

Mypy is a third-party static checker. Install it in the environment and run `python -m mypy path/to/file.py`. It inspects annotations and supported control flow without executing the program's input prompts or demonstrations.

A clean type-check result is different from passing behavioral tests. A perfectly typed subtraction can still subtract the wrong field. Conversely, a rejected annotation might reflect a genuinely unsupported path or missing library information; understand the diagnostic before adding an ignore comment.

## 4. Keep units and invariants visible

Both a budget and a number of days can have type int. An annotation cannot by itself establish that days is positive or that two integer fields use the same units. Names, documentation, guards, and tests still carry those rules.

Use type hints to reinforce a design rather than decorate every local variable unnecessarily. The function boundary is usually the best starting point. More advanced protocols and typed object models follow once classes are introduced.

## Describe dictionary interfaces as well as lists

`dict[str, int]` annotates a dictionary with string keys and integer values, while `list[int]` annotates integer elements. A function can therefore return count/total/remaining as dict[str, int] without a custom class. These annotations describe shapes, not the presence of specific required keys or whether amounts are nonnegative. Preserve those rules with the documented contract and runtime checks.

References: [Typing module](https://docs.python.org/3.13/library/typing.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which paths of an optional result need a None check.
2. **Explain:** Explain one bug a type checker can find and one it cannot.
3. **Modify:** Annotate an existing total function without changing its behavior.
4. **Debug:** Replace an unjustified ignore with a correct optional-value branch.

<details>
<summary>Hints</summary>

Describe both possible results and keep validation separate from the annotation.

</details>

## Independent task: type hints & static checking

In `Practice/05_Type_Hints_And_Static_Checking.py`, complete this task:

Define `daily_allowance(budget: int, days: int) -> int | None`, returning None for negative budget or nonpositive days and the whole-unit share otherwise. Print a valid result and an invalid result for `(500, 5)` and `(500, 0)`. Keep the guards as ordinary runtime conditions.

Expected output:

```text
100
None
```
