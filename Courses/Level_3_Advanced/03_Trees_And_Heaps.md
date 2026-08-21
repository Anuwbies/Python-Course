# Lesson 3: Non-Linear Hierarchies: Trees, Binary Search & Priority Heaps

Linear structures (like lists and queues) are constrained by sequential ordering. When systems require hierarchical data representations (such as filesystem directories, DOM structures, or database indexing) and fast logarithmic searching, **Tree** data structures are required. In this lesson, you will master **Binary Search Trees (BST)**, tree traversals, and **Priority Heaps** using Python's `heapq` module.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand non-linear hierarchical tree structures (Nodes, Roots, Edges, Leaves, Subtrees).
2. Implement custom **Binary Search Trees (BST)** maintaining the BST ordering invariant.
3. Master Depth-First Tree Traversals: **In-Order**, **Pre-Order**, and **Post-Order**.
4. Understand Binary Min-Heaps and Max-Heaps and their underlying array representation.
5. Utilize Python's built-in `heapq` module to implement $\mathcal{O}(\log n)$ **Priority Queues**.

---

## 1. Binary Search Trees (BST)

A Binary Search Tree is a binary tree where every node adheres to the **BST Invariant**:
- All keys in the **left subtree** are strictly less than the node's key: $\text{Left} < \text{Node}$.
- All keys in the **right subtree** are strictly greater than the node's key: $\text{Right} > \text{Node}$.

```
         [ 50 ]
        /      \
    [ 30 ]    [ 70 ]
    /    \    /    \
 [ 20 ] [ 40 ][ 60 ][ 80 ]
```

```python
class TreeNode:
    def __init__(self, key: int, value: any):
        self.key = key
        self.value = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None

class BinarySearchTree:
    def __init__(self):
        self.root: TreeNode | None = None

    def insert(self, key: int, value: any) -> None:
        """Inserts key-value pair in O(log n) average time."""
        if not self.root:
            self.root = TreeNode(key, value)
        else:
            self._insert_node(self.root, key, value)

    def _insert_node(self, current: TreeNode, key: int, value: any) -> None:
        if key < current.key:
            if current.left is None:
                current.left = TreeNode(key, value)
            else:
                self._insert_node(current.left, key, value)
        elif key > current.key:
            if current.right is None:
                current.right = TreeNode(key, value)
            else:
                self._insert_node(current.right, key, value)
        else:
            current.value = value # Update existing key

    def search(self, key: int) -> any | None:
        """Searches for key in O(log n) time."""
        current = self.root
        while current:
            if key == current.key:
                return current.value
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None
```

---

## 2. Tree Traversals

1. **In-Order (Left $\to$ Root $\to$ Right)**: Visits nodes in ascending sorted key order.
2. **Pre-Order (Root $\to$ Left $\to$ Right)**: Used for deep cloning or serializing tree topology.
3. **Post-Order (Left $\to$ Right $\to$ Root)**: Used for bottom-up directory size calculations and tree deletion.

```python
def traverse_in_order(node: TreeNode | None, result: list) -> None:
    if node:
        traverse_in_order(node.left, result)
        result.append((node.key, node.value))
        traverse_in_order(node.right, result)
```

---

---

## 4. Balanced Trees & Production Indexing (AVL, Red-Black & B-Trees)

When inserting pre-sorted data ($1 \to 2 \to 3 \to 4 \to 5$) into a naive BST, the tree degenerates into a singly linked list with disastrous $\mathcal{O}(n)$ search performance. Production engines solve this through **Self-Balancing Trees**:

- **AVL Trees**: Strictly balanced with height difference (balance factor) between left and right subtrees $\le 1$, maintained via tree rotations.
- **Red-Black Trees**: Used in C++ `std::map` and Linux CFS process scheduler, requiring at most 2 rotations per insertion.
- **B-Trees / B+ Trees**: High branching factor trees designed for block-storage disk drives and relational database indexes (PostgreSQL, MySQL InnoDB), minimizing disk I/O seek operations.

---

## 5. Under the Hood: $\mathcal{O}(n)$ `heapq.heapify` vs $\mathcal{O}(n \log n)$ Pushes

Building a heap from an existing list can be performed in **$\mathcal{O}(n)$ linear time** using Floyd's build-heap algorithm (`heapq.heapify()`), whereas iteratively calling `heappush()` takes $\mathcal{O}(n \log n)$:

```python
import heapq

raw_scores = [45, 12, 89, 23, 7, 66]
# Transforms list in-place into valid Min-Heap in O(n) time:
heapq.heapify(raw_scores)
print(raw_scores) # [7, 12, 66, 23, 45, 89]
```

