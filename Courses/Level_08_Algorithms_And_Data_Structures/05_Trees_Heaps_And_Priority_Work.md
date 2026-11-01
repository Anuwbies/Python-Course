# Lesson 5: Trees, Heaps & Priority Work

**Prerequisites:** Levels 1–7 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Trees_Heaps_And_Priority_Work.py`.

Distinguish a structure for hierarchical relationships from a structure for repeatedly selecting the next priority. Similar tree-shaped drawings do not imply identical ordering rules.

## 1. Interpret a tree's shape

A tree connects parent and child relationships without a cycle. A binary tree has at most two children per node. Traversal order determines when a node is visited relative to its children: preorder visits the parent first, inorder places it between left and right, and postorder visits it last.

A binary search tree adds an ordering invariant. Its operation cost depends on height; a balanced shape can support logarithmic-height navigation, while a chain can degrade to linear height. Merely naming an object Tree does not establish balance.

## 2. Understand the heap invariant

A min-heap keeps each parent no greater than its children, making the minimum available at the root. It does not keep the whole list in fully sorted order. heapq uses a list representation and provides heappush and heappop to maintain the invariant.

```python
import heapq
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
print(heapq.heappop(heap))  # 1
```

Popping an empty heap raises IndexError. Use while heap for a complete drain. A heap is useful when values arrive over time and the next minimum is needed repeatedly; a one-time complete sorted report may be simpler with sorted.

## 3. Give tied priorities a rule

A tuple compares lexicographically. Store `(priority, sequence, item)` so equal priorities are resolved by an insertion sequence. This makes ordering stable and avoids asking Python to compare arbitrary item objects that may not support ordering.

Do not mutate a priority inside an already stored item and assume the heap repairs itself. Updating priorities often uses a new entry and a policy for ignoring obsolete entries, as the shortest-path lesson demonstrates.

## 4. Choose the representation from the operation

A catalog hierarchy, an ordered search tree, and a priority queue solve different problems. State the required operations and invariants before choosing. Complexity claims include both update and selection costs, plus any extra state used to handle ties or obsolete entries.

Recursion may express a tree walk cleanly, but deep externally supplied trees may require an explicit stack. Review total visited nodes and maximum depth separately; the shape determines how much pending work must be retained.

References: [Heap queues](https://docs.python.org/3.13/library/heapq.html).

## Cost model

Heap insertion and removal take O(log n) time under the usual bounded-cost comparison model. Inserting all n jobs individually costs O(n log n); heapify can build an existing list in O(n), but draining it still costs O(n log n). The full priority-order task retains O(n) work state. A tree traversal visits O(n) nodes, with pending recursion or stack space determined by its height and traversal strategy.

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which item leaves a min-heap first.
2. **Explain:** Explain why the heap list is not a fully sorted report.
3. **Modify:** Add an insertion sequence to make equal priorities stable.
4. **Debug:** Find a priority update that changes an item without maintaining the heap invariant.

<details>
<summary>Hints</summary>

The sequence field provides a deterministic tie policy before the label is compared.

</details>

## Independent task: trees, heaps & priority work

In `Practice/05_Trees_Heaps_And_Priority_Work.py`, complete this task:

Define `priority_order(jobs)` for `(priority, label)` pairs with valid integer priorities. Use heapq and an insertion sequence to return labels in ascending priority order, preserving input order for ties. Do not mutate jobs. Demonstrate `[(2,"normal"),(1,"first"),(1,"second")]`.

Expected output:

```text
['first', 'second', 'normal']
```
