# Lesson 3: Non-Linear Data Structures: Trees & Heaps

Non-linear hierarchical data structures allow fast hierarchical searching, indexing, priority ordering, and routing.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Implement a **Binary Search Tree (BST)** from scratch.
2. Master tree traversals (In-order, Pre-order, Post-order, Level-order).
3. Understand tree balancing and AVL / Red-Black concepts.
4. Implement and utilize **Min/Max Heaps** for Priority Queues (`heapq`).

---

## 1. Binary Search Tree (BST) Implementation

In a BST, every left child is smaller than the parent node, and every right child is greater.

```python
from typing import Optional

class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

class BinarySearchTree:
    def __init__(self):
        self.root: Optional[TreeNode] = None

    def insert(self, val: int) -> None:
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert_recursive(self.root, val)

    def _insert_recursive(self, node: TreeNode, val: int) -> None:
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
            else:
                self._insert_recursive(node.left, val)
        else:
            if node.right is None:
                node.right = TreeNode(val)
            else:
                self._insert_recursive(node.right, val)

    def in_order_traversal(self, node: Optional[TreeNode]) -> list[int]:
        """In-order (Left -> Root -> Right) returns sorted array for BST!"""
        if not node:
            return []
        return self.in_order_traversal(node.left) + [node.val] + self.in_order_traversal(node.right)
```

---

## 2. Priority Queues with `heapq` (Min-Heap)

A **Binary Heap** is a complete binary tree where the parent node is always smaller than (or equal to) its children (Min-Heap).

```python
import heapq

# Priority queue storing (priority_level, task_name)
tasks = []
heapq.heappush(tasks, (3, "Low priority cleanup"))
heapq.heappush(tasks, (1, "CRITICAL: Server crash"))
heapq.heappush(tasks, (2, "Medium priority email"))

# Pops the highest priority item in O(log n) time:
priority, task = heapq.heappop(tasks)
print(f"Executing: {task} (Priority {priority})")
# Output: CRITICAL: Server crash (Priority 1)
```

---

## 📝 Quick Exercise

**Prompt**:
Implement a `search(val: int) -> bool` method on `BinarySearchTree` that searches for a value in $O(\log n)$ average time.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def search(self, val: int) -> bool:
    current = self.root
    while current is not None:
        if current.val == val:
            return True
        elif val < current.val:
            current = current.left
        else:
            current = current.right
    return False

# Attach to BinarySearchTree class:
BinarySearchTree.search = search

# Test:
bst = BinarySearchTree()
for num in [50, 30, 70, 20, 40, 60, 80]:
    bst.insert(num)

print(bst.search(40)) # True
print(bst.search(99)) # False
```
</details>