---

## 6. Breadth-First Search (BFS) / Level-Order Tree Traversal

While DFS traversals use recursion (call stack), Level-Order traversal explores nodes horizon-by-horizon using a FIFO Queue (`deque`):

```python
from collections import deque

def level_order_traversal(root: TreeNode | None) -> list[list[int]]:
    if not root: return []
    levels = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        current_level = []
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node.key)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        levels.append(current_level)
    return levels
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master trees, BST validation, DFS/BFS traversals, and priority heaps:

---

### 🟢 Tier 1: BST Construction & Heap Basics (Exercises 1–3)

#### 🔹 Exercise 1: Calculate Maximum Depth of Binary Tree
* **Goal**: Write recursive `max_depth(root: TreeNode) -> int` returning the maximum path length from root to leaf.

#### 🔹 Exercise 2: Top $K$ Smallest Elements with `heapq`
* **Goal**: Use `heapq.nsmallest(k, arr)` and custom min-heap to extract top 3 lowest prices in $\mathcal{O}(n \log k)$ time.

#### 🔹 Exercise 3: Leaf Node Counter
* **Goal**: Implement `count_leaves(root: TreeNode) -> int` counting nodes with no children.

---

### 🟡 Tier 2: Validations & Traversals (Exercises 4–6)

#### 🔹 Exercise 4: Validate Binary Search Tree (BST Invariant)
* **Goal**: Write `is_valid_bst(root: TreeNode) -> bool` validating that every node strictly adheres to left/right bounding constraints $(-\infty, \infty)$.

#### 🔹 Exercise 5: Lowest Common Ancestor (LCA) in BST
* **Goal**: Find the lowest common ancestor node for two given keys in a BST in $\mathcal{O}(\log n)$ time.

#### 🔹 Exercise 6: In-Order Successor in BST
* **Goal**: Find the node with the smallest key strictly greater than a given target key.

---

### 🟠 Tier 3: Heap Architectures & Inversions (Exercises 7–9)

#### 🔹 Exercise 7: Invert / Mirror Binary Tree
* **Goal**: Invert a binary tree in-place by swapping left and right child pointers at every level.

#### 🔹 Exercise 8: Top $K$ Frequent Elements with Min-Heap
* **Goal**: Given an array of strings, return the $K$ most frequent elements in $\mathcal{O}(n \log k)$ time using `Counter` and a Min-Heap.

#### 🔹 Exercise 9: Merge $K$ Sorted Streams with Min-Heap
* **Goal**: Merge $K$ sorted lists of integers into a single sorted list in $\mathcal{O}(N \log K)$ time using `heapq`.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Real-Time CPU Priority Process Dispatcher
* **Goal**: Build an RTOS process priority scheduler using Min-Heaps and custom `__lt__` task structures.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Hospital Emergency Room Real-Time Triage & Surgical Priority Queue**, combining a Binary Search Tree (for patient lookup by medical ID) with a Min-Heap Priority Queue (for emergency doctor dispatch):

```python
# =====================================================================
# REAL-WORLD SYSTEM: Hospital Emergency Triage & Medical Records Engine
# =====================================================================

import heapq
from datetime import datetime

# 1. Medical Record Node for BST (Lesson 3 BST)
class PatientRecordNode:
    def __init__(self, patient_id: int, name: str, blood_type: str):
        self.patient_id = patient_id # Unique numeric identifier
        self.name = name
        self.blood_type = blood_type
        self.left: PatientRecordNode | None = None
        self.right: PatientRecordNode | None = None


class PatientRecordRegistryBST:
    """Binary Search Tree indexing patient historical charts in O(log n) time."""
    def __init__(self):
        self.root = None

    def insert(self, patient_id: int, name: str, blood_type: str) -> None:
        new_node = PatientRecordNode(patient_id, name, blood_type)
        if not self.root:
            self.root = new_node
            return

        curr = self.root
        while True:
            if patient_id < curr.patient_id:
                if curr.left is None:
                    curr.left = new_node
                    break
                curr = curr.left
            elif patient_id > curr.patient_id:
                if curr.right is None:
                    curr.right = new_node
                    break
                curr = curr.right
            else:
                curr.name = name
                curr.blood_type = blood_type
                break

    def lookup(self, patient_id: int) -> PatientRecordNode | None:
        curr = self.root
        while curr:
            if patient_id == curr.patient_id:
                return curr
            curr = curr.left if patient_id < curr.patient_id else curr.right
        return None

    def get_all_records_sorted(self) -> list[tuple[int, str, str]]:
        """In-order traversal yielding sorted patient ID ledger."""
        records = []
        def _in_order(node):
            if node:
                _in_order(node.left)
                records.append((node.patient_id, node.name, node.blood_type))
                _in_order(node.right)
        _in_order(self.root)
        return records


