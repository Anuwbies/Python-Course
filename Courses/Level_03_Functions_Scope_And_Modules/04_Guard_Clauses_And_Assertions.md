# Lesson 4: Guard Clauses & Assertions

**Prerequisites:** Levels 1–2 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Guard_Clauses_And_Assertions.py`.

Define rejection behavior instead of letting an invalid limit accidentally reach arithmetic. Use small assertions to make your expectations executable while keeping validation part of ordinary program logic.

## 1. Reject before the risky operation

A guard clause is an early return for a case that should not proceed. In this lesson a function returns None when numeric limits are invalid, while zero remains a legitimate computed result.

```python
def allowance(budget, days):
    if budget < 0 or days <= 0:
        return None
    return budget // days

print(allowance(0, 5))    # 0
print(allowance(500, 0))  # None
```

Checking days after division would be too late. The guard also gives the caller an explicit contract: numeric rejection is represented by None, not a fake allowance of zero. Other input types remain outside this example's contract; conditions about numeric ranges are not a complete type-validation system.

## 2. Recognize a failed expectation

`assert condition` stops with AssertionError when the condition is false. When it is true, execution continues without printing anything. An assertion can express a known result directly.

```python
def double(amount):
    return amount * 2

assert double(7) == 14
assert double(0) == 0
print("Examples passed")
```

A passing example establishes that particular behavior; it does not prove all inputs correct. Normal, boundary, and rejection cases answer different questions. A zero budget and zero days are not interchangeable boundaries: the first is valid here and the second is rejected.

## 3. Keep validation outside assertions

Python can disable assertions with its optimization option. Conditions and explicit rejection behavior must therefore carry the actual input contract; assertions are for development expectations, not required runtime enforcement or access control.

An assert whose expression has a necessary side effect is also fragile. Call the operation normally, save its result if useful, and assert about the result. Tests should not be the only reason an application performs required work.

## 4. Diagnose the first discrepancy

When an assertion fails, identify the actual result, expected result, and smallest input that reproduces the difference. Check the contract before changing the code. If an empty collection has no documented meaning, first decide that meaning rather than changing the assertion to whatever happened.

A small table of cases is often easier to reason about than many nearly identical examples. Dedicated test organization arrives in Level 5; for now, a few assertions beside a demonstration are enough to make the reasoning concrete.

References: [Assert statement](https://docs.python.org/3.13/reference/simple_stmts.html#the-assert-statement).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which allowance call returns zero and which returns None.
2. **Explain:** Explain why assert should not enforce required input validation.
3. **Modify:** Add a boundary case where reserve consumes the entire budget.
4. **Debug:** Fix a guard placed after the division it is meant to protect.

<details>
<summary>Hints</summary>

Check invalid limits before computing; use is None for the rejection result.

</details>

## Independent task: guard clauses & assertions

In `Practice/04_Guard_Clauses_And_Assertions.py`, complete this task:

Define `daily_allowance(budget, days=5, reserve=0)`. Accept integer inputs. Return None for a negative budget or reserve, reserve greater than budget, or nonpositive days. Otherwise return the whole-unit daily share after reserve. Add assertions for `(500) -> 100`, `(100, reserve=100) -> 0`, `(100, days=0) -> None`, and `(100, reserve=101) -> None`. Print `Allowance examples passed` afterward.

Expected output:

```text
Allowance examples passed
```
