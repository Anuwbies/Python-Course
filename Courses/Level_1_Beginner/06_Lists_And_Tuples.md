# Lesson 6: Lists & Tuples

So far, all variables stored a single value. In this lesson, you will learn how to store collections of data using **Lists** (mutable) and **Tuples** (immutable).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Create and manipulate Python lists `[...]` and tuples `(...)`.
2. Master positive, negative, and slicing index syntax `[start:stop:step]`.
3. Use essential list methods (`.append()`, `.pop()`, `.insert()`, `.remove()`, `.sort()`).
4. Understand mutability vs immutability.
5. Write simple **list comprehensions**.

---

## 1. Lists: Mutable Sequences

A list is an ordered, changeable (mutable) collection that allows duplicate elements.

```python
fruits = ["apple", "banana", "cherry"]
scores = [95, 82, 100, 74]
mixed = ["Alice", 20, 3.8, True]  # Can store mixed types
empty_list = []
```

---

## 2. Indexing & Slicing

Python uses **0-based indexing**. It also supports negative indices (counting backwards from the end).

```python
colors = ["red", "green", "blue", "yellow", "purple"]

# Positive indexing:
print(colors[0])  # "red" (first element)
print(colors[2])  # "blue"

# Negative indexing:
print(colors[-1]) # "purple" (last element)
print(colors[-2]) # "yellow" (second to last)

# Slicing: [start : stop : step] (stop index is exclusive)
print(colors[1:4])   # ['green', 'blue', 'yellow']
print(colors[:3])    # ['red', 'green', 'blue'] (from start to index 2)
print(colors[2:])    # ['blue', 'yellow', 'purple'] (from index 2 to end)
print(colors[::2])   # ['red', 'blue', 'purple'] (every 2nd element)
print(colors[::-1])  # ['purple', 'yellow', 'blue', 'green', 'red'] (reversed!)
```

---

## 3. Essential List Methods

```python
nums = [10, 20, 30]

# Adding elements:
nums.append(40)          # [10, 20, 30, 40] (adds to end)
nums.insert(1, 15)       # [10, 15, 20, 30, 40] (inserts 15 at index 1)
nums.extend([50, 60])    # [10, 15, 20, 30, 40, 50, 60]

# Removing elements:
removed_val = nums.pop() # Removes and returns last element (60)
nums.pop(0)              # Removes element at index 0 (10)
nums.remove(20)          # Removes first occurrence of value 20

# Information & Sorting:
print(len(nums))         # Number of items in list
nums.sort()              # Sorts in-place (ascending)
nums.sort(reverse=True)  # Sorts in-place (descending)
```

---

## 4. Tuples: Immutable Sequences

A **tuple** is defined with parentheses `(...)`. Unlike lists, tuples are **immutable**—once created, elements cannot be added, removed, or changed.

```python
coordinates = (37.7749, -122.4194)
rgb_color = (255, 128, 0)

print(coordinates[0]) # 37.7749

# coordinates[0] = 40.0  # ❌ TypeError: 'tuple' object does not support item assignment
```

### Why use tuples?
1. **Safety**: Guarantee data cannot be accidentally modified.
2. **Speed & Memory**: Tuples are faster and use less memory than lists.
3. **Dictionary keys**: Tuples can be used as dictionary keys; lists cannot.

---

## 5. Introduction to List Comprehensions

List comprehensions offer a concise syntax to create new lists from existing ones:

```python
numbers = [1, 2, 3, 4, 5]

# Traditional loop way:
squares = []
for n in numbers:
    squares.append(n ** 2)

# Pythonic List Comprehension:
squares = [n ** 2 for n in numbers]          # [1, 4, 9, 16, 25]

# With filtering condition:
even_squares = [n ** 2 for n in numbers if n % 2 == 0] # [4, 16]
```

---

## 📝 Quick Exercise

**Prompt**:
1. Create a list of 5 test scores: `[88, 92, 79, 95, 84]`.
2. Append a new score `90`.
3. Calculate the average score using `sum()` and `len()`.
4. Find the highest score using `max()` and lowest using `min()`.
5. Print all statistics formatted nicely.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
scores = [88, 92, 79, 95, 84]
scores.append(90)

average_score = sum(scores) / len(scores)
highest_score = max(scores)
lowest_score = min(scores)

print(f"All Scores: {scores}")
print(f"Total Students: {len(scores)}")
print(f"Class Average: {average_score:.2f}")
print(f"Highest Score: {highest_score}")
print(f"Lowest Score: {lowest_score}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the output of `['a', 'b', 'c', 'd'][1:3]`?**
   - A) `['a', 'b']`
   - B) `['b', 'c']`
   - C) `['b', 'c', 'd']`
   - D) `['a', 'b', 'c']`

2. **Which method is used to remove an item by its value, not index?**
   - A) `.pop()`
   - B) `.delete()`
   - C) `.remove()`
   - D) `.discard()`

3. **Can you change the value of `t = (1, 2, 3)` using `t[0] = 10`?**
   - A) Yes, tuples are mutable
   - B) No, tuples are immutable and raise a `TypeError`
   - C) Only if the tuple contains numbers
   - D) Yes, but only in Python 3.12+

<details>
<summary><b>View Answers</b></summary>
1: B (Slice 1:3 extracts index 1 and index 2)<br>
2: C (.remove(val) removes by value, .pop(idx) removes by index)<br>
3: B (Tuples cannot be mutated)
</details>
