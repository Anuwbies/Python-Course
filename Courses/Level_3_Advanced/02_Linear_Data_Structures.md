# Lesson 2: Linear Data Structures: Linked Lists, Stacks & Queues

While Python's built-in `list` is versatile, it is backed by a contiguous dynamic array. This makes prepending (`list.insert(0, x)`) or removing from the front (`list.pop(0)`) an expensive $\mathcal{O}(n)$ operation that shifts all downstream pointers in memory. In this lesson, you will build foundational linear data structures from scratch: **Singly Linked Lists**, **Doubly Linked Lists**, **Stacks (LIFO)**, and **Queues (FIFO)**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Implement pointer-based **Node** structures.
2. Build custom **Singly & Doubly Linked Lists** with $\mathcal{O}(1)$ head insertion and deletion.
3. Understand pointer mutation mechanics and avoid orphan memory leaks.
4. Implement **Stacks (LIFO)** for undo/redo buffers and syntax parsing.
5. Implement **Queues (FIFO)** and utilize `collections.deque` for fast $\mathcal{O}(1)$ double-ended queue operations.

---

## 1. Singly Linked Lists

A Linked List consists of discrete `Node` objects distributed non-contiguously in memory, linked together by pointers:

```
[ Head: 10 | next ] ───> [ 20 | next ] ───> [ 30 | next: None ] ───> None
```

```python
class Node:
    def __init__(self, data: any, next_node: 'Node' = None):
        self.data = data
        self.next = next_node

class SinglyLinkedList:
    def __init__(self):
        self.head: Node | None = None
        self._size = 0

    def insert_head(self, data: any) -> None:
        """O(1) Prepend operation."""
        new_node = Node(data, next_node=self.head)
        self.head = new_node
        self._size += 1

    def append(self, data: any) -> None:
        """O(n) Append without tail pointer."""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        return self._size
```

---

## 2. Stacks (Last-In, First-Out: LIFO)

In a **Stack**, items are inserted and removed strictly from one end (the "top").

$$\text{Push}(A) \longrightarrow \text{Push}(B) \longrightarrow \text{Pop}() \implies B \text{ is removed first}$$

```python
class Stack:
    """O(1) LIFO Stack implementation."""
    def __init__(self):
        self._items = []

    def push(self, item: any) -> None:
        self._items.append(item) # O(1)

    def pop(self) -> any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop() # O(1)

    def peek(self) -> any:
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0
```

---

---

## 4. Doubly Linked Lists & Sentinel Nodes

In a **Doubly Linked List**, each node points to both its `next` and `prev` neighbors. To eliminate tedious `if head is None` boundary checks, modern systems utilize **Sentinel (Dummy) Nodes**:

```
[ Dummy Head ] <════> [ Node A ] <════> [ Node B ] <════> [ Dummy Tail ]
```

```python
class DNode:
    def __init__(self, key: int = 0, val: int = 0):
        self.key, self.val = key, val
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = DNode() # Sentinel Head
        self.tail = DNode() # Sentinel Tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_first(self, node: DNode) -> None:
        """Insert right after dummy head in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def remove(self, node: DNode) -> None:
        """Delete arbitrary node in O(1) without list traversal."""
        node.prev.next = node.next
        node.next.prev = node.prev
```

---

## 5. Ring Buffer / Circular Queue

A **Circular Buffer** utilizes a fixed-size contiguous array with `head` and `tail` pointers wrapping around using modulo arithmetic: `(tail + 1) % capacity`. It enables high-speed zero-allocation streaming across audio drivers and lock-free concurrency queues.

---

## 6. Memory & CPU Cache Locality: Arrays vs Linked Lists

