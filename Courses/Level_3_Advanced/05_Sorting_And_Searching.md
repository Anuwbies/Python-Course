# Lesson 5: Sorting & Searching: Binary Search, Merge Sort & Timsort

Ordering and querying structured datasets efficiently is among the most heavily studied problems in computer science. Sorting unlocks logarithmic $\mathcal{O}(\log n)$ searching and enables efficient deduplication, database indexing, and data compression. In this lesson, you will master **Binary Search**, divide-and-conquer sorting algorithms (**Merge Sort**, **Quick Sort**), and explore CPython's native **Timsort** engine.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Implement **Binary Search** from scratch and understand its logarithmic $\mathcal{O}(\log n)$ scaling.
2. Utilize Python's standard `bisect` library for high-speed binary searching and sorted list insertion.
3. Master the Divide-and-Conquer paradigm by implementing **Merge Sort** ($\mathcal{O}(n \log n)$ stable sort).
4. Understand **Quick Sort** partitioning and pivot selection strategies.
5. Understand **Timsort** (Python's native hybrid sorting algorithm) and write advanced multi-key `key` functions.

---

## 1. Binary Search: $\mathcal{O}(\log n)$

Binary search eliminates half of the remaining search space on every iteration, requiring that the input sequence is pre-sorted:

```python
def binary_search(sorted_arr: list[int], target: int) -> int:
    """Returns the index of target in sorted_arr, or -1 if not found."""
    left = 0
    right = len(sorted_arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1 # Search right half
        else:
            right = mid - 1 # Search left half
    return -1
```

---

## 2. Python's Standard `bisect` Module

The built-in `bisect` module implements binary search algorithms in optimized C:

```python
import bisect

sorted_scores = [60, 70, 80, 90, 95]

# Find insertion point (where 85 belongs):
idx = bisect.bisect_left(sorted_scores, 85) # Index 3

# Fast grading rubric lookup using bisect:
def get_letter_grade(score: float) -> str:
    breakpoints = [60, 70, 80, 90]
    grades = ["F", "D", "C", "B", "A"]
    i = bisect.bisect_right(breakpoints, score)
    return grades[i]

print(get_letter_grade(88.5)) # "B"
```

---

## 3. Merge Sort: Divide & Conquer ($\mathcal{O}(n \log n)$)

Merge Sort recursively splits the array into two halves, sorts each half, and merges the sorted halves back together:

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])

    return _merge(left_half, right_half)

def _merge(left: list[int], right: list[int]) -> list[int]:
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

---

---

## 5. QuickSort & In-Place Partitioning (Lomuto vs Hoare)

QuickSort selects a **pivot** and partitions elements into two sub-arrays (less than pivot vs greater than pivot):
- **Lomuto Partition**: Simple pointer swap iteration.
- **Hoare Partition**: Dual two-pointer scans from both ends inward (requires $3\times$ fewer swaps than Lomuto).
- **Pivot Selection Pitfall**: Choosing `arr[0]` causes catastrophic $\mathcal{O}(n^2)$ degradation on pre-sorted arrays. Production implementations select **Median-of-Three** (`median(first, middle, last)`).

