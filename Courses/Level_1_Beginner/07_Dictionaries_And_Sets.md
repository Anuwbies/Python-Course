# Lesson 7: Dictionaries & Sets

In this lesson, you will learn about Python's two primary hash-based data structures: **Dictionaries** (Key-Value mappings) and **Sets** (Unique item collections).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Store and retrieve data using key-value pairs in Dictionaries `{key: value}`.
2. Use safe dictionary access methods like `.get()` and `.setdefault()`.
3. Iterate through dictionary keys, values, and item pairs (`.items()`).
4. Perform mathematical set operations (unions, intersections, differences).

---

## 1. Dictionaries: Key-Value Hash Maps

A **dictionary** stores data associatively using labeled keys instead of numeric positions.

```python
student = {
    "name": "Sarah Connor",
    "id": 10452,
    "gpa": 3.92,
    "courses": ["CS101", "MATH201", "ENG102"]
}

# Accessing values by key:
print(student["name"])  # "Sarah Connor"
print(student["gpa"])   # 3.92

# Modifying and adding keys:
student["gpa"] = 3.95           # Update existing key
student["is_active"] = True     # Add brand new key
```

---

## 2. Safe Retrieval with `.get()`

Accessing a non-existent key with `dict[key]` raises a `KeyError`. Using `.get()` avoids crashes by returning `None` or a default fallback value:

```python
# Risky:
# print(student["phone"])  # ❌ KeyError: 'phone'

# Safe with .get(key, default_value):
phone = student.get("phone", "Not Provided")
print(phone)  # "Not Provided"
```

---

## 3. Iterating Over Dictionaries

```python
inventory = {"Apples": 50, "Bananas": 30, "Oranges": 25}

# 1. Iterate over keys:
for item in inventory.keys():
    print(f"Product: {item}")

# 2. Iterate over values:
for qty in inventory.values():
    print(f"Stock: {qty}")

# 3. Iterate over key-value pairs (Most Common):
for item, qty in inventory.items():
    print(f"Item: {item} | Quantity: {qty}")
```

---

## 4. Sets: Unique Collections

A **set** is an unordered collection of unique elements with no duplicates.

```python
raw_tags = ["python", "code", "python", "dev", "code", "backend"]
unique_tags = set(raw_tags)
print(unique_tags)  # {'python', 'code', 'dev', 'backend'}
```

### Mathematical Set Operations:
```python
group_a = {"Alice", "Bob", "Charlie"}
group_b = {"Charlie", "David", "Eve"}

# Union (all students in either group): |
print(group_a | group_b)  # {'Alice', 'Bob', 'Charlie', 'David', 'Eve'}

# Intersection (students in BOTH groups): &
print(group_a & group_b)  # {'Charlie'}

# Difference (in group_a but NOT in group_b): -
print(group_a - group_b)  # {'Alice', 'Bob'}
```

---

## 📝 Quick Exercise

**Prompt**:
Write a **Word Frequency Counter**:
1. Take a sentence: `"to be or not to be that is the question"`.
2. Split it into words using `.split()`.
3. Build a dictionary where the keys are words and values are how many times each word occurs.
4. Print the resulting dictionary.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
sentence = "to be or not to be that is the question"
words = sentence.split()

frequency = {}
for word in words:
    frequency[word] = frequency.get(word, 0) + 1

print("--- Word Frequencies ---")
for word, count in frequency.items():
    print(f"'{word}': {count} time(s)")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What happens if you run `d = {}; print(d['age'])`?**
   - A) Prints `None`
   - B) Prints `0`
   - C) Raises a `KeyError`
   - D) Raises an `IndexError`

2. **Can a Python list be used as a dictionary key?**
   - A) Yes, any data type can be a key
   - B) No, dictionary keys must be hashable/immutable (like strings, ints, tuples)
   - C) Only if the list contains strings
   - D) Yes, in Python 3.10+

3. **What is the result of `len({1, 2, 2, 3, 3, 3})`?**
   - A) `6`
   - B) `3`
   - C) `1`
   - D) `TypeError`

<details>
<summary><b>View Answers</b></summary>
1: C (Direct square bracket lookup for a missing key throws KeyError)<br>
2: B (Lists are mutable and unhashable, so they cannot be dict keys)<br>
3: B (Sets deduplicate all elements, leaving {1, 2, 3})
</details>
