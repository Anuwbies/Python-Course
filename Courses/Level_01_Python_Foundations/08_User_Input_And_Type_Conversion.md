# Lesson 8: User Input & Type Conversion

**Prerequisites:** Lessons 1–7. **Save your work:** `Practice/08_input_converter.py`.

Until now, changing a calculation required editing its source values. Input makes a script interactive: the user supplies those values while the program is running. The key boundary is that terminal input arrives as text, even when the user types digits. Your program must convert suitable text before using it as a numeric quantity.

## 1. Read a line with `input()`

```python
print("Name:")
name = input()
print(f"Hello, {name}.")
```

When the interpreter reaches `input()`, it waits for a line of text. The user types their response and presses Enter. Python returns that line as a string, without the line-ending Enter produced, and the assignment saves it in `name`.

This course often uses a separate `print()` for a prompt. That makes it clear which statement displays the question and which reads the response. The shorter form `input("Name: ")` also displays a prompt, but does not add a newline after that prompt. Both forms return a string.

Input is read in source order. If a program has three calls to `input()`, it needs three responses. The name of the variable does not tell Python where to fetch a value; the next input line is what the next call receives.

## 2. Numeric-looking input is still text

```python
print("Study days:")
days_text = input()
print(type(days_text))
print(days_text + days_text)
```

If you enter `5`, the type is `str`, and the last line displays `55`. That is string concatenation, not addition of the numbers five and five. Python is applying the operation appropriate for the values it actually received.

A common debugging mistake is to inspect only printed values and assume they are numeric. Use your knowledge of where the data came from, and temporarily display its type when necessary.

## 3. Convert only when the meaning requires it

```python
print("Study days:")
days_text = input()
days = int(days_text)
print(days + days)
```

`int()` creates an integer from suitable text. Entering `5` now leads to the numeric result `10`. The original string and the new integer can be kept under separate names so their roles are clear.

Once you understand those steps, `days = int(input())` combines the read and conversion in one expression. Python evaluates the inner `input()` first, then passes its returned string to `int()`, then assigns the integer result.

| Operation | Example | Result or behavior |
| --- | --- | --- |
| `int(text)` | `int("5")` | Integer `5` |
| `float(text)` | `float("82.5")` | Float `82.5` |
| `str(value)` | `str(5)` | String `"5"` |
| `int(text)` with decimal-point text | `int("5.0")` | Raises `ValueError` |

Do not convert a decimal string through `float()` and then `int()` merely to avoid an error. `int(5.9)` truncates toward zero and produces `5`, which discards information. Choose the accepted input format deliberately: this level's whole-peso tasks require integer text.

## 4. Clean text without guessing its meaning

```python
print("Name:")
name = input().strip()
print("Daily measurement:")
measurement = float(input())

print(f"Name: {name}")
print(f"Measurement: {measurement:.2f}")
```

The expression `input().strip()` first reads a string, then calls `.strip()` on that returned string. It removes surrounding whitespace while preserving meaningful internal spaces. Save the result because the cleanup produces a new string.

Python's integer conversion accepts surrounding whitespace in otherwise valid integer text, so you do not need `.strip()` just to convert an ordinary numeric response. For names and labels, cleanup is a separate choice about how text should be stored and displayed.

Avoid using `bool(input())` to interpret a yes/no response. A nonempty string such as `"False"` becomes `True` when converted with `bool()`. That conversion asks whether the string is empty, not whether its spelling means yes or no. Deciding among textual answers requires conditions, which are taught in Level 2.

## 5. State the accepted inputs before calculating

For the independent task, the name must contain meaningful text, days must be a positive integer, and the budget must be a nonnegative whole-peso integer. These are the **input assumptions** of the task.

The script can read and calculate under those assumptions without pretending to handle every possible response. If a user enters `five`, `int()` raises `ValueError`. If the number of days is zero, division raises `ZeroDivisionError`. The error messages are observations to understand; recovering and asking again requires later concepts.

Do not add unexplained conditions, exception handlers, or loops copied from elsewhere. A smaller program with an honest contract is more useful at this stage than a larger program you cannot explain.

## 6. Follow one response through the whole program

```python
print("Name:")
name = input().strip()
print("Days:")
days = int(input())
print("Budget (whole PHP):")
budget = int(input())

daily_budget = budget / days

print(f"Hello, {name}.")
print(f"Days: {days}")
print(f"Budget: PHP {budget}")
print(f"Daily budget: PHP {daily_budget:.2f}")
```

For responses `Mika`, `5`, and `1000`, the trace is:

| Stage | Meaning |
| --- | --- |
| Read name | The text is cleaned and saved as `"Mika"` |
| Read days | The text `"5"` is converted to integer `5` |
| Read budget | The text `"1000"` is converted to integer `1000` |
| Calculate | `1000 / 5` produces float `200.0` |
| Format | The displayed average becomes `200.00`; the calculation remains numeric |

During an interactive run, the terminal also shows what you type. The expected program output below lists what the script prints; the typed responses are provided separately.

Reference: [Python's built-in functions](https://docs.python.org/3.13/library/functions.html#input).

## Practice: predict, explain, modify, debug

1. **Predict:** If the user enters `7`, what does `input()` return, and how does adding that value to itself differ before and after integer conversion?
2. **Explain:** Describe the evaluation order in `days = int(input())`.
3. **Modify:** In a scratch file, read a whole-number count and a decimal measurement, then display their values and types. Specify valid sample responses before running it.
4. **Debug:** A script reads `budget = input()` and then tries `budget / 5`. Explain the type mismatch and where conversion belongs.

<details>
<summary>Hints</summary>

Reading text does not interpret the user's intended numeric meaning. Choose `int` for the task's whole units and `float` for accepted fractional measurements. Keep the input assumptions visible.

</details>

## Independent task: interactive daily average

In `Practice/08_input_converter.py`, write a program that:

1. Prints `Name:` and reads a name, removing surrounding whitespace.
2. Prints `Days:` and reads a positive integer number of days.
3. Prints `Budget (whole PHP):` and reads a nonnegative integer budget.
4. Converts the two numeric responses to integers and calculates the average budget per day.
5. Displays the greeting, days, budget, and daily average, with the average formatted to two decimal places.

Assume the user provides a nonempty name, positive integer days, and a nonnegative integer budget.

Sample input, one response per line:

```text
Mika
5
1000
```

Expected program output, excluding the typed responses:

```text
Name:
Days:
Budget (whole PHP):
Hello, Mika.
Days: 5
Budget: PHP 1000
Daily budget: PHP 200.00
```
