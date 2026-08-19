# Lesson 1: Computational Complexity & Big-O Notation

Understanding algorithmic complexity is the foundational bridge separating junior coders from senior systems architects. As datasets scale from thousands to millions or billions of records, poorly chosen algorithms degrade from sub-second responses to system freeze. In this lesson, you will master theoretical Big-O notation, Time vs. Space Complexity, Amortized Analysis, and the internal complexity profiles of Python's built-in data structures.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Analyze and express algorithm performance using **Big-O ($\mathcal{O}$)**, Big-$\Omega$, and Big-$\Theta$ notation.
2. Master the core complexity classes: $\mathcal{O}(1)$, $\mathcal{O}(\log n)$, $\mathcal{O}(n)$, $\mathcal{O}(n \log n)$, $\mathcal{O}(n^2)$, and $\mathcal{O}(2^n)$.
3. Understand **Amortized Complexity** and Python dynamic array memory over-allocation.
4. Know the exact Time & Space complexities of Python built-in collections (`list`, `dict`, `set`, `deque`).
5. Benchmark and measure empirical wall-clock performance against theoretical expectations.

---

## 1. The Big-O Hierarchy

Big-O notation describes the upper bound of an algorithm's growth rate as input size $N$ approaches infinity ($N \to \infty$).

$$\text{Fastest} \longrightarrow \mathcal{O}(1) < \mathcal{O}(\log n) < \mathcal{O}(n) < \mathcal{O}(n \log n) < \mathcal{O}(n^2) < \mathcal{O}(2^n) < \mathcal{O}(n!) \longrightarrow \text{Slowest}$$

| Complexity | Name | Typical Example | Operations for $N = 1,000,000$ |
| :--- | :--- | :--- | :--- |
| $\mathcal{O}(1)$ | Constant | Hash map lookup, list index access | $1$ operation |
| $\mathcal{O}(\log n)$ | Logarithmic | Binary search in sorted array | $\approx 20$ operations |
| $\mathcal{O}(n)$ | Linear | Single linear scan through unsorted list | $1,000,000$ operations |
| $\mathcal{O}(n \log n)$ | Linearithmic | Merge Sort, Timsort (`list.sort()`) | $\approx 20,000,000$ operations |
| $\mathcal{O}(n^2)$ | Quadratic | Nested comparison loops, Bubble Sort | $1,000,000,000,000$ operations |
| $\mathcal{O}(2^n)$ | Exponential | Recursive Fibonacci without memoization | Uncomputable (Trillions of years) |

---

## 2. Python Built-In Data Structures Complexity Table

| Data Structure | Operation | Average Case | Worst Case | Underlying Implementation |
| :--- | :--- | :---: | :---: | :--- |
| **`list`** | Index: `list[i]` | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Contiguous pointer array |
| **`list`** | Append: `list.append(x)` | $\mathcal{O}(1)$ amortized | $\mathcal{O}(n)$ (resize copy) | Over-allocated dynamic array |
| **`list`** | Insert/Delete: `list.insert(0, x)`, `pop(0)` | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Shifts all downstream pointers in RAM |
| **`list`** | Containment: `x in list` | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ | Sequential linear scan |
| **`dict` / `set`** | Lookup / Insert / Delete: `d[k]`, `k in s` | $\mathcal{O}(1)$ | $\mathcal{O}(n)$ (collisions) | Combined hash table with open addressing |
| **`deque`** | Push/Pop Ends: `appendleft()`, `popleft()` | $\mathcal{O}(1)$ | $\mathcal{O}(1)$ | Doubly-linked block buffer |

---

## 3. Amortized Analysis: How Python Lists Grow

When a Python `list` runs out of pre-allocated memory during `append()`, CPython allocates a larger contiguous memory block (roughly $1.125 \times$ to $1.25 \times$ the current size) and copies all pointers over. 

Because resizes happen exponentially less frequently as the list grows, the expensive $\mathcal{O}(n)$ resize cost is spread out ("amortized") over thousands of fast $\mathcal{O}(1)$ operations, making the average append cost **$\mathcal{O}(1)$ amortized**.

