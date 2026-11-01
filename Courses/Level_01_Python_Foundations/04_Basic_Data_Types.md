# Lesson 4: Basic Data Types

**Prerequisites:** Lessons 1–3. **Save your work:** `Practice/04_type_inspection.py`.

A value's type determines what it represents and which operations make sense for it. The characters `500` can represent a number when written as `500`, or text when written as `"500"`. They may look similar when printed, but they are different values with different behavior.

## 1. Four useful built-in types

| Type | Purpose | Examples |
| --- | --- | --- |
| `int` | Whole numbers | `5`, `0`, `-20`, `1_000` |
| `float` | Approximate numeric values that can include a fractional part | `82.5`, `0.0`, `-1.25` |
| `str` | Text | `"Mika"`, `"500"`, `""` |
| `bool` | A true or false value | `True`, `False` |

These are four types used in this level, not the complete set of Python types. Python also has collections and other values that later levels introduce.

An underscore can separate digits in a numeric literal for readability: `1_000` represents the same integer as `1000`. It does not become part of the value displayed by `print()`.

## 2. Inspect values with `type()`

```python
learner_name = "Mika"
study_days = 5
daily_cost = 82.5
is_student = True

print(type(learner_name))
print(type(study_days))
print(type(daily_cost))
print(type(is_student))
```

The output is:

```text
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```

`type()` reports the type of the value supplied to it. The word `class` is how Python describes these types in its display; you do not need to define a class to use them. Class definitions are a later topic.

The outer `print()` displays the result produced by the inner `type()` call. Python first evaluates the inner expression, then supplies its result to the outer call. This is an early example of one operation using the result of another.

## 3. Numbers and numeric-looking text differ

```python
amount = 500
amount_text = "500"

print(amount)
print(amount_text)
print(type(amount))
print(type(amount_text))
```

Both of the first two lines display `500`. The next two lines reveal that one value is an integer and the other is a string. Printed appearance alone therefore does not identify the type.

Numbers are suited to arithmetic. Strings preserve textual information, including leading zeros and words. For example, a label such as `"007"` may be an identifier whose exact characters matter, rather than a quantity you intend to add. Do not convert every digit sequence to a number just because conversion is possible.

Type conversion in Lesson 8 lets you deliberately create a numeric value from suitable text. It does not mean Python should silently guess which interpretation you intended.

## 4. Integers and floats represent different kinds of quantities

Use an integer for a whole-number count such as a number of study days. A float is useful for measurements and calculations that involve fractions. `5` is an integer literal, while `5.0` is a float literal, even though they can describe the same numeric magnitude.

Floats represent many fractional values approximately. A displayed result such as `0.30000000000000004` can reflect this representation, rather than a typing mistake. Formatting a float changes its display; it does not turn the underlying arithmetic into exact decimal arithmetic.

For the Level 1 budget capstone, use integer whole pesos as the input amounts. You will format an average with decimal places, but the spending totals themselves remain whole-number calculations. This gives the exercise an explicit, manageable numeric model.

## 5. Booleans express a state

```python
is_student = True
is_finished = False
label = "False"

print(is_student)
print(is_finished)
print(type(label))
```

`True` and `False` are Boolean values with capital first letters. `"False"` is a string containing five characters. Quoting a Boolean's spelling changes it into text.

At this level you can store and display Boolean values. Level 2 uses them in conditions to select which statements execute. You do not need a condition to understand that a stored status and the text describing that status are distinct representations.

## 6. Values have types; names can be reassigned

```python
record = 5
print(type(record))  # int
record = "five"
print(type(record))  # str
```

Python permits the name `record` to refer to values of different types at different times. This behavior is often called dynamic typing. The integer did not transform itself into a string; the second assignment bound the name to a different value.

Although this is allowed, reusing one name for unrelated meanings makes a program harder to reason about. Prefer names that retain a clear role, such as `days_text` for raw input and `days` for its converted integer.

## Practice: predict, explain, modify, debug

1. **Predict:** Identify the types of `0`, `0.0`, `"0"`, `False`, and `"False"` before checking them.
2. **Explain:** Why can two calls display the same text while their arguments have different types?
3. **Modify:** Create four descriptively named values about a trip: a destination, a day count, a measurement, and a Boolean status. Display each type.
4. **Debug:** Someone expects `"True"` to have type `bool`. Explain the effect of the quotes and correct the value when a Boolean is intended.

<details>
<summary>Hints</summary>

A decimal point marks these float literals. Quotes mark strings even when their contents look numeric. `type()` examines the value, rather than inferring a type from the variable's name.

</details>

## Independent task: type inspection

In `Practice/04_type_inspection.py`, create these four variables:

- `learner_name` with the value `"Mika"`.
- `study_days` with the value `5`.
- `daily_cost` with the value `82.5`.
- `is_student` with the value `True`.

Use `type()` and `print()` to display the type of each value in that order. Do not print hardcoded type descriptions.

Expected output:

```text
<class 'str'>
<class 'int'>
<class 'float'>
<class 'bool'>
```
