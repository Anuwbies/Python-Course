# Lesson 4: Searching, Sorting & Order

**Prerequisites:** Levels 1–7 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Searching_Sorting_And_Order.py`.

Use ordering to reduce search work, and account for the cost of obtaining that order. A binary-search contract includes its sorted-input precondition and its duplicate policy.

## 1. Keep a shrinking interval

Binary search compares a middle value and excludes the portion that cannot contain the desired answer. A half-open interval `[low, high)` makes the stopping condition low < high and permits an insertion position at the end.

For a leftmost occurrence, move low past values strictly smaller than target and move high to middle otherwise. At termination, low identifies the first possible position. Check that it is in range and actually contains the target before returning an index.

```python
from bisect import bisect_left
values = [1, 3, 5, 5, 8]
position = bisect_left(values, 5)
print(position)  # 2
```

The standard library's bisect_left finds an insertion boundary, not a guaranteed match. An insertion point can refer to a different value or the position after the final element.

## 2. State the ordering assumption

Binary search requires a compatible sorted order. It does not sort or validate the whole input automatically. Checking every element for sortedness adds linear work, so describe whether that validation is part of the measured operation.

Sorting first can be worthwhile for many searches, but one search may not justify that preprocessing. Compare workloads honestly: building once and querying repeatedly answers a different question from receiving a fresh unordered collection for every query.

## 3. Preserve or change the collection deliberately

`sorted(values)` returns a new list. `values.sort()` changes the list in place and returns None. Python's sorting is stable: records with equal sort keys retain their relative order. A key function describes the ordering without rewriting the records.

Sorting does not imply deduplication. Repeated values remain unless a separate uniqueness rule is applied. A report that needs the first matching record should state what first means under its selected ordering.

## 4. Handle boundaries and duplicates

Include empty data, a target before the first value, a target after the last, and repeated targets. Off-by-one mistakes often appear only at these boundaries. Use a trace of low, high, and middle rather than randomly changing plus/minus one operations.

Avoid claiming logarithmic total work when a function copies or sorts the whole input on every call. The search loop can be logarithmic while the complete public operation has additional linear or sorting costs.

References: [Bisect](https://docs.python.org/3.13/library/bisect.html), [Sorting HOWTO](https://docs.python.org/3.13/howto/sorting.html).

## Cost model

The shrinking binary-search interval gives O(log n) comparisons and O(1) auxiliary search state, assuming constant-time indexing and bounded-cost comparisons. Sorting a fresh input adds its own cost; a conventional comparison-sort analysis uses O(n log n) worst-case time, while adaptive implementations can exploit existing order. The supplied search deliberately does not hide a sort or full-input validation inside that bound.

## Practice: predict, explain, modify, debug

1. **Predict:** Trace the left boundary for a repeated target.
2. **Explain:** Explain why an insertion position is not necessarily a match.
3. **Modify:** Compare an empty list and a target beyond the final value.
4. **Debug:** Find a binary search that fails to shrink its interval.

<details>
<summary>Hints</summary>

Keep high exclusive and make each iteration strictly reduce the interval.

</details>

## Independent task: searching, sorting & order

In `Practice/04_Searching_Sorting_And_Order.py`, complete this task:

Implement `leftmost_index(values, target)` with a binary-search loop over an already sorted ascending integer list. Return the first matching index or -1. Do not sort, copy, or mutate the input. Print results for targets 5 and 4 in `[1, 3, 5, 5, 8]`.

Expected output:

```text
2
-1
```
