# Lesson 3: Variables, Assignment & Names

**Prerequisites:** Lessons 1–2. **Save your work:** `Practice/03_assignment_trace.py`.

A program becomes easier to change when its values have meaningful names. Instead of repeating the same literal in several statements, you can assign it to a variable and use that name where the value is needed. The important skill is tracking what each name refers to at each point in the program.

## 1. Assignment gives a value a name

```python
learner_name = "Mika"
weekly_budget = 500
print(learner_name)
print(weekly_budget)
```

The right side of `=` supplies a value. The left side identifies the name to bind to that value. Once the assignment executes, Python can look up the name in later statements. The assignment itself does not display anything; the `print()` calls produce the visible output.

Read `weekly_budget = 500` as “assign 500 to weekly_budget.” It is an instruction to update a name, not a mathematical statement claiming that two sides are permanently equal. Comparison is a separate operation introduced in Level 2.

Writing a name inside quotes changes its meaning:

```python
learner_name = "Mika"
print(learner_name)    # Mika
print("learner_name") # learner_name
```

The first call looks up a variable. The second displays the literal text between the quotes. Python does not replace words inside an ordinary string just because they match variable names.

## 2. Statements execute in order

Python must reach an assignment before that name can be used. A line that tries to display `weekly_budget` before it has been assigned raises `NameError` in an otherwise empty script.

This means that source order affects behavior. Moving an assignment below the statement that needs it can break a program, even though both lines look correct when read separately.

Use a trace table when a sequence is confusing. Walk down the statements one at a time and record the current value of each name. Do not jump to the final value and assume earlier statements used it.

## 3. Reassignment changes a binding

```python
weekly_budget = 500
saved_budget = weekly_budget
weekly_budget = 650
print(saved_budget)   # 500
print(weekly_budget)  # 650
```

When the second statement runs, `weekly_budget` currently refers to the integer value 500. `saved_budget` is assigned that current value. Reassigning `weekly_budget` later does not turn the earlier assignment into a live formula or an automatic link that follows future changes.

| After statement | `weekly_budget` | `saved_budget` |
| --- | --- | --- |
| `weekly_budget = 500` | 500 | Not assigned |
| `saved_budget = weekly_budget` | 500 | 500 |
| `weekly_budget = 650` | 650 | 500 |

This example uses integers. Later, when you work with mutable collections such as lists, changing a shared object is different from reassigning one of its names. You do not need memory addresses or interpreter internals to understand this integer example.

## 4. Choose names that explain meaning

A useful name describes what the value means in the problem. `weekly_budget` communicates more than `x`. `transport_cost` is clearer than `cost2` when there are several kinds of spending.

For the course, use lowercase words separated by underscores: **snake_case**. Names are case-sensitive, so `budget`, `Budget`, and `BUDGET` are different names. A variable may contain letters, digits, and underscores, but must not begin with a digit. Python allows additional Unicode identifiers; simple descriptive names make these beginner exercises easier to share and read.

| Name | Suitable? | Reason |
| --- | --- | --- |
| `weekly_budget` | Yes | Descriptive and consistent |
| `budget_2026` | Yes | A digit can appear after the first character |
| `2026_budget` | No | Begins with a digit |
| `weekly-budget` | No | A hyphen is interpreted as an operator |
| `class` | No | Reserved Python keyword |

Avoid assigning your own values to names such as `print`, `type`, `int`, or `input`. These are built-in names rather than reserved keywords, so Python permits reassignment, but doing so can hide the operations you intend to call later.

## 5. Keep related values together in the source

For small scripts, place the named inputs near the top, calculations after them, and display statements after the calculations. At this stage there may be no calculation yet, but the same organization will carry forward to the capstone.

```python
# Values describing this study session.
learner_name = "Mika"
course_name = "Python Foundations"
study_status = "Started"

# Display the current values.
print("Learner:", learner_name)
print("Course:", course_name)
print("Status:", study_status)
```

The labels are literal text; the second argument in each call is a variable lookup. Separating these roles lets you change the learner's name once rather than editing every output statement.

## Practice: predict, explain, modify, debug

1. **Predict:** In section 3, write the output before running it. Then change the final reassignment to 700 and predict which output line changes.
2. **Explain:** Why does `print("weekly_budget")` display a word rather than a number?
3. **Modify:** Change section 5 to describe your own study session. Keep labels as literal text and information as named values.
4. **Debug:** A program assigns `weekly_budget = 500` and later prints `weekly_Budget`. Identify the precise mismatch and its likely error.

<details>
<summary>Hints</summary>

Trace assignments in order. Variable names are case-sensitive. The second assignment in section 3 captures the value available at that moment, not a future calculation.

</details>

## Independent task: assignment trace

In `Practice/03_assignment_trace.py`:

1. Assign `"Mika"` to `learner_name`.
2. Assign `500` to `budget`.
3. Assign the current value of `budget` to `saved_budget`.
4. Reassign `budget` to `650`.
5. Print `learner_name`, `saved_budget`, and `budget`, one per line, using the variables.

Expected output:

```text
Mika
500
650
```