---

## 💻 Code Example & Reference

The following real-life program models an **Algorithmic Complexity Benchmark: Two-Sum Transaction Matching Engine**, comparing an $\mathcal{O}(n^2)$ nested loop algorithm against an $\mathcal{O}(n)$ Hash-Map algorithm with empirical timing:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Frequency Transaction Reconciliation Benchmark
# =====================================================================

import time
import random

# Scenario: Financial ledger must find two offsetting transactions that sum to target amount
def find_offset_pair_quadratic(transactions: list[float], target_sum: float) -> tuple[float, float] | None:
    """Naive Quadratic Approach: O(n^2) Time Complexity, O(1) Space Complexity."""
    n = len(transactions)
    for i in range(n):
        for j in range(i + 1, n):
            if transactions[i] + transactions[j] == target_sum:
                return transactions[i], transactions[j]
    return None

def find_offset_pair_linear(transactions: list[float], target_sum: float) -> tuple[float, float] | None:
    """Optimized Hash-Set Approach: O(n) Time Complexity, O(n) Space Complexity."""
    seen_complements = set() # O(1) lookup hash table
    for amount in transactions:
        complement = target_sum - amount
        if complement in seen_complements: # O(1) check
            return complement, amount
        seen_complements.add(amount)
    return None


# Benchmark Execution Simulation
DATASET_SIZE = 15_000
random.seed(42)
test_transactions = [round(random.uniform(10.0, 5000.0), 2) for _ in range(DATASET_SIZE)]
# Insert known target pair
test_transactions[100] = 500.00
test_transactions[-50] = 1500.00
TARGET = 2000.00

print("=" * 75)
print(f"{'ALGORITHMIC COMPLEXITY BENCHMARK: O(n^2) vs O(n)':^75}")
print("=" * 75)
print(f"Synthesizing transaction dataset of N = {DATASET_SIZE:,} records...")

# Benchmark O(n^2)
start_quad = time.perf_counter()
quad_res = find_offset_pair_quadratic(test_transactions, TARGET)
time_quad_ms = (time.perf_counter() - start_quad) * 1000.0

# Benchmark O(n)
start_lin = time.perf_counter()
lin_res = find_offset_pair_linear(test_transactions, TARGET)
time_lin_ms = (time.perf_counter() - start_lin) * 1000.0

speedup_factor = time_quad_ms / time_lin_ms if time_lin_ms > 0 else 1.0

print("-" * 75)
print(f"{'Algorithm Approach':<25} | {'Big-O Time':<12} | {'Time (ms)':>15} | {'Result Pair':>15}")
print("-" * 75)
print(f"{'Nested Loop (Brute Force)':<25} | {'O(n^2)':<12} | {time_quad_ms:>13.2f} ms | {str(quad_res):>15}")
print(f"{'Hash Set Lookup':<25} | {'O(n)':<12} | {time_lin_ms:>13.2f} ms | {str(lin_res):>15}")
print("=" * 75)
print(f"🚀 Optimized O(n) algorithm is {speedup_factor:,.1f}x faster at N = {DATASET_SIZE:,}!")
print("=" * 75)
```

### 🔍 Code Explanation:
- **$\mathcal{O}(n^2)$ Analysis**: The nested loop compares every element against every other element, performing $\frac{N(N-1)}{2} \approx 112,500,000$ operations.
- **$\mathcal{O}(n)$ Optimization**: By using a hash `set()`, we trade $\mathcal{O}(n)$ auxiliary memory for a single linear pass that completes in only $\approx 15,000$ operations.
- **Performance Gap**: The hash map approach executes in under a millisecond, demonstrating why algorithmic complexity governs real-world throughput.

---

## 📝 Quick Exercise: Duplicate Detection Algorithmic Optimizer & Performance Profiler

### 🏢 Real-Life Scenario
You are developing the deduplication module for an enterprise data warehouse ingesting customer lead records. The current legacy implementation uses a list-membership check (`if item in seen_list:`), which degrades exponentially as the customer dataset grows. You must write an optimized $\mathcal{O}(n)$ deduplication engine and verify that it correctly preserves the first occurrence order.

### 📋 Requirements
1. **Define `deduplicate_naive_quadratic(records: list[str]) -> list[str]`**:
   - Iterates through `records`.
   - Uses an internal list `seen = []`. If `item not in seen`, appends to `seen`.
   - Big-O: $\mathcal{O}(n^2)$ time due to `x in list` scanning $\mathcal{O}(n)$ per element.
2. **Define `deduplicate_optimized_linear(records: list[str]) -> list[str]`**:
   - Uses a combination of a hash `set()` for $\mathcal{O}(1)$ presence checks and an output list to maintain original order.
   - Big-O: $\mathcal{O}(n)$ time and $\mathcal{O}(n)$ space.
3. Compare both implementations over a test list of customer email leads, ensuring identical deduplication outputs.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 computational complexity analysis with Level 1 lists, sets, loops, and f-string reporting.

### 🎯 Expected Output
```text
==================================================
        LEAD DEDUPLICATION ENGINE BENCHMARK       