# 2. Emergency Room Dispatch Priority Queue (Lesson 3 Heaps)
class EmergencyTriageDispatcher:
    """Min-Heap Priority Queue dispatching patients by clinical severity."""
    def __init__(self):
        self._heap = []
        self._counter = 0 # Tie-breaker for identical severity scores

    def enqueue_patient(self, severity_rank: int, patient_id: int, chief_complaint: str) -> None:
        # Severity rank 1 = Resuscitation (highest priority), Rank 4 = Standard
        self._counter += 1
        entry = (severity_rank, self._counter, patient_id, chief_complaint)
        heapq.heappush(self._heap, entry)

    def dispatch_next_patient(self, registry: PatientRecordRegistryBST) -> dict | None:
        if not self._heap:
            return None
        severity, _, patient_id, complaint = heapq.heappop(self._heap)
        chart = registry.lookup(patient_id)
        name = chart.name if chart else "UNKNOWN PATIENT"
        blood = chart.blood_type if chart else "N/A"
        return {
            "severity_level": severity,
            "patient_id": patient_id,
            "name": name,
            "blood_type": blood,
            "complaint": complaint
        }


# 3. Execution Simulation
registry = PatientRecordRegistryBST()
# Index patient medical records into BST
registry.insert(1045, "Elena Rostova", "O+")
registry.insert(1012, "Marcus Vance", "A-")
registry.insert(1089, "Sarah Connor", "AB+")
registry.insert(1005, "David Kim", "B+")

triage = EmergencyTriageDispatcher()
# Arriving emergency cases
triage.enqueue_patient(severity_rank=3, patient_id=1012, chief_complaint="Sprained ankle")
triage.enqueue_patient(severity_rank=1, patient_id=1089, chief_complaint="Severe cardiac arrest")
triage.enqueue_patient(severity_rank=2, patient_id=1045, chief_complaint="Deep laceration with bleeding")

print("=" * 75)
print(f"{'HOSPITAL EMERGENCY TRIAGE & BST REGISTRY DISPATCH':^75}")
print("=" * 75)
print("IN-ORDER SORTED PATIENT REGISTRY (BST In-Order Traversal):")
for pid, name, blood in registry.get_all_records_sorted():
    print(f"  Chart #{pid:<6} | {name:<20} | Blood Type: {blood}")

print("-" * 75)
print("EMERGENCY OPERATING THEATER DISPATCH ORDER (Min-Heap):")
while triage._heap:
    p = triage.dispatch_next_patient(registry)
    print(f"  🚨 [SEVERITY {p['severity_level']}] Patient: {p['name']:<18} (#{p['patient_id']}) -> {p['complaint']}")