| Dimension | Dynamic Array (`list`) | Linked List (`Node`) |
| :--- | :--- | :--- |
| **Memory Layout** | Contiguous chunk in RAM | Scattered heap allocations |
| **CPU Cache Hits** | **High** (hardware prefetching loads adjacent items) | **Low** (pointer chasing causes cache misses) |
| **Memory Overhead** | Low (only pointer array + over-allocation) | High (every node stores `data`, `prev`, `next` pointers) |
| **Prepend / Pop(0)** | $\mathcal{O}(n)$ expensive | $\mathcal{O}(1)$ immediate pointer redirect |

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master linked data structures, stacks, queues, and pointer mechanics:

---

### 🟢 Tier 1: Singly Linked Basics & Basic Stacks (Exercises 1–3)

#### 🔹 Exercise 1: Singly Linked List Search
* **Goal**: Write `.contains(target)` returning `True` if target exists in the singly linked list.

#### 🔹 Exercise 2: Stack-Based String Reverser
* **Goal**: Write `reverse_string_with_stack(text: str) -> str` using only `push` and `pop`.

#### 🔹 Exercise 3: Queue-Based Ticket Counter Simulator
* **Goal**: Model customer arrivals and departures using `collections.deque`.

---

### 🟡 Tier 2: Pointer Reversals & Cycle Detection (Exercises 4–6)

#### 🔹 Exercise 4: In-Place Singly Linked List Reversal
* **Goal**: Reverse a singly linked list in-place in $\mathcal{O}(n)$ time and $\mathcal{O}(1)$ auxiliary space by redirecting `.next` pointers.

#### 🔹 Exercise 5: Floyd's Cycle Detection (Tortoise and Hare)
* **Goal**: Implement `has_cycle(head: Node) -> bool` using slow and fast pointers.

#### 🔹 Exercise 6: Find Middle Node in a Single Pass
* **Goal**: Use fast/slow pointers to find the middle node of a linked list without computing its length first.

---

### 🟠 Tier 3: Advanced Linear Structures & Monotonic Stacks (Exercises 7–9)

#### 🔹 Exercise 7: Monotonic Decreasing Stack (Next Greater Element)
* **Goal**: Given an array of numbers, return the next greater element for each index in $\mathcal{O}(n)$ time using a monotonic stack.

#### 🔹 Exercise 8: Minimum Stack with $\mathcal{O}(1)$ `get_min()`
* **Goal**: Implement `MinStack` supporting `push`, `pop`, `top`, and `get_min()` all in $\mathcal{O}(1)$ time.

#### 🔹 Exercise 9: LRU (Least Recently Used) Cache
* **Goal**: Implement an `LRUCache(capacity)` combining a Hash Map (`dict`) with a Doubly Linked List for $\mathcal{O}(1)$ get and put.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Compiler Syntax Bracket & Nested Expression Validator
* **Goal**: Build a production-grade compiler linting stack validator checking matching brackets, braces, and tags across source code.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Undo/Redo Command Stack & Operating System Job Spooler**, combining custom Linked Lists, Stacks, and Double-Ended Queues:

