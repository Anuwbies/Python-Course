# Lesson 6: Sequence Data Structures: Lists & Tuples

Up to this point, our variables held single individual values. However, real-world systems manage collections of items: orders in a shopping cart, server logs in a queue, or stock price ticks across a trading day. In this lesson, you will master Python's two foundational sequence types: mutable **Lists** and immutable **Tuples**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Create and manipulate dynamic mutable **Lists** (`list`).
2. Master core list methods: `append()`, `insert()`, `extend()`, `pop()`, `remove()`, and `sort()`.
3. Slice sequences using zero-indexed notation: `[start:stop:step]`.
4. Write concise, performant **List Comprehensions** with conditional filters.
5. Create immutable **Tuples** (`tuple`) and perform multi-variable **Tuple Unpacking**.
6. Calculate statistical aggregations using built-in functions: `len()`, `sum()`, `min()`, `max()`.

---

## 1. Lists: Mutable Ordered Sequences

A Python `list` is a dynamic, ordered array that can grow or shrink in memory and hold heterogeneous data types.

```python
# Creating lists:
inventory = ["Laptop", "Keyboard", "Mouse", "Monitor"]

# 1. Zero-based and negative indexing:
print(inventory[0])   # "Laptop" (First element)
print(inventory[-1])  # "Monitor" (Last element)

# 2. Mutability (Modifying items directly):
inventory[1] = "Mechanical Keyboard"

# 3. Essential List Methods:
inventory.append("Headset")             # Adds to end
inventory.insert(1, "Webcam")           # Inserts at specific index
inventory.extend(["USB Hub", "Cable"])  # Appends multiple items from another sequence

removed_item = inventory.pop()          # Removes and returns last element ("Cable")
inventory.remove("Webcam")              # Removes first occurrence of value

# 4. Sorting:
prices = [1299.99, 49.50, 24.99, 399.00]
prices.sort()                           # In-place ascending sort: [24.99, 49.50, 399.00, 1299.99]
prices.sort(reverse=True)               # Descending sort
```

---

## 2. Advanced Sequence Slicing (`[start:stop:step]`)

Slicing extracts a sub-sequence without modifying the original collection:
- `start`: The starting index (inclusive). Default is `0`.
- `stop`: The ending index (**exclusive**). Default is `len(sequence)`.
- `step`: Stride length. Default is `1`.

```python
data = [10, 20, 30, 40, 50, 60, 70, 80]

print(data[1:4])    # [20, 30, 40] (Indices 1, 2, 3)
print(data[:3])     # [10, 20, 30] (First 3 elements)
print(data[-3:])    # [60, 70, 80] (Last 3 elements)
print(data[::2])    # [10, 30, 50, 70] (Every second element)
print(data[::-1])   # [80, 70, 60, 50, 40, 30, 20, 10] (Reverses list)
```

---

## 3. List Comprehensions

List comprehensions provide an idiomatic, readable, and faster way to create new lists by transforming or filtering existing iterables:

$$\text{new\_list} = [\textbf{expression} \textbf{ for } \text{item} \textbf{ in } \text{iterable} \textbf{ if } \text{condition}]$$

```python
raw_readings = [14.2, -999.0, 18.5, 22.1, -999.0, 19.8]

# 1. Filtering corrupted sensor readings (-999.0):
clean_readings = [val for val in raw_readings if val != -999.0]
# [14.2, 18.5, 22.1, 19.8]

# 2. Transforming data (Convert Celsius to Fahrenheit):
readings_f = [(c * 9/5) + 32 for c in clean_readings]
# [57.56, 65.3, 71.78, 67.64]
```

---

## 4. Tuples: Immutable Sequences & Unpacking

A **tuple** is an immutable sequence defined with parentheses `( )`. Once initialized, its elements **cannot** be added, modified, or removed.

### Why use Tuples over Lists?
1. **Data Integrity**: Guarantees fixed records (e.g. `(latitude, longitude)` or database row records) cannot be accidentally altered.
2. **Performance & Memory**: Tuples consume less memory and allocate faster than dynamic lists.

```python
# Fixed geographic coordinate tuple:
server_location = (37.7749, -122.4194, "San Francisco DC-1")

# Tuple Unpacking (Destructuring):
lat, lon, facility_name = server_location
print(f"DC Name: {facility_name} (Lat: {lat}, Lon: {lon})")

# Swapping two variables in a single line using tuple packing/unpacking:
x, y = 10, 20
x, y = y, x   # x is now 20, y is now 10!
```

---