print("=" * 75)
```

### 🔍 Code Explanation:
- **`PatientRecordRegistryBST`**: Provides $\mathcal{O}(\log n)$ record searching by integer patient ID, while `get_all_records_sorted()` utilizes In-Order DFS traversal to yield sorted output.
- **`heapq` Min-Heap**: Organizes emergency cases so that severe Level 1 cardiac incidents immediately pop ahead of Level 3 minor injuries regardless of chronological arrival time.
- **Tie-Breaking Tuples**: `(severity, self._counter, ...)` prevents comparison errors when two patients present with identical triage severity rankings.

---

## 📝 Quick Exercise: Operating System Process Priority Scheduler

### 🏢 Real-Life Scenario
You are developing the CPU process scheduler for a real-time operating system (RTOS). Running tasks have varying priority levels (Priority 1 = Kernel Interrupt, Priority 5 = Background Disk Defrag) and execution durations. You will implement a Min-Heap Task Scheduler that continuously dispatches and executes highest-priority tasks first.

### 📋 Requirements
1. **Define Class `CPUTask`**:
   - Attributes: `priority: int`, `pid: str`, `task_name: str`, `duration_ms: int`.
   - Implement `__lt__(self, other: 'CPUTask') -> bool`: Compares `self.priority < other.priority` (ensures Min-Heap ordering).
2. **Define Class `KernelPriorityScheduler`**:
   - Uses `heapq` to manage an internal list `self._task_heap: list[CPUTask] = []`.
   - `add_task(self, task: CPUTask) -> None`: Uses `heapq.heappush()` to insert the task.
   - `execute_all(self) -> list[str]`: While the heap is not empty, pops tasks with `heapq.heappop()` and returns execution log strings.
3. Submit multiple tasks in mixed priority order and verify that execution occurs strictly in priority sequence.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 Min-Heaps and `heapq` with Level 2 dunders (`__lt__`) and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
         KERNEL CPU PRIORITY SCHEDULER            
==================================================
[DISPATCHED] PID: KERNEL-01 | Priority: 1 | Hardware Interrupt Handler (5ms)
[DISPATCHED] PID: NET-04    | Priority: 2 | Socket Packet Ingest (12ms)
[DISPATCHED] PID: AUDIO-09  | Priority: 3 | Real-Time Audio Mixer (20ms)
[DISPATCHED] PID: BKG-99    | Priority: 5 | Background Log Compression (150ms)
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Scheduler & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Kernel CPU Priority Scheduler
# =====================================================================
import heapq

class CPUTask:
    def __init__(self, priority: int, pid: str, task_name: str, duration_ms: int):
        self.priority = priority
        self.pid = pid
        self.task_name = task_name
        self.duration_ms = duration_ms

    def __lt__(self, other: 'CPUTask') -> bool:
        return self.priority < other.priority

    def __str__(self) -> str:
        return f"[DISPATCHED] PID: {self.pid:<10} | Priority: {self.priority} | {self.task_name} ({self.duration_ms}ms)"


class KernelPriorityScheduler:
    def __init__(self):
        self._heap: list[CPUTask] = []

    def add_task(self, task: CPUTask) -> None:
        heapq.heappush(self._heap, task)

    def execute_all(self) -> None:
        print("==================================================")
        print("         KERNEL CPU PRIORITY SCHEDULER            ")
        print("==================================================")
        while self._heap:
            task = heapq.heappop(self._heap)
            print(task)
        print("==================================================")


scheduler = KernelPriorityScheduler()
scheduler.add_task(CPUTask(priority=5, pid="BKG-99", task_name="Background Log Compression", duration_ms=150))
scheduler.add_task(CPUTask(priority=1, pid="KERNEL-01", task_name="Hardware Interrupt Handler", duration_ms=5))
scheduler.add_task(CPUTask(priority=3, pid="AUDIO-09", task_name="Real-Time Audio Mixer", duration_ms=20))
scheduler.add_task(CPUTask(priority=2, pid="NET-04", task_name="Socket Packet Ingest", duration_ms=12))

scheduler.execute_all()

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
class TreeNode:
    def __init__(self, key=0, val=None, left=None, right=None):
        self.key, self.val, self.left, self.right = key, val, left, right

# Ex 1: Maximum Depth of Binary Tree
def max_depth(root: TreeNode | None) -> int:
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Ex 2: Top K Smallest Elements with heapq
def top_k_smallest(arr: list[int], k: int) -> list[int]:
    return heapq.nsmallest(k, arr)

# Ex 3: Count Leaf Nodes
def count_leaves(root: TreeNode | None) -> int:
    if not root: return 0
    if not root.left and not root.right: return 1
    return count_leaves(root.left) + count_leaves(root.right)

# Ex 4: Validate BST Invariant
def is_valid_bst(root: TreeNode | None, min_val=float('-inf'), max_val=float('inf')) -> bool:
    if not root: return True
    if not (min_val < root.key < max_val): return False
    return is_valid_bst(root.left, min_val, root.key) and is_valid_bst(root.right, root.key, max_val)

# Ex 5: LCA in BST
def lowest_common_ancestor(root: TreeNode, p: int, q: int) -> TreeNode:
    curr = root
    while curr:
        if p < curr.key and q < curr.key: curr = curr.left
        elif p > curr.key and q > curr.key: curr = curr.right
        else: return curr

# Ex 6: In-Order Successor in BST
def inorder_successor(root: TreeNode, target_key: int) -> TreeNode | None:
    successor = None
    curr = root
    while curr:
        if curr.key > target_key:
            successor = curr
            curr = curr.left
        else:
            curr = curr.right
    return successor

# Ex 7: Invert Binary Tree
def invert_tree(root: TreeNode | None) -> TreeNode | None:
    if not root: return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

# Ex 8: Top K Frequent Elements
from collections import Counter
def top_k_frequent(words: list[str], k: int) -> list[str]:
    counts = Counter(words)
    # Min-Heap of size k: (freq, word)
    return [item[0] for item in counts.most_common(k)]

# Ex 9: Merge K Sorted Lists
def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    heap = []
    for i, lst in enumerate(lists):
        if lst: heapq.heappush(heap, (lst[0], i, 0))
    res = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        res.append(val)
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    return res
```
</details>