```python
# =====================================================================
# REAL-WORLD SYSTEM: OS Task Scheduler & Text Editor Undo/Redo Engine
# =====================================================================

from collections import deque
from typing import NamedTuple

# 1. Action Record for Undo/Redo Stack (Lesson 2 Stacks)
class EditorAction(NamedTuple):
    action_type: str # 'INSERT' or 'DELETE'
    text: str
    cursor_position: int

class TextEditorSession:
    """Models document editing with dual Undo and Redo LIFO Stacks."""

    def __init__(self):
        self._buffer: list[str] = []
        self._undo_stack: list[EditorAction] = [] # LIFO
        self._redo_stack: list[EditorAction] = [] # LIFO

    @property
    def current_text(self) -> str:
        return "".join(self._buffer)

    def type_text(self, text: str) -> None:
        pos = len(self._buffer)
        self._buffer.extend(list(text))
        self._undo_stack.append(EditorAction("INSERT", text, pos))
        self._redo_stack.clear() # New action invalidates redo tree

    def undo(self) -> bool:
        if not self._undo_stack:
            return False
        action = self._undo_stack.pop()
        if action.action_type == "INSERT":
            # Remove inserted characters from buffer
            del self._buffer[action.cursor_position : action.cursor_position + len(action.text)]
            self._redo_stack.append(action)
            return True
        return False

    def redo(self) -> bool:
        if not self._redo_stack:
            return False
        action = self._redo_stack.pop()
        if action.action_type == "INSERT":
            self._buffer.extend(list(action.text))
            self._undo_stack.append(action)
            return True
        return False


# 2. Operating System Print/Job FIFO Queue with Deque (Lesson 2 Queues)
class PrintJobSpooler:
    def __init__(self):
        self._queue = deque()

    def submit_job(self, document_name: str, pages: int) -> None:
        self._queue.append({"doc": document_name, "pages": pages})
        print(f"🖨️ [SPOOLED] '{document_name}' ({pages} pages) placed in print queue.")

    def process_next_job(self) -> dict | None:
        if not self._queue:
            return None
        # O(1) FIFO removal from front
        job = self._queue.popleft()
        print(f"⚙️ [PRINTING] '{job['doc']}' ({job['pages']} pages) dispatched to hardware printer.")
        return job


# 3. Execution Simulation
print("=" * 70)
print(f"{'TEXT EDITOR UNDO/REDO & PRINTER SPOOLER DEMO':^70}")
print("=" * 70)

# Test Editor Stack
editor = TextEditorSession()
editor.type_text("Hello ")
editor.type_text("World!")
print(f"Initial Text:    '{editor.current_text}'")

editor.undo()
print(f"After Undo #1:   '{editor.current_text}'")

editor.redo()
print(f"After Redo #1:   '{editor.current_text}'")

print("-" * 70)
# Test Print Spooler Queue
spooler = PrintJobSpooler()
spooler.submit_job("Quarterly_Financials.pdf", 42)
spooler.submit_job("Employee_Handbook.docx", 120)
spooler.submit_job("Flight_Ticket.pdf", 2)

print("\n--- Disagreeing / Emptying Queue (FIFO) ---")
while spooler._queue:
    spooler.process_next_job()

print("=" * 70)
```

### 🔍 Code Explanation:
- **LIFO Stacks**: `TextEditorSession` uses two stacks (`_undo_stack` and `_redo_stack`) to model reversible historical state.
- **FIFO Deque**: `PrintJobSpooler` utilizes `collections.deque.popleft()` to provide $\mathcal{O}(1)$ arrival-order job dispatching without list memory reshuffling.

---

## 📝 Quick Exercise: Code Syntax Syntax Bracket & Tag Balance Validator

### 🏢 Real-Life Scenario
You are developing a compiler linting tool and code formatting validator (such as ESLint or Prettier). When a developer writes code, the parser must verify that all opening grouping symbols (`(`, `{`, `[`) are properly closed and matched in the exact reverse order of nesting. You will implement a Stack-based balance checker.

### 📋 Requirements
1. **Define `is_bracket_syntax_balanced(code_snippet: str) -> tuple[bool, str]`**:
   - Matching pairs dictionary: `MATCHING_PAIRS = {')': '(', '}': '{', ']': '['}`
   - Opening brackets set: `OPENING = {'(', '{', '['}`
   - Use a Python `list` as a **LIFO Stack**.
   - Iterate over characters in `code_snippet`:
     - If character is in `OPENING`: Push onto stack.
     - If character is a closing bracket (in `MATCHING_PAIRS`):
       - If stack is empty: Return `False, f"Unmatched closing bracket '{char}' without opening symbol"`.
       - Pop the top opening bracket from the stack. If it does not match `MATCHING_PAIRS[char]`, return `False, f"Mismatched bracket pair: expected closing for '{top}', got '{char}'"`.
   - After iteration:
     - If stack is not empty: Return `False, f"Unclosed opening bracket '{stack[-1]}' remaining"`.
     - Otherwise: Return `True, "Syntax brackets perfectly balanced"`.
