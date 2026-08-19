# Lesson 6: Lists & Tuples

Until now, each variable in our programs stored only a single value. In this lesson, you will learn how to store, organize, and transform ordered collections of data using **Lists** (mutable sequences) and **Tuples** (immutable sequences).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Create and manipulate Python lists `[...]` and tuples `(...)`.
2. Master 0-based indexing, negative indexing, and slicing `[start:stop:step]`.
3. Use essential list mutation methods (`.append()`, `.extend()`, `.insert()`, `.pop()`, `.remove()`, `.sort()`, `.reverse()`, `.copy()`).
4. Understand **mutability vs. immutability** and the reference vs. shallow copy model.
5. Utilize built-in sequence functions: `len()`, `sum()`, `min()`, `max()`, and `.index()`.
6. Write concise, readable, and high-performance **List Comprehensions**.

---

## 1. Lists: Ordered, Mutable Collections

A **list** is an ordered, changeable collection of items enclosed in square brackets `[...]`. Lists can contain duplicate elements and store heterogeneous (mixed) data types.

```python
# Creating lists:
product_codes = ["SKU-101", "SKU-102", "SKU-103"]
sensor_readings = [23.4, 25.1, 22.8, 24.0]
mixed_record = ["Server-01", 8080, True, 99.98]
empty_list = []
```

---

## 2. Indexing & Slicing Mechanics

Python sequences use **0-based indexing** (counting from `0` to `len - 1`) and support **negative indexing** (counting backwards from `-1`).

```
List Elements:   ["Alpha", "Bravo", "Charlie", "Delta", "Echo"]
Positive Index:     0        1         2         3        4
Negative Index:    -5       -4        -3        -2       -1
```

```python
servers = ["Alpha", "Bravo", "Charlie", "Delta", "Echo"]

# Positive Indexing:
print(servers[0])   # "Alpha" (First element)
print(servers[2])   # "Charlie"

# Negative Indexing:
print(servers[-1])  # "Echo" (Last element)
print(servers[-2])  # "Delta" (Second to last)
```

### Slicing Syntax: `[start : stop : step]`
- `start`: The starting index (inclusive). Defaults to `0`.
- `stop`: The ending index (**exclusive**). Defaults to `len(list)`.
- `step`: The step interval. Defaults to `1`.

```python
# Sub-slice from index 1 up to (not including) index 4:
print(servers[1:4])   # ['Bravo', 'Charlie', 'Delta']

# Slicing from the beginning up to index 3:
print(servers[:3])    # ['Alpha', 'Bravo', 'Charlie']

# Slicing from index 2 to the end:
print(servers[2:])    # ['Charlie', 'Delta', 'Echo']

# Slicing with step of 2 (every second element):
print(servers[::2])   # ['Alpha', 'Charlie', 'Echo']

# Reversing a list using negative step:
print(servers[::-1])  # ['Echo', 'Delta', 'Charlie', 'Bravo', 'Alpha']
```

---

## 3. Essential List Methods

```python
inventory = ["Mouse", "Keyboard"]

# 1. Adding elements:
inventory.append("Monitor")             # ['Mouse', 'Keyboard', 'Monitor'] (Adds to end)
inventory.insert(1, "Webcam")           # ['Mouse', 'Webcam', 'Keyboard', 'Monitor']
inventory.extend(["Headset", "Desk"])   # Adds multiple items to end

# 2. Removing elements:
last_item = inventory.pop()             # Removes and returns last item ('Desk')
first_item = inventory.pop(0)           # Removes and returns item at index 0 ('Mouse')
inventory.remove("Webcam")              # Removes first occurrence of "Webcam"

# 3. Inspecting and Sorting:
print(len(inventory))                   # Total items count
print(inventory.index("Monitor"))       # Returns index of item
print(inventory.count("Keyboard"))      # Counts occurrences

scores = [88, 95, 72, 100, 64]
scores.sort()                           # In-place ascending sort: [64, 72, 88, 95, 100]
scores.sort(reverse=True)               # In-place descending sort: [100, 95, 88, 72, 64]
```