## 💻 Code Example & Reference

The following real-life program models an **Algorithmic Stock Trading Day Analytics & Outlier Engine**, combining all list, tuple, and aggregation concepts taught in this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Frequency Stock Market Analytics Engine
# =====================================================================

print("=" * 70)
print(f"{'📊 FINANCIAL EQUITIES TICKER ANALYTICS ENGINE':^70}")
print("=" * 70)

# 1. Historical Trade Records stored as immutable (timestamp, price, volume) tuples
trade_records = [
    ("09:30:00", 182.50, 500),
    ("09:30:15", 183.10, 1200),
    ("09:30:30", 182.90, 800),
    ("09:31:00", 184.25, 2500),
    ("09:31:45", 183.80, 450),
    ("09:32:10", 185.00, 3100),
    ("09:32:50", 184.60, 600),
    ("09:33:15", 185.75, 4200),
]

# 2. Extracting Prices and Volumes using List Comprehensions & Unpacking (Lesson 6)
all_prices = [price for _, price, _ in trade_records]
all_volumes = [volume for _, _, volume in trade_records]

# 3. Built-in Statistical Aggregations
total_trades = len(trade_records)
total_volume_traded = sum(all_volumes)
min_session_price = min(all_prices)
max_session_price = max(all_prices)
open_price = trade_records[0][1]      # First trade price
close_price = trade_records[-1][1]    # Last trade price

# Volume-Weighted Average Price (VWAP) Calculation: sum(price * volume) / total_volume
vwap_numerator = sum([price * volume for _, price, volume in trade_records])
session_vwap = vwap_numerator / total_volume_traded

# 4. Slicing Top High-Volume Trades (Lessons 3 & 6)
# Sort trades descending by volume
sorted_by_volume = sorted(trade_records, key=lambda x: x[2], reverse=True)
top_3_volume_trades = sorted_by_volume[:3]

# 5. Formatted Market Terminal Output (Lessons 1 & 6)
print(f"{'Metric':<35} | {'Value':>25}")
print("-" * 70)
print(f"{'Total Logged Trades':<35} | {total_trades:>25}")
print(f"{'Total Shares Exchanged':<35} | {total_volume_traded:>25,}")
print(f"{'Market Opening Price':<35} | {f'${open_price:.2f}':>25}")
print(f"{'Market Closing Price':<35} | {f'${close_price:.2f}':>25}")
print(f"{'Session Price Low / High':<35} | {f'${min_session_price:.2f} - ${max_session_price:.2f}':>25}")
print(f"{'Session VWAP (Benchmark)':<35} | {f'${session_vwap:.2f}':>25}")
print("=" * 70)

print(f"{'TOP 3 HIGH-VOLUME TRANSACTIONS (WHALE TRADES)':^70}")
print("-" * 70)
print(f"{'Rank':<8} | {'Timestamp':^15} | {'Execution Price':>18} | {'Volume':>15}")
print("-" * 70)

for rank, (ts, price, vol) in enumerate(top_3_volume_trades, start=1):
    print(f"{rank:<8} | {ts:^15} | {f'${price:.2f}':>18} | {f'{vol:,} shares':>15}")

print("=" * 70)
```

### 🔍 Code Explanation:
- **Tuples for Fixed Records**: Each transaction is modeled as an immutable `(timestamp, price, volume)` tuple to ensure financial audit integrity.
- **List Comprehensions**: Comprehensions with tuple unpacking (`[price for _, price, _ in trade_records]`) isolate pricing streams concisely without manual loops.
- **Statistical Aggregation Functions**: `min()`, `max()`, `sum()`, and `len()` calculate high-level market metrics efficiently.
- **Slicing**: `sorted_by_volume[:3]` extracts the top 3 highest-volume transactions.

---

## 📝 Quick Exercise: Academic Class Grade Registry & Performance Analyzer

### 🏢 Real-Life Scenario
You are developing the semester grading and academic standing module for a university computer science department. The professor enters student names along with their raw exam scores. The program filters passing students, computes statistical class metrics (mean, highest, lowest score), detects honor roll qualifiers, and outputs a ranked grade leaderboard.

### 📋 Requirements
1. Capture student records interactively:
   - Use a `while True` loop to prompt for student records until the instructor enters `"done"`.
   - In each iteration, capture:
     - `student_name`: Sanitized with `.strip().title()`
     - `score`: Cast to `float` (range 0.0 to 100.0)
   - Store each entry as a `(student_name, score)` tuple inside a master `student_records` list.
2. Analytics & Slicing:
   - Compute `class_average = sum(all_scores) / len(all_scores)`.
   - Identify `highest_score` and `lowest_score`.
   - Use a **List Comprehension** to create a list of `honor_students` (scores $\ge 90.0$).
   - Use a **List Comprehension** to create a list of `failing_students` (scores $< 60.0$).
3. Sort the `student_records` in descending order of score.
4. Output the complete academic performance summary and ranked leaderboard.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1 through 6** (variables, types, input sanitization, casting, arithmetic, compound conditionals, while/for loops, lists, tuples, slicing, list comprehensions, `min`/`max`/`sum`/`len`, and f-strings).

### 🎯 Expected Output
*(Assuming the instructor inputs: `Elena Rostova` 94.5, `Marcus Vance` 78.0, `Sarah Connor` 98.0, `David Kim` 56.5, `Chloe Price` 88.0, and `done`)*

```text
Enter Student Name (or 'done' to finish): Elena Rostova
Enter Exam Score (0-100): 94.5

