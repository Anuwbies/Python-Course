# Lesson 1: Comparisons & Boolean Logic

**Prerequisites:** Level 1. **Practice file:** `Practice/01_Comparisons_And_Boolean_Logic.py`.

Use a condition to describe a rule precisely before you use it to choose an action. A condition is an expression that produces a Boolean result; it does not itself change which line runs.

## 1. Compare values, not variable names

`==` compares values for equality. It is different from `=`, which assigns a value to a name. The other ordinary comparisons are `!=`, `<`, `<=`, `>`, and `>=`. Their boundaries matter: a minimum age of 18 includes 18, so it needs `>=`, not `>`.

```python
age = 18
minimum_age = 18
print(age == minimum_age)  # True
print(age > minimum_age)   # False
print(age >= minimum_age)  # True
```

Each expression looks up the values available at that point. A comparison result can be stored under a descriptive name, such as `meets_minimum`, and displayed just like any other Boolean. Comparing numeric-looking strings does not turn them into numbers; convert input deliberately before comparing numeric quantities.

## 2. Combine requirements

`and` expresses that both conditions must hold. `or` expresses that at least one must hold. `not` reverses a truth value. Write the requirements in plain language before translating them so an inclusive alternative does not accidentally become a requirement to satisfy both choices.

```python
age = 18
has_ticket = True
may_enter = age >= 18 and has_ticket
needs_ticket = not has_ticket
print(may_enter)     # True
print(needs_ticket)  # False
```

Python short-circuits these operators: when the first operand determines an `and` or `or` result, the second is not evaluated. In general these operators can return operands rather than literal Booleans; in this lesson both operands are Boolean conditions, making the result Boolean as well. Parentheses make the grouping of a mixed condition explicit.

## 3. Trace boundaries systematically

For a rule accepting ages from 18 through 65, use `18 <= age <= 65`. This chained comparison requires both boundaries to hold. A useful manual investigation includes 17, 18, 65, and 66, because examples far from the boundary can hide an incorrect operator.

| Age | At least 18 | At most 65 | Accepted range |
| --- | --- | --- | --- |
| 17 | False | True | False |
| 18 | True | True | True |
| 65 | True | True | True |
| 66 | True | False | False |

## 4. Avoid misleading conversions

The string `"False"` is nonempty, so `bool("False")` is True. That operation tests truthiness, not the spelling's intended meaning. Compare an external answer with an explicit accepted value when interpreting a yes/no response. A variable named `is_approved` should hold the rule's actual result, not a convenient-looking label.

For now, print the resulting conditions. The next lesson uses those results to select a branch. This separates deciding what a rule means from deciding which action to execute.

References: [Python control flow](https://docs.python.org/3.13/tutorial/controlflow.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the results for ages 17, 18, and 19 with the ticket flag unchanged.
2. **Explain:** Explain why assignment and equality need different operators.
3. **Modify:** Change the accepted age interval and write the two boundary examples first.
4. **Debug:** Correct a rule that uses or when both age and ticket are required.

<details>
<summary>Hints</summary>

Translate both/either into and/or, then evaluate each operand before combining it.

</details>

## Independent task: comparisons & boolean logic

In `Practice/01_Comparisons_And_Boolean_Logic.py`, complete this task:

Use `age = 18`, `has_ticket = True`, and `is_staff = False`.
Calculate and print, in order: whether age is at least 18; whether both the age requirement and ticket hold; whether either staff status or ticket ownership holds. Print Boolean results, not fixed text.

Expected output:

```text
True
True
True
```