### ⚠️ Referencing vs. Copying (`.copy()`)
```python
list_a = [1, 2, 3]
list_b = list_a         # ❌ Copies REFERENCE only! Modifying list_b mutates list_a!
list_c = list_a.copy()  # ✅ Creates an independent shallow copy
```

---

## 4. Tuples: Ordered, Immutable Sequences

A **tuple** is defined with parentheses `(...)`. Unlike lists, tuples are **immutable**—once created, their elements cannot be changed, added, or removed.

```python
# Defining tuples:
server_location = ("US-East", "Rack-4B", 42)
rgb_primary = (255, 0, 0)
single_element_tuple = (42,)  # Note the trailing comma!

print(server_location[0])     # 'US-East'

# Attempting mutation raises an error:
# server_location[0] = "US-West" # ❌ TypeError: 'tuple' object does not support item assignment
```

### Why Use Tuples Over Lists?
1. **Data Integrity**: Guarantees fixed configurations or constants cannot be altered accidentally at runtime.
2. **Performance**: Tuples use less memory and are faster to allocate than dynamic lists.
3. **Tuple Unpacking**: Unpack multiple values cleanly in a single assignment:
   ```python
   region, rack, port = server_location
   print(f"Region: {region} | Port: {port}")
   ```

---

## 5. List Comprehensions

List comprehensions offer a concise, Pythonic syntax for creating new lists by transforming or filtering existing iterables.

**Basic Syntax**: `[expression for item in iterable]`  
**Filtered Syntax**: `[expression for item in iterable if condition]`

```python
raw_prices = [10.0, 25.0, 50.0, 100.0]

# Traditional loop:
taxed_prices = []
for p in raw_prices:
    taxed_prices.append(p * 1.08)

# Pythonic List Comprehension:
taxed_prices = [p * 1.08 for p in raw_prices]            # [10.8, 27.0, 54.0, 108.0]

# With condition filter (only include prices >= $50):
expensive_taxed = [p * 1.08 for p in raw_prices if p >= 50.0]  # [54.0, 108.0]
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_06_Lists_And_Tuples.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_06_Lists_And_Tuples.py):

```python
# Student Grade Analytics
exam_scores = [78, 92, 85, 64, 98, 89, 74, 91]

total_students = len(exam_scores)
class_average = sum(exam_scores) / total_students
top_score = max(exam_scores)
lowest_score = min(exam_scores)

# Filter honor roll scores (>= 90) using list comprehension:
honor_roll = [s for s in exam_scores if s >= 90]

print(f"Enrollment:    {total_students} students")
print(f"Class Average: {class_average:.2f}%")
print(f"Score Range:   {lowest_score}% to {top_score}%")
print(f"Honor Roll:    {honor_roll} ({len(honor_roll)} students)")
```

---

## 📝 Quick Exercise: Warehouse Inventory Fulfillment Analytics

### 🏢 Real-Life Scenario
You are developing the weekly logistics and demand forecasting report for an e-commerce fulfillment warehouse. The operations team tracks daily shipped unit counts for a flagship consumer electronic SKU across the 7 days of the operational week. The system must analyze sales volume, identify peak and lowest volume days, isolate above-average fulfillment spikes, and project next week's initial restock requirement.

### 📋 Requirements
1. Declare the data collections:
   - `weekly_sales`: `[145, 230, 180, 310, 260, 420, 195]` (shipped unit count list)
   - `day_names`: `("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")` (day names tuple)
2. Compute statistical aggregates using built-in functions:
   - `total_units = sum(weekly_sales)`
   - `days_count = len(weekly_sales)`
   - `average_daily_units = total_units / days_count`
   - `max_units = max(weekly_sales)`
   - `min_units = min(weekly_sales)`
   - `peak_day_index = weekly_sales.index(max_units)` $\rightarrow$ `peak_day_name = day_names[peak_day_index]`
   - `lowest_day_index = weekly_sales.index(min_units)` $\rightarrow$ `lowest_day_name = day_names[lowest_day_index]`
3. Use a **list comprehension** to generate a new list `above_average_sales` containing only the daily sales numbers strictly greater than `average_daily_units`.
4. Use `.copy()` and `.append()` to create a `restock_projection` list containing all 7 days plus an 8th projected restock target (`int(average_daily_units * 1.15)`).
5. Use a `for` loop over `range(len(weekly_sales))` to print a clean day-by-day fulfillment ledger.
6. Print the formatted supply chain summary report.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 through 6 (variables, primitives, `input()`, numbers, strings, conditionals, loops, `range()`, lists, tuples, indexing, slicing, list methods, list comprehensions, aggregate functions `sum()`, `len()`, `min()`, `max()`, f-strings, and `print()`). Do **not** use dictionaries, sets, or functions.

### 🎯 Expected Output
```text
==================================================
      WAREHOUSE WEEKLY FULFILLMENT REPORT         
