# Lesson 1: Functions, Parameters & Returns

**Prerequisites:** Levels 1–2. **Practice file:** `Practice/01_Functions_Parameters_And_Returns.py`.

Name a reusable operation, give it explicit inputs, and return a result that another part of the program can use. A function definition describes behavior; a call actually runs that behavior.

## 1. Define and then call

`def` introduces a function definition, followed by its name, parentheses, and a colon. The indented body contains the statements run for each call. Parameter names identify the inputs within that body; argument values are supplied by the caller.

```python
def double(amount):
    result = amount * 2
    return result

answer = double(7)
print(answer)  # 14
```

Defining `double` does not multiply anything immediately. The call binds amount to 7, evaluates the body, and returns 14. A later call can use a different argument without editing the definition. Names chosen inside the body should describe that one operation rather than depend on a particular caller's variable names.

## 2. Return and display are different effects

`return` ends the current function call and sends a value to its caller. `print()` sends text to output. A function that only prints a calculation implicitly returns `None`, Python's value for no meaningful result here.

```python
def show_double(amount):
    print(amount * 2)

saved = show_double(7)  # Displays 14
print(saved)           # Displays None
```

Replacing return with print can therefore break a larger calculation even when the screen appears correct. Conversely, a function whose job is displaying a report can intentionally return None. Decide the function's responsibility before writing its body.

## 3. Document the operation

A string placed first inside the function body is its docstring. It explains purpose and assumptions for a reader or documentation tool. For a small function, one accurate sentence is more useful than a long description repeating the obvious syntax.

```python
def remaining_budget(budget, spent):
    """Return whole pesos remaining, including a negative shortfall."""
    return budget - spent

print(remaining_budget(100, 120))  # -20
```

The function returns a numeric value and performs no input or output. Keeping input, calculation, and display separate lets the same calculation support a menu, a report, or later an API without asking the user a question at each call.

## 4. Stop at the intended point

Only statements reached before return execute. Returning inside an accumulation loop processes just the first element; returning after the loop processes all elements and also covers an empty collection. Trace indentation as carefully as the formula.

A function should be small enough that you can describe its task and expected result without listing unrelated actions. That does not impose a fixed line count: a short function with an unclear contract can still be difficult to reuse.

References: [Defining functions](https://docs.python.org/3.13/tutorial/controlflow.html#defining-functions).

## Practice: predict, explain, modify, debug

1. **Predict:** Trace double(7) from argument binding to the caller assignment.
2. **Explain:** Explain why a function can display 14 while saved becomes None.
3. **Modify:** Use the returned balance in a separate formatted display.
4. **Debug:** Move a total-return statement out of a loop so it includes every expense.

<details>
<summary>Hints</summary>

Initialize before the loop and return after it, including the empty case.

</details>

## Independent task: functions, parameters & returns

In `Practice/01_Functions_Parameters_And_Returns.py`, complete this task:

Define `total_expenses(amounts)` to return the total of a list of nonnegative integer amounts, without printing or changing the list. An empty list totals 0. Call it for `[120, 80, 50]` and `[]` and print those returned totals on separate lines.

Expected output:

```text
250
0
```
