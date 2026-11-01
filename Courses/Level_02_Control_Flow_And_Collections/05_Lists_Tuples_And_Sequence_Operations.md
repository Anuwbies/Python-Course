# Lesson 5: Lists, Tuples & Sequence Operations

**Prerequisites:** Level 1 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Lists_Tuples_And_Sequence_Operations.py`.

Store an ordered group of values and choose whether that group should be changed. A sequence introduces positions, shared objects, and empty cases that a single variable could not express.

## 1. Work with ordered values

A list literal uses square brackets and comma-separated elements. Index zero identifies the first element. Negative index -1 identifies the last. A slice such as `values[1:3]` returns a new outer list containing positions one and two; the ending position is excluded.

```python
expenses = [120, 80, 50]
print(expenses[0])   # 120
print(expenses[-1])  # 50
print(expenses[1:])  # [80, 50]
```

Indexing a nonexistent position raises IndexError, while slicing can safely return fewer elements. An empty list has length zero and no first element. Use its length or truthiness in a condition before an operation that assumes data exists.

## 2. Change a list deliberately

`.append(value)` adds one element, `.remove(value)` removes the first matching element, and `.pop()` removes and returns an element. `.remove()` raises ValueError if the value is absent. An indexed assignment replaces a particular slot.

```python
expenses = [120, 80]
expenses.append(50)
expenses[0] = 100
last = expenses.pop()
print(expenses)  # [100, 80]
print(last)      # 50
```

Methods such as append modify the list and return None; assigning `expenses = expenses.append(50)` therefore loses the list binding. Keep mutation as its own statement and use a new name for a returned element when the method actually provides one.

## 3. Separate copying from aliasing

`other = expenses` makes another name refer to the same list. A mutation through either name is visible through both. `other = expenses.copy()` makes a new outer list, so appending to that new list does not append to the original.

A shallow copy does not recursively clone nested objects. Later records containing nested lists need a deliberate copying policy. For a flat list of integers, an outer copy is enough to keep this task's original values unchanged.

## 4. Use tuples for fixed records

A tuple is an immutable sequence: its element references cannot be replaced after creation. `location = (10, 20)` can be unpacked with `x, y = location`. The number of names must match the number of values. A one-element tuple needs a trailing comma, such as `(10,)`.

Lists and tuples can both be visited with for loops. Choose a list for a changing collection and a tuple for a fixed small record when that meaning fits. Membership uses `value in sequence`; it checks for a matching value, not an index. `sum()` totals numeric elements, but a visible accumulator loop remains useful while learning how aggregation works.

References: [Python data structures](https://docs.python.org/3.13/tutorial/datastructures.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict what two names show after appending through one alias.
2. **Explain:** Explain why append returns None rather than a new list.
3. **Modify:** Make an independent outer copy and change it without changing the source.
4. **Debug:** Repair an attempt to read index zero from an empty list.

<details>
<summary>Hints</summary>

An assignment alone aliases the list; call copy before appending.

</details>

## Independent task: lists, tuples & sequence operations

In `Practice/05_Lists_Tuples_And_Sequence_Operations.py`, complete this task:

Use `original = [120, 80]`. Make a new outer list, append 50 to the copy, and calculate the copy's total with a loop. Keep the original unchanged. Print the original, updated list, and total, one per line.

Expected output:

```text
[120, 80]
[120, 80, 50]
250
```