Enter Student Name (or 'done' to finish): Marcus Vance
Enter Exam Score (0-100): 78.0

Enter Student Name (or 'done' to finish): Sarah Connor
Enter Exam Score (0-100): 98.0

Enter Student Name (or 'done' to finish): David Kim
Enter Exam Score (0-100): 56.5

Enter Student Name (or 'done' to finish): Chloe Price
Enter Exam Score (0-100): 88.0

Enter Student Name (or 'done' to finish): done

==================================================
           CLASSROOM GRADE ANALYTICS              
==================================================
Total Students:    5
Class Average:     83.00%
Top Exam Score:    98.00%
Lowest Exam Score: 56.50%
Honor Roll Count:  2 student(s) (>=90%)
Failing Count:     1 student(s) (<60%)
--------------------------------------------------
RANKED LEADERBOARD:
  #1: Sarah Connor         - 98.00% [HONOR ROLL 🌟]
  #2: Elena Rostova        - 94.50% [HONOR ROLL 🌟]
  #3: Chloe Price          - 88.00%
  #4: Marcus Vance         - 78.00%
  #5: David Kim            - 56.50% [ACADEMIC WARNING ⚠️]
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Interactive Collection Loop (Lessons 1-6)
student_records = []

while True:
    name_input = input("Enter Student Name (or 'done' to finish): ").strip().title()
    if name_input.lower() == "done":
        if len(student_records) == 0:
            print("❌ Must enter at least one student.")
            continue
        break

    score_input = float(input("Enter Exam Score (0-100): "))
    if 0.0 <= score_input <= 100.0:
        student_records.append((name_input, score_input))
    else:
        print("❌ Score must be between 0 and 100.")

# 2. Extract Scores and Compute Metrics (Lesson 6)
scores_list = [score for _, score in student_records]

total_students = len(student_records)
class_average = sum(scores_list) / total_students
top_score = max(scores_list)
lowest_score = min(scores_list)

honor_students = [name for name, score in student_records if score >= 90.0]
failing_students = [name for name, score in student_records if score < 60.0]

# 3. Sort Descending by Score (Lesson 6)
sorted_records = sorted(student_records, key=lambda x: x[1], reverse=True)

# 4. Formatted Display Output (Lessons 1 & 6)
print("\n==================================================")
print("           CLASSROOM GRADE ANALYTICS              ")
print("==================================================")
print(f"Total Students:    {total_students}")
print(f"Class Average:     {class_average:.2f}%")
print(f"Top Exam Score:    {top_score:.2f}%")
print(f"Lowest Exam Score: {lowest_score:.2f}%")
print(f"Honor Roll Count:  {len(honor_students)} student(s) (>=90%)")
print(f"Failing Count:     {len(failing_students)} student(s) (<60%)")
print("--------------------------------------------------")
print("RANKED LEADERBOARD:")

for rank, (name, score) in enumerate(sorted_records, start=1):
    tag = ""
    if score >= 90.0:
        tag = " [HONOR ROLL 🌟]"
    elif score < 60.0:
        tag = " [ACADEMIC WARNING ⚠️]"

    print(f"  #{rank}: {name:<20} - {score:.2f}%{tag}")

print("==================================================")
```

**Explanation of the Solution:**
- `student_records` collects `(name, score)` tuples dynamically during a `while` loop.
- List comprehensions extract score lists and filter students based on performance thresholds.
- `sorted(..., key=lambda x: x[1], reverse=True)` orders students by highest score for the leaderboard.
</details>