```python
def quicksort(arr: list[int]) -> list[int]:
    """In-place or divide-and-conquer QuickSort."""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

---

## 6. Sorting Stability & The $\Omega(n \log n)$ Lower Bound

### 1. Stability
A sort is **stable** if elements with identical keys maintain their original relative order. In multi-column database queries (e.g. `SORT BY lastName, THEN BY age`), Timsort and Merge Sort guarantee stability; QuickSort and HeapSort do not.

### 2. Comparison Sort Lower Bound
Any comparison-based sort can be modeled as a binary decision tree with $n!$ leaves. The minimum tree depth is:
$$\text{Depth} \ge \log_2(n!) = \Omega(n \log n)$$
To beat $n \log n$, non-comparison algorithms (**Counting Sort**, **Radix Sort**) exploit integer digit properties to achieve **$\mathcal{O}(n + k)$ linear time**.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master binary search variations, divide-and-conquer sorting, and multi-key ranking:

---

### 🟢 Tier 1: Binary Search Basics & Custom Keys (Exercises 1–3)

#### 🔹 Exercise 1: First and Last Position in Sorted Array
* **Goal**: Write binary search finding the starting and ending index of a target value in $\mathcal{O}(\log n)$ time.

#### 🔹 Exercise 2: Multi-Key List Sorting with Lambdas
* **Goal**: Sort a list of employees by department (ascending) and salary (descending) using `sorted(..., key=lambda x: (...))`.

#### 🔹 Exercise 3: Bisect Insertion into Live Sorted Feed
* **Goal**: Use `bisect.insort` to maintain an ordered stream of stock trade prices dynamically.

---

### 🟡 Tier 2: Search Space Reduction & Rotations (Exercises 4–6)

#### 🔹 Exercise 4: Search in Rotated Sorted Array
* **Goal**: Search for a target in a sorted array that has been rotated at an unknown pivot in $\mathcal{O}(\log n)$ time.

#### 🔹 Exercise 5: Find Peak Element
* **Goal**: Find a local maximum element in an array using modified binary search in $\mathcal{O}(\log n)$ time.

#### 🔹 Exercise 6: Integer Square Root via Binary Search
* **Goal**: Compute $\lfloor\sqrt{x}\rfloor$ for integer $x$ in $\mathcal{O}(\log x)$ time without using `math.sqrt()` or `** 0.5`.

---

### 🟠 Tier 3: Advanced Sorting & Non-Comparison Algorithms (Exercises 7–9)

#### 🔹 Exercise 7: In-Place QuickSort with Hoare Partition
* **Goal**: Implement in-place QuickSort using two-pointer partitioning without allocating sub-lists.

#### 🔹 Exercise 8: Counting Sort for Bounded Integers
* **Goal**: Implement Counting Sort sorting an array of 1,000,000 numbers in range $[0, 100]$ in $\mathcal{O}(n + k)$ linear time.

#### 🔹 Exercise 9: Kth Largest Element via Quickselect
* **Goal**: Find the $K$th largest element in an unsorted array in $\mathcal{O}(n)$ average time using Hoare's Quickselect algorithm.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Securities Exchange Order Book Engine
* **Goal**: Implement a dual Merge Sort and Binary Search limit order book engine matching incoming market trades at target price levels.

---

---

## 💻 Code Example & Reference

The following real-life program models a **High-Traffic E-Commerce Catalog Sorting, Multi-Key Ranking & Price-Band Bisect Search Engine**, demonstrating custom Merge Sort, `bisect` price range queries, and multi-key Timsort lambdas:

```python
# =====================================================================
# REAL-WORLD SYSTEM: E-Commerce Product Search & Price-Band Indexer
# =====================================================================

import bisect

class ProductCatalogItem:
    def __init__(self, sku: str, title: str, price: float, rating: float, sales_count: int):
        self.sku = sku
        self.title = title
        self.price = price
        self.rating = rating
        self.sales_count = sales_count

    def __repr__(self) -> str:
        return f"{self.sku:<8} | {self.title:<28} | ${self.price:>7.2f} | ⭐ {self.rating:.1f} | {self.sales_count:>5} sold"


class ProductCatalogEngine:
    def __init__(self, items: list[ProductCatalogItem]):
        self.items = items
        # Create sorted index by price for binary range search (Lesson 5)
        self.sorted_by_price = sorted(self.items, key=lambda x: x.price)
        self._price_keys = [item.price for item in self.sorted_by_price]

    # Binary Search Price Range Query via bisect (Lesson 5)
    def query_price_band(self, min_price: float, max_price: float) -> list[ProductCatalogItem]:
        left_idx = bisect.bisect_left(self._price_keys, min_price)
        right_idx = bisect.bisect_right(self._price_keys, max_price)
        return self.sorted_by_price[left_idx:right_idx]

    # Multi-Key Stable Ranking (Timsort)
    def rank_by_popularity_and_rating(self) -> list[ProductCatalogItem]:
        # Sort primary by rating descending, secondary by sales_count descending
        return sorted(self.items, key=lambda x: (x.rating, x.sales_count), reverse=True)


