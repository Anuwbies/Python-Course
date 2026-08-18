# Lesson 2: Custom Linear Data Structures: Linked Lists, Stacks & Queues

Linear data structures organize elements sequentially. Implementing them from scratch is essential for understanding dynamic memory allocation, pointers, and custom collection protocols.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Implement Singly and Doubly Linked Lists from scratch.
2. Build a LIFO (Last-In, First-Out) Stack with $O(1)$ push/pop.
3. Build a FIFO (First-In, First-Out) Queue.
4. Compare linked structures with contiguous dynamic arrays.

---

## 1. Singly Linked List Implementation

```python
from typing import Any, Optional

class Node:
    def __init__(self, data: Any, next_node: Optional['Node'] = None):
        self.data = data
        self.next = next_node

class LinkedList:
    def __init__(self):
        self.head: Optional[Node] = None
        self._size = 0

    def append(self, data: Any) -> None:
        """Appends to end in O(n) or O(1) if tracking tail."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data: Any) -> None:
        """Inserts at start in O(1) time."""
        self.head = Node(data, self.head)
        self._size += 1

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        return self._size
```

---

## 2. Stack (LIFO) & Queue (FIFO)

```python
class Stack:
    """LIFO Structure: Last In, First Out."""
    def __init__(self):
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        self._items.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        return self._items[-1] if not self.is_empty() else None

    def is_empty(self) -> bool:
        return len(self._items) == 0
```

---

## 📝 Quick Exercise

**Prompt**:
Write a function `is_valid_parentheses(s: str) -> bool` using a `Stack` to check if brackets `()`, `{}`, `[]` are correctly balanced and closed in valid order.
*(e.g., `"{[()]}"` $\rightarrow$ `True`, `"{[(])}"` $\rightarrow$ `False`).*

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def is_valid_parentheses(s: str) -> bool:
    stack = []
    bracket_map = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map.keys():
            if not stack or stack.pop() != bracket_map[char]:
                return False
        # Ignore other non-bracket characters if any

    return len(stack) == 0

# Test cases:
print(is_valid_parentheses("{[()]}")) # True
print(is_valid_parentheses("{[(])}")) # False
print(is_valid_parentheses("((()))")) # True
```
</details>
