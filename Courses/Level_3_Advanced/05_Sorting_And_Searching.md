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

## 4. Timsort Internals

Python's built-in `.sort()` and `sorted()` use **Timsort** (created by Tim Peters in 2002 for CPython):
- **Hybrid Algorithm**: Combines Merge Sort with Insertion Sort.
- **Adaptive**: Identifies already-sorted subsequences ("natural runs") in raw data.
- **Stable**: Elements with equal keys preserve their original relative order.
- **Complexity**: $\mathcal{O}(n)$ best case (already sorted), $\mathcal{O}(n \log n)$ average/worst case.

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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Custom Merge Sort for Order Book (Level 3)
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


# 2. Binary Search on Sorted Orders (Level 3)
def binary_search_order(orders: list[dict], target_price: float) -> int:
    left = 0
    right = len(orders) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_price = orders[mid]["price"]
        if mid_price == target_price:
            return mid
        # Assuming descending sorted order
        elif mid_price < target_price:
            right = mid - 1
        else:
            left = mid + 1
    return -1


# 3. Execution Run
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
```

**Explanation of the Solution:**
- `merge_sort_orders` sorts financial dictionaries in guaranteed $\mathcal{O}(n \log n)$ time.
- `binary_search_order` locates specific limit orders in $\mathcal{O}(\log n)$ time over sorted arrays.
</details>
