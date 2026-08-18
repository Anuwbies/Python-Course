# Lesson 1: Big-O Notation & Computational Complexity Analysis

Understanding algorithm complexity is the foundation of computer science. It allows engineers to predict and compare how algorithms scale as input sizes grow to millions or billions of elements.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand and compute Time Complexity and Space Complexity.
2. Master common Big-O classes: $O(1)$, $O(\log n)$, $O(n)$, $O(n \log n)$, $O(n^2)$, and $O(2^n)$.
3. Know the internal algorithmic complexity of Python built-in operations (lists vs sets vs dicts).
4. Measure wall-clock runtime vs theoretical complexity.

---

## 1. Big-O Complexity Hierarchy

$$\text{Fastest} \longrightarrow O(1) < O(\log n) < O(n) < O(n \log n) < O(n^2) < O(2^n) < O(n!) \longrightarrow \text{Slowest}$$

| Notation | Name | Typical Example | Behavior as $N=1,000,000$ |
| :--- | :--- | :--- | :--- |
| **$O(1)$** | Constant | Dict key lookup, list index access | Instant (~1 operation) |
| **$O(\log n)$** | Logarithmic | Binary search in sorted array | ~20 operations |
| **$O(n)$** | Linear | Searching an unsorted list, single loop | 1,000,000 operations |
| **$O(n \log n)$** | Linearithmic | Merge Sort, Timsort (`list.sort()`) | ~20,000,000 operations |
| **$O(n^2)$** | Quadratic | Nested loops, Bubble sort | $1,000,000,000,000$ (Freeze!) |

---

## 2. Python Built-in Complexity Cheat Sheet

| Data Structure | Operation | Average Complexity | Worst Case |
| :--- | :--- | :--- | :--- |
| **List** | `list[i]` (Index access) | $O(1)$ | $O(1)$ |
| **List** | `list.append(x)` | $O(1)$ (amortized) | $O(n)$ |
| **List** | `list.insert(0, x)` / `list.pop(0)` | **$O(n)$** (shifts all elements) | $O(n)$ |
| **List** | `x in list` (Linear search) | **$O(n)$** | $O(n)$ |
| **Dict / Set** | `key in dict` / `x in set` | **$O(1)$** (Hash table lookup) | $O(n)$ (hash collisions) |
| **Deque** | `deque.appendleft(x)` / `popleft()` | **$O(1)$** (Doubly linked list) | $O(1)$ |

```python
# Demonstrating O(n) vs O(1) lookup
large_list = list(range(1_000_000))
large_set = set(range(1_000_000))

# ❌ 999,999 in large_list -> O(n): Checks 1,000,000 elements sequentially
# ✅ 999,999 in large_set  -> O(1): Hashes number and jumps directly to bucket
```

---

## 📝 Quick Exercise

**Prompt**:
Analyze the Big-O time complexity of this function:
```python
def find_pairs(nums, target):
    pairs = []
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                pairs.append((nums[i], nums[j]))
    return pairs
```
How can you optimize this to $O(n)$ using a hash set?

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

### 1. Analysis:
The original implementation contains nested loops iterating through $N$ elements, resulting in **$O(n^2)$ Quadratic Time Complexity**.

### 2. $O(n)$ Optimized Solution:
```python
def find_pairs_optimized(nums: list[int], target: int) -> list[tuple[int, int]]:
    seen = set()
    pairs = []
    for num in nums:
        complement = target - num
        if complement in seen: # O(1) hash set lookup!
            pairs.append((complement, num))
        seen.add(num)
    return pairs

# Time Complexity: O(n) Linear Time
# Space Complexity: O(n) Linear Space
```
</details>

---

## 🧠 Self-Check Quiz

1. **Why is `deque.popleft()` faster than `list.pop(0)` for large collections?**
   - A) `deque` is written in C++, list is in Python
   - B) `list.pop(0)` must shift all remaining $N-1$ elements in memory ($O(n)$), while `deque` adjusts a pointer in $O(1)$
   - C) `deque` automatically drops duplicate values
   - D) There is no speed difference
   *(Answer: B)*
