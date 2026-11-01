# Lesson 1: Comprehensions & Unpacking

**Prerequisites:** Levels 1–6. **Practice file:** `Practice/01_Comprehensions_And_Unpacking.py`.

Express a small transformation directly when doing so makes the relationship between source and result easier to read. Concision is useful only while the evaluation and effects remain understandable.

## 1. Translate a visible loop

A list comprehension creates a new list from an iterable. Read the for clause as the source of values, the optional if clause as a filter, and the leading expression as the result produced for each accepted value.

```python
amounts = [0, 10, 20]
doubled = [amount * 2 for amount in amounts if amount > 0]
print(doubled)  # [20, 40]
```

This is equivalent to an explicit loop that conditionally appends to a new list. The source list is not changed. Do not use a comprehension merely to execute print or mutate another object; an ordinary loop makes those side effects clearer.

## 2. Distinguish filtering from conditional results

A trailing if filters out elements. A conditional expression `positive if condition else negative` chooses one result value and retains one output per visited element when used as the leading expression.

```python
amounts = [-1, 0, 2]
labels = ["valid" if amount >= 0 else "invalid" for amount in amounts]
print(labels)
```

The two uses of if have different output lengths and meanings. Trace the source and selected result for each item before combining several clauses. Nested comprehensions evaluate loops in the order written; too many nested rules usually deserve a named helper.

## 3. Build dictionaries and sets

A dictionary comprehension uses a key:value expression, while a set comprehension uses a value without a colon. Duplicate dictionary keys keep the last supplied value rather than adding their numeric values. Grouped totals still require an explicit accumulation rule.

For example, `{name.strip().lower() for name in names}` builds unique normalized labels. The original spellings are not preserved in that result, so retain the source when display or audit history matters. Set order is not a report contract.

## 4. Unpack an intended shape

Sequence unpacking assigns positions to names. A starred target can collect remaining values, such as `first, *rest = values`. It requires enough values for the nonstarred targets. Dictionary unpacking with `**mapping` builds or passes named associations; later values can overwrite earlier keys during construction.

These forms do not validate a record's meaning. A record with the wrong units can unpack successfully. Keep normalization, validation, and ownership decisions explicit even when the transformation fits on one line.

## Convert iterables deliberately

`list(iterable)` materializes its values in order, and `tuple(iterable)` materializes a fixed outer sequence. `set(iterable)` retains unique members; `dict(pair_iterable)` builds key/value associations from two-element pairs. Converting a one-shot iterator consumes it. Choose a conversion because the caller needs that representation, rather than assuming every iterable can be replayed without storage.

References: [Comprehensions](https://docs.python.org/3.13/tutorial/datastructures.html#list-comprehensions).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the output length for a filter compared with a conditional expression.
2. **Explain:** Explain why duplicate dictionary keys do not automatically aggregate amounts.
3. **Modify:** Build a set of normalized labels while retaining the source list.
4. **Debug:** Replace a comprehension used only for side-effect prints with a normal loop.

<details>
<summary>Hints</summary>

Filter before producing each doubled result; sort only the displayed set values.

</details>

## Independent task: comprehensions & unpacking

In `Practice/01_Comprehensions_And_Unpacking.py`, complete this task:

Use `amounts = [0, 10, 20]` and `labels = [" FOOD ", "Travel", "food"]`. Build a new list doubling only positive amounts and a set of normalized unique labels. Print the doubled list, the sorted unique labels, and the unchanged amounts list.

Expected output:

```text
[20, 40]
['food', 'travel']
[0, 10, 20]
```
