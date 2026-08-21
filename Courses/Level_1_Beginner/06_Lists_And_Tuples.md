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

---

## 5. CPython List Internals & Memory Architecture

Under the hood in CPython, a `list` is implemented as a **contiguous array of pointers to `PyObject` items** (not the raw objects themselves).

```
Python list variable [ nums ] ──► [ PyListObject Header | Capacity: 8 | Size: 3 ]
                                  [ Ptr 0 ] ──► [ PyObject: 10 ]
                                  [ Ptr 1 ] ──► [ PyObject: 20 ]
                                  [ Ptr 2 ] ──► [ PyObject: 30 ]
                                  [ Ptr 3 ] ──► (Empty pre-allocated slot)
```

### ⚡ Geometric Over-Allocation Strategy
When you `.append()` items to a list and its capacity is exceeded, CPython resizes the underlying array with a growth factor (`0, 4, 8, 16, 25, 35, 46, 58, 72, 88...`). This ensures `.append()` runs in **amortized $O(1)$ constant time**!

### 📊 Time Complexity Reference Table for Lists

| Operation | Syntax / Method | Average Time Complexity | Note |
| :--- | :--- | :---: | :--- |
| **Index Access / Update** | `lst[i]`, `lst[i] = x` | **$O(1)$** | Direct pointer offset calculation |
| **Append to End** | `lst.append(x)` | **$O(1)$** amortized | Inserts into pre-allocated slot |
| **Pop from End** | `lst.pop()` | **$O(1)$** | Just decrements size counter |
| **Insert / Delete at Index 0** | `lst.insert(0, x)`, `lst.pop(0)` | **$O(N)$** | Must shift all $N$ pointers right/left |
| **Membership Search** | `x in lst` | **$O(N)$** | Linear scan from index 0 to $N-1$ |
| **Sorting** | `lst.sort()` | **$O(N \log N)$** | Timsort algorithm |

---

## 6. Shallow Copy vs. Deep Copy & The Nested List Trap

### ⚠️ The Nested List Multiplication Trap
```python
# ❌ DANGEROUS BUG: Creates 3 references to the EXACT SAME inner list object!
grid_bad = [[0] * 3] * 3
grid_bad[0][0] = 99
print(grid_bad) # Output: [[99, 0, 0], [99, 0, 0], [99, 0, 0]] (All rows changed!)

# ✅ CORRECT: Use a list comprehension to allocate 3 independent inner lists:
grid_good = [[0] * 3 for _ in range(3)]
grid_good[0][0] = 99
print(grid_good) # Output: [[99, 0, 0], [0, 0, 0], [0, 0, 0]] (Isolated!)
```

### 🛡️ Shallow vs. Deep Copying
- **Shallow Copy (`lst.copy()`, `lst[:]`)**: Copies the outer container pointers, but nested objects still share memory.
- **Deep Copy (`copy.deepcopy(lst)`)**: Recursively copies all nested objects at all depths.

```python
import copy

original = [1, [2, 3]]
shallow = original.copy()
deep = copy.deepcopy(original)

original[1][0] = 999
print("Original:", original) # [1, [999, 3]]
print("Shallow: ", shallow)  # [1, [999, 3]] (Inner list was shared!)
print("Deep:    ", deep)     # [1, [2, 3]]   (Completely isolated!)
```

---

## 7. Namedtuples: Self-Documenting Lightweight Tuples

When you want the immutability and memory performance of tuples with attribute-based access like an object:

```python
from collections import namedtuple

# Define a lightweight record blueprint:
ServerNode = namedtuple("ServerNode", ["hostname", "ip", "cores", "ram_gb"])

node = ServerNode("prod-db-01", "10.0.0.1", 32, 128.0)
print(node.hostname) # "prod-db-01" (Clean dot notation!)
print(node[1])       # "10.0.0.1" (Also indexable!)
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

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master dynamic lists, slicing, list comprehensions, tuples, unpacking, memory copy patterns, and statistical aggregations:

---

### 🟢 Tier 1: List Operations & Basic Slicing (Exercises 1–3)

#### 🔹 Exercise 1: Task Queue FIFO/LIFO Simulator
* **Goal**: Initialize `queue = []`.
* **Operations**: Append `"Task 1"`, `"Task 2"`, `"Task 3"`. Pop the first item using `.pop(0)`, then pop the last item using `.pop()`. Print remaining queue.

#### 🔹 Exercise 2: Sequence Slicing Extractor
* **Goal**: Given `data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]`.
* **Extract**: (1) First 3 items, (2) Last 3 items, (3) Every second item, (4) Reversed list. Print each slice.

#### 🔹 Exercise 3: In-Place Sorting & Reversal
* **Goal**: Given `grades = [78.5, 92.0, 64.0, 88.5, 99.0]`.
* **Requirement**: Sort ascending using `.sort()`, then reverse in-place using `.reverse()`. Print highest and lowest using index `[0]` and `[-1]`.

---

### 🟡 Tier 2: Comprehensions & Tuples (Exercises 4–6)

#### 🔹 Exercise 4: Conditional List Comprehension Filter
* **Goal**: Given `temperatures = [28.5, -999.0, 32.0, 31.5, -999.0, 29.0]`.
* **Requirement**: Use a list comprehension to filter out missing sensor codes (`-999.0`) and convert remaining to Fahrenheit: `[(c * 9/5) + 32 for c in temperatures if c != -999.0]`.

#### 🔹 Exercise 5: Multi-Variable Tuple Unpacking & Swapping
* **Goal**: Given `server_record = ("192.168.1.1", 8080, "PRODUCTION", True)`.
* **Requirement**: Unpack into `ip`, `port`, `env`, `is_active`. Swap `ip` and `env` in one line (`ip, env = env, ip`).

#### 🔹 Exercise 6: Deduplication Preserving Order
* **Goal**: Given `logs = ["user_login", "page_view", "user_login", "checkout", "page_view"]`.
* **Requirement**: Create a new list containing unique events in the order they first appeared.

---

### 🟠 Tier 3: Memory Models & Multi-Dimensional Lists (Exercises 7–9)

#### 🔹 Exercise 7: Deep Copy vs Shallow Copy Inspector
* **Goal**: Given nested list `team = [["Alice", 90], ["Bob", 85]]`.
* **Requirement**: Create a shallow copy with `.copy()` and a deep copy with `copy.deepcopy()`. Modify the inner score of `"Alice"` in the original. Demonstrate how shallow is affected while deep remains isolated.

#### 🔹 Exercise 8: Matrix Transposition with Comprehensions
* **Goal**: Given a $3 \times 3$ grid `matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]`.
* **Requirement**: Use a nested list comprehension `[[row[i] for row in matrix] for i in range(3)]` to compute the transposed matrix.

#### 🔹 Exercise 9: Namedtuple Financial Portfolio Analyzer
* **Goal**: Use `namedtuple("Asset", ["symbol", "shares", "price"])`.
* **Requirement**: Create 3 asset records, calculate total portfolio value `sum(a.shares * a.price for a in portfolio)`, and print formatted summary.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Classroom Grade Registry & Ranked Leaderboard
* **Goal**: Interactively ingest student tuples `(name, score)`, calculate class mean/min/max, filter honor roll and failing lists with comprehensions, and print a sorted leaderboard.

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
<summary><b>🔍 View Exercise Solutions (Grade Analytics & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Classroom Grade Analytics
# =====================================================================
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

scores_list = [score for _, score in student_records]

total_students = len(student_records)
class_average = sum(scores_list) / total_students
top_score = max(scores_list)
lowest_score = min(scores_list)

honor_students = [name for name, score in student_records if score >= 90.0]
failing_students = [name for name, score in student_records if score < 60.0]

sorted_records = sorted(student_records, key=lambda x: x[1], reverse=True)

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

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
queue = []
queue.extend(["Task 1", "Task 2", "Task 3"])
first = queue.pop(0)
last = queue.pop()
print(f"Popped First: {first}, Popped Last: {last}, Remaining: {queue}")

# Ex 2:
data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
print(f"First 3: {data[:3]}, Last 3: {data[-3:]}, Every 2nd: {data[::2]}, Rev: {data[::-1]}")

# Ex 3:
grades = [78.5, 92.0, 64.0, 88.5, 99.0]
grades.sort()
grades.reverse()
print(f"High: {grades[0]}, Low: {grades[-1]}")

# Ex 4:
temperatures = [28.5, -999.0, 32.0, 31.5, -999.0, 29.0]
temps_f = [(c * 9/5) + 32 for c in temperatures if c != -999.0]
print(f"Temps (F): {temps_f}")

# Ex 5:
server_rec = ("192.168.1.1", 8080, "PRODUCTION", True)
ip, port, env, is_active = server_rec
ip, env = env, ip
print(f"Swapped: ip={ip}, env={env}")

# Ex 6:
logs = ["user_login", "page_view", "user_login", "checkout", "page_view"]
seen = set()
unique_logs = [x for x in logs if not (x in seen or seen.add(x))]
print(f"Unique Ordered: {unique_logs}")

# Ex 7:
import copy
team = [["Alice", 90], ["Bob", 85]]
shallow, deep = team.copy(), copy.deepcopy(team)
team[0][1] = 100
print(f"Shallow Alice Score: {shallow[0][1]}, Deep Alice Score: {deep[0][1]}")

# Ex 8:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"Transposed: {transposed}")

# Ex 9:
from collections import namedtuple
Asset = namedtuple("Asset", ["symbol", "shares", "price"])
portfolio = [Asset("AAPL", 50, 180.0), Asset("GOOGL", 20, 140.0), Asset("NVDA", 30, 450.0)]
tot_val = sum(a.shares * a.price for a in portfolio)
print(f"Portfolio Total Value: ${tot_val:,.2f}")
```
</details>