==================================================
Total Raw Leads:      8
Unique Leads Found:   5
--------------------------------------------------
DEDUPLICATED CUSTOMER STREAM (Order Preserved):
  1. alice@corp.com
  2. bob@startup.io
  3. charlie@enterprise.net
  4. elena@cloud.com
  5. david@agency.org
--------------------------------------------------
COMPLEXITY COMPARISON:
  - Naive List Scan:     O(n^2) Quadratic
  - Hash Set Optimized:  O(n)   Linear
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Quadratic Deduplication (O(n^2))
def deduplicate_naive_quadratic(records: list[str]) -> list[str]:
    seen = []
    for item in records:
        if item not in seen: # O(n) linear scan on every iteration
            seen.append(item)
    return seen


# 2. Optimized Linear Deduplication (O(n))
def deduplicate_optimized_linear(records: list[str]) -> list[str]:
    seen_set = set() # O(1) hash table lookup
    unique_ordered = []
    for item in records:
        if item not in seen_set: # O(1) check
            seen_set.add(item)
            unique_ordered.append(item)
    return unique_ordered


# 3. Verification & Execution Run
sample_leads = [
    "alice@corp.com",
    "bob@startup.io",
    "alice@corp.com",
    "charlie@enterprise.net",
    "bob@startup.io",
    "elena@cloud.com",
    "david@agency.org",
    "alice@corp.com"
]

res_naive = deduplicate_naive_quadratic(sample_leads)
res_optimized = deduplicate_optimized_linear(sample_leads)

assert res_naive == res_optimized # Guarantees algorithmic parity

print("==================================================")
print("        LEAD DEDUPLICATION ENGINE BENCHMARK       ")
print("==================================================")
print(f"Total Raw Leads:      {len(sample_leads)}")
print(f"Unique Leads Found:   {len(res_optimized)}")
print("--------------------------------------------------")
print("DEDUPLICATED CUSTOMER STREAM (Order Preserved):")
for idx, lead in enumerate(res_optimized, start=1):
    print(f"  {idx}. {lead}")
print("--------------------------------------------------")
print("COMPLEXITY COMPARISON:")
print("  - Naive List Scan:     O(n^2) Quadratic")
print("  - Hash Set Optimized:  O(n)   Linear")
print("==================================================")
```

**Explanation of the Solution:**
- `deduplicate_naive_quadratic` performs an $\mathcal{O}(n)$ list scan inside an $\mathcal{O}(n)$ loop, resulting in $\mathcal{O}(n^2)$ quadratic slowdown.
- `deduplicate_optimized_linear` tracks seen elements using an $\mathcal{O}(1)$ hash set while appending new items to a list, achieving true $\mathcal{O}(n)$ linear speed while preserving insertion ordering.
</details>
