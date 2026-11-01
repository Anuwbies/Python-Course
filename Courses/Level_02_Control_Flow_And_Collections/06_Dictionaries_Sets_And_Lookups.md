# Lesson 6: Dictionaries, Sets & Lookups

**Prerequisites:** Level 1 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Dictionaries_Sets_And_Lookups.py`.

Use a dictionary when you need values identified by keys and a set when you need unique membership. Select by the relationship the data represents rather than by which syntax looks shortest.

## 1. Associate a key with a value

A dictionary literal maps keys to values with a colon. `totals["food"]` retrieves the value for that exact key. Assigning the same key again replaces its value; it does not create a second independent entry under that key.

```python
totals = {"food": 120, "travel": 30}
totals["food"] = totals["food"] + 80
print(totals["food"])  # 200
```

A direct lookup for a missing key raises KeyError. `.get(key, default)` returns the default when the key is absent. A counting loop can therefore express `counts[word] = counts.get(word, 0) + 1` without inventing a starting count for every possible word in advance.

## 2. Iterate over the relationship you need

Iterating over a dictionary directly visits keys. `.values()` visits values, and `.items()` supplies key/value pairs that can be unpacked in a for loop. Do not assume iterating directly gives pairs.

```python
totals = {"food": 200, "travel": 30}
for category, amount in totals.items():
    print(f"{category}: {amount}")
```

Dictionaries preserve insertion order, but a report's desired order may be different from entry order. The next lesson uses sorted keys for a deliberate display order. Do not add or remove keys while iterating a live dictionary; collect the intended changes or iterate an appropriate copy.

To remove a known dictionary key, `del totals["food"]` deletes that association. A missing key raises KeyError. Check membership first when absence should be handled as an ordinary case. Deletion changes the dictionary, so do not perform it while iterating its live keys.

`totals.clear()` removes every association in place and returns None. Use it only when discarding the entire mapping is intended; a copy held by another name is independent, while an alias observes the clearing.

## 3. Represent uniqueness with a set

A set stores unique elements and supports membership, union, intersection, and difference. A nonempty set literal uses braces without key/value colons; an empty set is created with `set()`. Empty braces create a dictionary instead.

```python
visited = {"food", "food", "travel"}
print(len(visited))       # 2
print("food" in visited)  # True
```

Set iteration order is not a report contract. Displaying an entire set and expecting one exact order makes a brittle example. Sort its elements when order matters, or ask a membership or length question instead.

## 4. Think about valid keys

Dictionary keys and set elements must be hashable. Strings and integers fit these examples; a list cannot be used as a key. A tuple can be hashable when all its elements are hashable. This is about stable key behavior, not whether the key looks small.

Use a dictionary to track how much each category contains. Use a set to track which categories have been seen. A list is still suitable for the sequence of individual entries because repeated expenses and entry order may both be meaningful.

## Build and combine sets explicitly

`set(iterable)` copies the unique elements of an iterable into a new set. `labels.add(value)` inserts one element in place and returns None; inserting an existing value leaves the membership unchanged. `labels.copy()` makes an independent outer set. As with dictionaries, membership concerns values, not positions.

```python
labels = set()
for category in ["food", "food", "travel"]:
    labels.add(category)
required = {"food"}
print(required <= labels)                 # True: every required item is present
print(sorted(labels & {"food", "books"})) # ['food']: intersection
print(sorted(labels - required))          # ['travel']: difference
```

`left <= right` tests whether left is a subset of right. `left & right` returns the elements present in both, `left | right` returns their union, and `left - right` returns elements only in left. These expressions create new sets; they do not change either input. Empty sets are false in conditions, like empty lists and dictionaries.

For a dictionary whose values are collections, `mapping.setdefault(key, default)` returns the existing value, or stores and returns default when the key is absent. For example, `groups.setdefault("food", set()).add("D1")` obtains the food set and inserts D1. Unlike get, setdefault changes the dictionary on a missing key. Use get for numeric counts and setdefault when deliberately building a collection per key. `set(record)` collects a dictionary's keys, so comparing it with an expected field-name set checks exact fields without depending on order.

References: [Python data structures](https://docs.python.org/3.13/tutorial/datastructures.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict how many elements remain after constructing a set with repeated labels.
2. **Explain:** Explain the difference between an absent key and a key whose value is zero.
3. **Modify:** Add a new category through get without prepopulating it.
4. **Debug:** Correct a loop that expects two values from direct dictionary iteration.

<details>
<summary>Hints</summary>

Use a zero default only for a missing count; the unique set needs add for each label.

</details>

## Independent task: dictionaries, sets & lookups

In `Practice/06_Dictionaries_Sets_And_Lookups.py`, complete this task:

Use `categories = ["food", "travel", "food"]`. Build a dictionary counting each label and a set of unique labels. Print the food count, travel count, and number of unique labels in that order.

Expected output:

```text
2
1
2
```