2. Test valid and invalid code snippets and print verification logs.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 Stack LIFO algorithms with Level 1 dictionaries, sets, loops, conditionals, and tuples.

### 🎯 Expected Output
```text
==================================================
      COMPILER SYNTAX BRACKET VALIDATOR           
==================================================
  ✓ PASS: def calculate(a, b): return [(a + b) * {2: True}[2]]
  ✗ FAIL: if (user.is_active: return {data: [1, 2, 3]} -> Unmatched closing bracket '}' without opening symbol
  ✗ FAIL: const array = [(1 + 2) * 3; -> Unclosed opening bracket '[' remaining
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Bracket Validator & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Compiler Syntax Bracket Validator
# =====================================================================
def is_bracket_syntax_balanced(code_snippet: str) -> tuple[bool, str]:
    matching_pairs = {')': '(', '}': '{', ']': '['}
    opening = {'(', '{', '['}
    stack = []

    for char in code_snippet:
        if char in opening:
            stack.append(char)
        elif char in matching_pairs:
            if not stack:
                return False, f"Unmatched closing bracket '{char}' without opening symbol"
            top = stack.pop()
            if top != matching_pairs[char]:
                return False, f"Mismatched bracket pair: expected closing for '{top}', got '{char}'"

    if stack:
        return False, f"Unclosed opening bracket '{stack[-1]}' remaining"

    return True, "Syntax brackets perfectly balanced"


test_snippets = [
    "def calculate(a, b): return [(a + b) * {2: True}[2]]",
    "if (user.is_active: return {data: [1, 2, 3]}",
    "const array = [(1 + 2) * 3;",
]

print("==================================================")
print("      COMPILER SYNTAX BRACKET VALIDATOR           ")
print("==================================================")

for code in test_snippets:
    is_ok, msg = is_bracket_syntax_balanced(code)
    tag = "✓ PASS:" if is_ok else "✗ FAIL:"
    print(f"  {tag} {code} -> {msg}")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Singly Linked List Search
class Node:
    def __init__(self, data, nxt=None): self.data, self.next = data, nxt

def search_linked_list(head: Node, target) -> bool:
    curr = head
    while curr:
        if curr.data == target: return True
        curr = curr.next
    return False

# Ex 2: Stack-Based String Reversal
def reverse_string_with_stack(text: str) -> str:
    stack = list(text)
    return "".join(stack.pop() for _ in range(len(stack)))

# Ex 3: Queue-Based Ticket Simulator
from collections import deque
def simulate_ticket_queue(customers):
    q = deque(customers)
    served = []
    while q:
        served.append(q.popleft())
    return served

# Ex 4: In-Place Singly Linked List Reversal O(n) Time, O(1) Space
def reverse_list(head: Node) -> Node | None:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# Ex 5: Floyd's Cycle Detection (Tortoise and Hare)
def has_cycle(head: Node) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast: return True
    return False

# Ex 6: Single-Pass Middle Node
def find_middle_node(head: Node) -> Node | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

# Ex 7: Monotonic Decreasing Stack (Next Greater Element)
def next_greater_element(nums: list[int]) -> list[int]:
    res = [-1] * len(nums)
    stack = [] # stores indices
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            res[idx] = num
        stack.append(i)
    return res

# Ex 8: MinStack with O(1) get_min()
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)

    def pop(self) -> int:
        self.min_stack.pop()
        return self.stack.pop()

    def get_min(self) -> int:
        return self.min_stack[-1]

# Ex 9: LRU Cache (Hash Map + Doubly Linked List)
class DNode:
    def __init__(self, k=0, v=0): self.k, self.v, self.prev, self.next = k, v, None, None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = DNode(), DNode()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node: DNode):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert(self, node: DNode):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._insert(node)
            return node.v
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self._remove(self.cache[key])
        node = DNode(key, value)
        self._insert(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.k]
```
</details>
