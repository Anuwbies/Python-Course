# Lesson 7: Formatted Output

**Prerequisites:** Lessons 1–6. **Save your work:** `Practice/07_cost_report.py`.

A calculation and its presentation are different responsibilities, even inside a short script. The numeric result should remain usable for later arithmetic; the display should give the reader enough context to interpret it. Formatted strings help you combine labels, values, and readable numeric formatting without manually converting every piece.

## 1. Put values into text with f-strings

```python
learner_name = "Mika"
days = 5

print(f"Learner: {learner_name}")
print(f"Days: {days}")
```

The `f` immediately before the opening quote marks a **formatted string literal**, usually called an f-string. Inside it, braces mark an expression that Python should evaluate and insert into the resulting text.

`Learner: ` remains literal text. `learner_name` inside braces is a variable lookup. The braces themselves are not displayed. A missing `f` leaves an ordinary string, so `"Learner: {learner_name}"` displays the braces and name literally.

An f-string produces a string value. `print()` then displays that string. You could also save the formatted result in a variable before displaying it.

## 2. Keep arithmetic understandable

```python
daily_cost = 82.5
days = 5
total_cost = daily_cost * days
report_line = f"Total cost: PHP {total_cost}"

print(report_line)  # Total cost: PHP 412.5
```

Expressions inside braces can contain arithmetic, such as `{daily_cost * days}`. For a report with several related values, named intermediate results often make the source easier to inspect. They also avoid hiding a complicated formula inside a long display statement.

The label `PHP` is ordinary text identifying the currency. It does not change the number's type or apply a currency-specific rounding policy. Units and assumptions still need to be chosen by the program's author.

## 3. Choose decimal places for display

```python
daily_cost = 82.5
days = 5
total_cost = daily_cost * days

print(f"Daily cost: PHP {daily_cost:.2f}")
print(f"Total cost: PHP {total_cost:.2f}")
print(total_cost)  # Still the numeric value 412.5
```

The colon introduces a formatting specification. `.2f` asks for a fixed-point display with two digits after the decimal point. This gives `82.50` and `412.50` in the formatted lines. It does not reassign either numeric variable.

Formatting rounds the displayed representation to the requested precision. It cannot repair an incorrect formula, and it does not make binary floating-point arithmetic exact. If the unformatted result is wrong because a daily expense was counted only once, adding `.2f` merely presents the wrong result neatly.

Separate a displayed average from an actual allocation rule. Showing `333.33` as an average does not explain where an unallocated cent or whole peso went. For the Level 1 capstone, the exact whole-peso split and remainder are reported separately.

## 4. Group large numbers when useful

```python
annual_budget = 1250000
average_cost = 1250.5

print(f"Annual budget: PHP {annual_budget:,}")
print(f"Average cost: PHP {average_cost:,.2f}")
```

The comma groups thousands in this formatting style. Combining it with `.2f` displays a grouped number with two decimal places. These are presentation choices, not extra digits stored in the original number.

This course uses explicit labels and modest formatting. You do not need column alignment, nested format specifications, or decorative terminal output to complete this level. A concise report with correct values is easier to review than a large banner hiding the calculation.

## 5. Make a report reflect the actual variables

```python
learner_name = "Mika"
daily_cost = 82.5
days = 5
total_cost = daily_cost * days

print(f"Learner: {learner_name}")
print(f"Daily cost: PHP {daily_cost:.2f}")
print(f"Days: {days}")
print(f"Total cost: PHP {total_cost:.2f}")
```

The report should change when the source values change. A program that always prints `Total cost: PHP 412.50` as a literal can match one example while failing every other case. Keeping the calculation in `total_cost` and referencing it in the f-string connects the display to the program's actual state.

Read the source in three parts: inputs, calculation, report. This organization is enough for a small straight-line script. Later levels will split the same responsibilities into functions and modules.

Reference: [Python's formatted string literals](https://docs.python.org/3.13/tutorial/inputoutput.html#formatted-string-literals).

## Practice: predict, explain, modify, debug

1. **Predict:** What does `f"Value: {5:.2f}"` display? What happens to braces in an ordinary string without the `f` prefix?
2. **Explain:** Does displaying a value with `.2f` change the variable used in later calculations?
3. **Modify:** Add a whole-number weekly budget to the report and display it with a thousands separator. Keep its numeric value available.
4. **Debug:** A script prints `"Days: {days}"` after assigning `days = 5`. Correct the formatting and explain why Python originally displayed the variable's name literally.

<details>
<summary>Hints</summary>

The prefix enables brace expressions. The formatting specification follows a colon inside the same braces. Check the calculation before changing the display format.

</details>

## Independent task: cost report

In `Practice/07_cost_report.py`, use `learner_name = "Mika"`, `daily_cost = 82.5`, and `days = 5`.

Calculate `total_cost` from the daily cost and number of days. Use f-strings to display the report below, formatting the daily and total costs with two decimal places. Keep the calculation variables numeric.

Expected output:

```text
Learner: Mika
Daily cost: PHP 82.50
Days: 5
Total cost: PHP 412.50
```
