# Lesson 5: Numbers & Operators

**Prerequisites:** Lessons 1–4. **Save your work:** `Practice/05_budget_split.py`.

A calculation starts with a relationship between quantities. Python operators let you express that relationship, but choosing an operator is only part of the task. You also need to identify the units, group operations correctly, and decide what a fractional result or remainder means in the problem.

## 1. Expressions produce values

```python
daily_transport = 40
study_days = 5
weekly_transport = daily_transport * study_days
print(weekly_transport)  # 200
```

The expression on the right of the last assignment multiplies the current values of two variables. Python evaluates that expression first, then assigns the result to `weekly_transport`. The name describes the resulting quantity: pesos per day multiplied by days gives pesos for the week.

Writing a formula next to the code helps reveal mistakes. Multiplying a daily cost by a number of days is meaningful; multiplying it by an unrelated budget simply because both values are numbers may run successfully while representing the wrong relationship.

## 2. The arithmetic operators

| Operator | Meaning | Example and result |
| --- | --- | --- |
| `+` | Addition | `12 + 3` gives `15` |
| `-` | Subtraction | `12 - 3` gives `9` |
| `*` | Multiplication | `12 * 3` gives `36` |
| `/` | Division | `12 / 3` gives `4.0` |
| `//` | Floor division | `14 // 3` gives `4` |
| `%` | Remainder | `14 % 3` gives `2` |
| `**` | Exponentiation | `3 ** 2` gives `9` |

For the ordinary integer and float values used here, `/` produces a float even when the division comes out evenly. `//` applied to two integers produces an integer quotient rounded downward. The `%` operator supplies the corresponding remainder.

Do not use `^` for a power. Python assigns that symbol a different operation that is outside this level. Use `**` when you mean exponentiation.

## 3. Division answers different questions

```python
budget = 503
people = 4
average_share = budget / people
whole_share = budget // people
leftover = budget % people

print(average_share)  # 125.75
print(whole_share)    # 125
print(leftover)       # 3
```

An average share answers “how much would each person receive if fractions were allowed?” A whole share answers “how many complete units can everyone receive equally?” The remainder answers “how many units are still unallocated after that whole-unit distribution?”

For nonnegative integers, the relationship can be checked by rebuilding the original amount:

```python
budget = 503
people = 4
whole_share = budget // people
leftover = budget % people
print(whole_share * people + leftover)  # 503
```

The remainder has not vanished. If your program displays only the whole share, the user may assume all money was distributed when it was not. A correct report can show both the share and the unallocated amount.

The word *floor* matters for negative values: `-7 // 3` is `-3`, because rounding downward moves toward negative infinity. This level's equal-split inputs are nonnegative, so you will not need negative floor division in the task.

## 4. Group operations to match the intended formula

```python
transport = 40
food = 100
days = 5

correct_total = (transport + food) * days
different_total = transport + food * days
print(correct_total)    # 700
print(different_total)  # 540
```

Multiplication and division take precedence over addition and subtraction. Without parentheses, the second expression multiplies only food by days, then adds one day's transport. Parentheses make the daily combined cost a single grouped expression before multiplication.

For the common operations at this level, evaluate parentheses first, then powers, then multiplication/division/floor division/remainder, then addition/subtraction. Operations at the multiplication level and at the addition level generally proceed left to right. Exponentiation groups differently: use explicit parentheses when combining powers rather than relying on a remembered shortcut.

Clear intermediate names can make an expression easier to inspect:

```python
transport = 40
food = 100
days = 5
daily_cost = transport + food
weekly_cost = daily_cost * days
print(weekly_cost)  # 700
```

This also lets you display `daily_cost` temporarily when investigating a wrong result.

## 5. Floating-point display and exact whole-unit totals

```python
print(0.1 + 0.2)          # 0.30000000000000004
print(round(0.1 + 0.2, 2)) # 0.3
```

Many decimal fractions are approximated in binary floating-point representation. The first result reflects that approximation. `round(value, 2)` asks for a rounded numeric result, but it does not change the general representation into exact decimal arithmetic. Lesson 7 shows how to choose decimal places for display.

For the capstone, spending inputs are integer whole pesos. Adding and multiplying those integers keeps the totals in whole pesos. Division is used for a displayed average, not to allocate fractional money back into the totals.

Never divide by zero. For `/`, `//`, and `%`, a zero divisor raises `ZeroDivisionError`. At this level, the input contract requires positive numbers of people or days. Recovering from invalid input belongs to the exceptions level; hiding a failure by inventing a zero answer would misrepresent the calculation.

Reference: [Python's numeric introduction](https://docs.python.org/3.13/tutorial/introduction.html#numbers).

## Practice: predict, explain, modify, debug

1. **Predict:** Calculate `17 / 5`, `17 // 5`, and `17 % 5` by hand, then compare the output.
2. **Explain:** Why does a remainder matter when dividing a whole-peso budget among days?
3. **Modify:** Change the combined daily-cost example to 6 days. Calculate the new result before running it.
4. **Debug:** A weekly transport-and-food total uses `transport + food * days`. Explain which part is multiplied and correct the grouping when both costs occur daily.

<details>
<summary>Hints</summary>

Separate the fractional average, complete units, and unallocated units. Write the problem's formula in words, then group the matching expression. Use intermediate variables when the formula becomes hard to read.

</details>

## Independent task: whole-peso budget split

In `Practice/05_budget_split.py`, use `budget = 503` and `people = 4`.

Calculate and store:

- `whole_share`: the equal whole-peso amount each person receives.
- `leftover`: the amount left after that equal distribution.
- `reconstructed_total`: the original budget rebuilt from the share, number of people, and leftover amount.

Print those three calculated values, one per line. Do not hardcode the answers.

Expected output:

```text
125
3
503
```
