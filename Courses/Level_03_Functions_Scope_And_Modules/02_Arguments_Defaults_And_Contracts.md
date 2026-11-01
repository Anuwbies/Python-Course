# Lesson 2: Arguments, Defaults & Contracts

**Prerequisites:** Levels 1–2 and Lesson 1 of this level. **Practice file:** `Practice/02_Arguments_Defaults_And_Contracts.py`.

Choose an interface that makes required values and optional choices clear. A call should communicate what the function needs without forcing the caller to know its internal variables.

## 1. Match values by position or name

Positional arguments match parameters from left to right. Keyword arguments match a parameter by its spelling, making a call clearer when several inputs have similar types. In ordinary calls, place positional arguments before keyword arguments and do not supply the same parameter twice.

```python
def weekly_cost(daily_cost, days):
    return daily_cost * days

print(weekly_cost(40, 5))
print(weekly_cost(days=5, daily_cost=40))
```

The two calls have the same result. Swapping two positional numbers may produce valid arithmetic with the wrong meaning, so keyword arguments are especially useful when parameter order is easy to forget.

## 2. Offer a meaningful default

A default is used when the caller omits that argument. Required parameters normally come before parameters with defaults.

```python
def allowance(budget, days=5):
    return budget // days

print(allowance(500))          # 100
print(allowance(500, days=10)) # 50
```

The default is part of the interface and must have a reason. A missing argument is not the same as an invalid argument: explicitly passing zero days does not request the default and would make the division invalid. A contract must state the accepted range even when it supplies a convenient default.

## 3. State more than the formula

A useful function contract describes accepted types and ranges, returned values, and side effects. For allowance, state that budget is a nonnegative integer, days is a positive integer, and the result is the whole-unit daily share. A fractional average is a different operation.

Contracts help callers and reviewers decide which examples are meaningful. They also prevent a vague instruction such as handle bad input from producing arbitrary fallback values. This lesson assumes the documented valid numeric range; a later lesson adds explicit rejection behavior.

## 4. Recognize definition-time choices

Default expressions are evaluated when the definition executes, not on every call. Immutable numeric defaults are straightforward. A mutable list used as a default can be shared between omitted-argument calls; the next lesson explains why a None default and a new list are safer for an independent collection.

For now, use explicit named parameters and simple immutable defaults. Variable-length argument syntax is reserved for Level 7, after the interface and call mechanics are well understood.

References: [Defining functions](https://docs.python.org/3.13/tutorial/controlflow.html#defining-functions).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict allowance(500) and allowance(500, days=4).
2. **Explain:** Explain how keyword arguments reduce ambiguity between similar numeric inputs.
3. **Modify:** Add a reserve parameter with default zero under a clearly stated valid-input contract.
4. **Debug:** Identify a call that gives days both positionally and by keyword.

<details>
<summary>Hints</summary>

Subtract the weekly reserve before dividing, and keep the default days unchanged.

</details>

## Independent task: arguments, defaults & contracts

In `Practice/02_Arguments_Defaults_And_Contracts.py`, complete this task:

Define `daily_allowance(budget, days=5, reserve=0)`. Inputs are nonnegative integer budget and reserve with reserve no greater than budget, and positive integer days. Return the whole-unit share of budget minus reserve divided among days. Print the results of `daily_allowance(500)` and `daily_allowance(500, days=4, reserve=100)`.

Expected output:

```text
100
100
```
