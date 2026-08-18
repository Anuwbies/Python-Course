# Lesson 5: Advanced Sorting, Searching & Algorithmic Patterns

In this lesson, you will master classic divide-and-conquer algorithms and critical competitive programming patterns.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Implement **Binary Search** ($O(\log n)$).
2. Implement **Merge Sort** ($O(n \log n)$ divide-and-conquer).
3. Implement **Quick Sort** with in-place partitioning.
4. Master core patterns: Two-Pointers and Sliding Window.

---

## 1. Binary Search ($O(\log n)$)

```python
def binary_search(sorted_arr: list[int], target: int) -> int:
    """Returns index of target, or -1 if not found."""
    left = 0
    right = len(sorted_arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

---

## 2. Merge Sort ($O(n \log n)$ Stable Sort)

```python
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)

def _merge(left: list[int], right: list[int]) -> list[int]:
    sorted_merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            sorted_merged.append(left[i])
            i += 1
        else:
            sorted_merged.append(right[j])
            j += 1

    sorted_merged.extend(left[i:])
    sorted_merged.extend(right[j:])
    return sorted_merged
```

---

## 📝 Quick Exercise

**Prompt**:
Implement the **Two-Pointer Pattern** to find two numbers in a sorted array that sum up to a `target` value in $O(n)$ time and $O(1)$ space.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def two_sum_sorted(arr: list[int], target: int) -> tuple[int, int] | None:
    left = 0
    right = len(arr) - 1

    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (arr[left], arr[right])
        elif current_sum < target:
            left += 1  # Need larger sum, move left pointer right
        else:
            right -= 1 # Need smaller sum, move right pointer left
    return None

# Test:
sorted_numbers = [2, 7, 11, 15, 18, 22]
print(two_sum_sorted(sorted_numbers, 25)) # (7, 18)
```
</details>