==================================================
DAILY SHIPMENT LEDGER:
- Monday   : 145 units
- Tuesday  : 230 units
- Wednesday: 180 units
- Thursday : 310 units
- Friday   : 260 units
- Saturday : 420 units
- Sunday   : 195 units
--------------------------------------------------
WEEKLY PERFORMANCE METRICS:
Total Volume:       1,740 units
Daily Average:      248.57 units/day
Peak Fulfillment:   Saturday (420 units)
Lowest Fulfillment: Monday (145 units)
--------------------------------------------------
High Volume Days (>Avg): [310, 260, 420] (3 days)
Next Day Projected Need: 285 units
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Declare weekly data collections
weekly_sales = [145, 230, 180, 310, 260, 420, 195]
day_names = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

# 2. Compute aggregate metrics
total_units = sum(weekly_sales)
days_count = len(weekly_sales)
average_daily_units = total_units / days_count
max_units = max(weekly_sales)
min_units = min(weekly_sales)

peak_day_index = weekly_sales.index(max_units)
peak_day_name = day_names[peak_day_index]

lowest_day_index = weekly_sales.index(min_units)
lowest_day_name = day_names[lowest_day_index]

# 3. List comprehension for above-average days
above_average_sales = [units for units in weekly_sales if units > average_daily_units]

# 4. Projected demand with copy and append
projected_target = int(average_daily_units * 1.15)
restock_projection = weekly_sales.copy()
restock_projection.append(projected_target)

# 5. Output formatted report
print("==================================================")
print("      WAREHOUSE WEEKLY FULFILLMENT REPORT         ")
print("==================================================")
print("DAILY SHIPMENT LEDGER:")
for i in range(len(weekly_sales)):
    print(f"- {day_names[i]:<9}: {weekly_sales[i]} units")

print("--------------------------------------------------")
print("WEEKLY PERFORMANCE METRICS:")
print(f"Total Volume:       {total_units:,} units")
print(f"Daily Average:      {average_daily_units:.2f} units/day")
print(f"Peak Fulfillment:   {peak_day_name} ({max_units} units)")
print(f"Lowest Fulfillment: {lowest_day_name} ({min_units} units)")
print("--------------------------------------------------")
print(f"High Volume Days (>Avg): {above_average_sales} ({len(above_average_sales)} days)")
print(f"Next Day Projected Need: {projected_target} units")
print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What is the result of `['a', 'b', 'c', 'd', 'e'][1:4]`?**
   - A) `['a', 'b', 'c']`
   - B) `['b', 'c', 'd']`
   - C) `['b', 'c', 'd', 'e']`
   - D) `['c', 'd']`

2. **If `x = [10, 20]`, what is the difference between `y = x` and `y = x.copy()`?**
   - A) `y = x` copies values, while `y = x.copy()` copies reference.
   - B) `y = x` assigns a reference to the same list; modifying `y` modifies `x`. `x.copy()` creates an independent copy.
   - C) There is no difference.
   - D) `x.copy()` converts the list into a tuple.

3. **What is the output of `[n * 2 for n in [1, 2, 3, 4] if n % 2 == 0]`?**
   - A) `[2, 4, 6, 8]`
   - B) `[4, 8]`
   - C) `[2, 6]`
   - D) `[4]`

<details>
<summary><b>View Answers</b></summary>
1: B (Slicing 1:4 captures indices 1, 2, 3: 'b', 'c', 'd')<br>
2: B (Direct assignment creates an alias pointing to the exact same list in memory)<br>
3: B (Filter keeps only even numbers [2, 4], then doubles them: [4, 8])
</details>