# Catalog Dataset
catalog = [
    ProductCatalogItem("SKU-101", "Mechanical Keyboard", 129.99, 4.8, 1420),
    ProductCatalogItem("SKU-102", "Ergonomic Optical Mouse", 49.50, 4.6, 3800),
    ProductCatalogItem("SKU-103", "4K UltraWide Monitor", 499.00, 4.9, 850),
    ProductCatalogItem("SKU-104", "USB-C Braided Cable 2m", 14.99, 4.2, 12000),
    ProductCatalogItem("SKU-105", "Noise-Cancelling Headset", 199.95, 4.7, 2100),
    ProductCatalogItem("SKU-106", "Aluminum Laptop Stand", 39.99, 4.5, 4500),
    ProductCatalogItem("SKU-107", "Desk Pad Large Mat", 24.50, 4.8, 6200),
]

engine = ProductCatalogEngine(catalog)

print("=" * 80)
print(f"{'E-COMMERCE CATALOG SEARCH & BISECT PRICE-BAND ENGINE':^80}")
print("=" * 80)

# 1. Binary Range Search via bisect
print("\n--- 1. FILTER PRODUCTS IN PRICE BAND: $30.00 TO $150.00 (Bisect Logarithmic Range) ---")
price_band_results = engine.query_price_band(30.00, 150.00)
for p in price_band_results:
    print(f"  {p}")

# 2. Multi-Key Ranked Popularity Sort
print("\n--- 2. TOP POPULARITY & RATING LEADERBOARD (Timsort Multi-Key) ---")
ranked_results = engine.rank_by_popularity_and_rating()
for rank, p in enumerate(ranked_results, start=1):
    print(f"  #{rank} {p}")

print("=" * 80)
```

### 🔍 Code Explanation:
- **`bisect_left` & `bisect_right`**: Finds matching price slice boundaries in $\mathcal{O}(\log n)$ time without iterating over every product.
- **Multi-Key Sorting**: `key=lambda x: (x.rating, x.sales_count)` sorts by composite tuple priorities in a single stable Timsort pass.

---

## 📝 Quick Exercise: Stock Market Order Book Price Sorter & Binary Matcher

### 🏢 Real-Life Scenario
You are developing the matching engine for a financial securities exchange. Stock limit orders arrive asynchronously. The engine must maintain buy bids in descending price order and ask offers in ascending price order, and use Binary Search to quickly locate exact limit price matches.

### 📋 Requirements
1. **Define `binary_search_order(orders: list[dict], target_price: float) -> int`**:
   - `orders` is a pre-sorted list of orders by `price`.
   - Implement Binary Search to locate the exact index of `target_price` in $\mathcal{O}(\log n)$ time.
   - Return index if found; else `-1`.
2. **Define Custom `merge_sort_orders(orders: list[dict], ascending: bool = True) -> list[dict]`**:
   - Implements recursive Merge Sort to sort dictionaries by `order["price"]`.
   - If `ascending=False`, sorts in descending order (highest bids first).
3. Test sorting raw incoming market orders and executing binary search lookups.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 Merge Sort and Binary Search with Level 1 dictionaries, lists, and string formatting.

### 🎯 Expected Output
```text
==================================================
       SECURITIES EXCHANGE ORDER BOOK ENGINE      
==================================================
SORTED BUY BIDS (Descending Merge Sort):
  - BID #1: $185.50 (Qty: 500)
  - BID #2: $184.25 (Qty: 1200)
  - BID #3: $183.10 (Qty: 800)
  - BID #4: $180.00 (Qty: 250)
--------------------------------------------------
BINARY SEARCH LIMIT ORDER LOOKUP ($184.25):
  ✓ MATCH FOUND at Index #1: Order with price $184.25 and quantity 1200
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Order Book & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Securities Exchange Order Book Engine
# =====================================================================
def merge_sort_orders(orders: list[dict], ascending: bool = True) -> list[dict]:
    if len(orders) <= 1:
        return orders

    mid = len(orders) // 2
    left = merge_sort_orders(orders[:mid], ascending)
    right = merge_sort_orders(orders[mid:], ascending)

    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        condition = (left[i]["price"] <= right[j]["price"]) if ascending else (left[i]["price"] >= right[j]["price"])
        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def binary_search_order(orders: list[dict], target_price: float) -> int:
    left = 0
    right = len(orders) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_price = orders[mid]["price"]
        if mid_price == target_price:
            return mid
        elif mid_price < target_price:
            right = mid - 1
        else:
            left = mid + 1
    return -1


raw_bids = [
    {"price": 183.10, "qty": 800},
    {"price": 185.50, "qty": 500},
    {"price": 180.00, "qty": 250},
    {"price": 184.25, "qty": 1200},
]

sorted_bids = merge_sort_orders(raw_bids, ascending=False)
match_idx = binary_search_order(sorted_bids, 184.25)

print("==================================================")
print("       SECURITIES EXCHANGE ORDER BOOK ENGINE      ")
print("==================================================")
print("SORTED BUY BIDS (Descending Merge Sort):")
for idx, bid in enumerate(sorted_bids, start=1):
    print(f"  - BID #{idx}: ${bid['price']:.2f} (Qty: {bid['qty']})")

print("--------------------------------------------------")
print("BINARY SEARCH LIMIT ORDER LOOKUP ($184.25):")
if match_idx != -1:
    matched = sorted_bids[match_idx]
    print(f"  ✓ MATCH FOUND at Index #{match_idx}: Order with price ${matched['price']:.2f} and quantity {matched['qty']}")
else:
    print("  ❌ No order matching target price.")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: First and Last Position in Sorted Array
def search_range(nums: list[int], target: int) -> list[int]:
    def find_bound(is_first):
        lo, hi, ans = 0, len(nums) - 1, -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                ans = mid
                if is_first: hi = mid - 1
                else: lo = mid + 1
            elif nums[mid] < target: lo = mid + 1
            else: hi = mid - 1
        return ans
    return [find_bound(True), find_bound(False)]

# Ex 2: Multi-Key List Sorting
employees = [("Eng", 95000), ("Sales", 110000), ("Eng", 120000)]
sorted_emp = sorted(employees, key=lambda x: (x[0], -x[1]))

# Ex 3: Bisect Insort
import bisect
live_feed = [10.5, 12.0, 15.2]
bisect.insort(live_feed, 11.4)

# Ex 4: Search Rotated Sorted Array
def search_rotated(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target: return mid
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]: hi = mid - 1
            else: lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]: lo = mid + 1
            else: hi = mid - 1
    return -1

# Ex 5: Find Peak Element
def find_peak(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[mid + 1]: hi = mid
        else: lo = mid + 1
    return lo

# Ex 6: Sqrt(x) via Binary Search
def my_sqrt(x: int) -> int:
    if x < 2: return x
    lo, hi, ans = 1, x // 2, 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            ans = mid
            lo = mid + 1
        else: hi = mid - 1
    return ans

# Ex 7: In-Place QuickSort
def quicksort_inplace(arr, lo=0, hi=None):
    if hi is None: hi = len(arr) - 1
    if lo < hi:
        pivot = arr[hi]
        i = lo
        for j in range(lo, hi):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[hi] = arr[hi], arr[i]
        quicksort_inplace(arr, lo, i - 1)
        quicksort_inplace(arr, i + 1, hi)
    return arr

# Ex 8: Counting Sort O(n+k)
def counting_sort(arr: list[int], max_val: int) -> list[int]:
    counts = [0] * (max_val + 1)
    for num in arr: counts[num] += 1
    res = []
    for val, count in enumerate(counts):
        res.extend([val] * count)
    return res

# Ex 9: Quickselect Kth Largest
def find_kth_largest(nums: list[int], k: int) -> int:
    target_idx = len(nums) - k
    def select(lo, hi):
        pivot = nums[hi]
        i = lo
        for j in range(lo, hi):
            if nums[j] <= pivot:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
        nums[i], nums[hi] = nums[hi], nums[i]
        if i == target_idx: return nums[i]
        elif i < target_idx: return select(i + 1, hi)
        else: return select(lo, i - 1)
    return select(0, len(nums) - 1)
```
</details>
