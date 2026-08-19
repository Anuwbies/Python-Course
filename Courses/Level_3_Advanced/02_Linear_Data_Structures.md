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

## 3. Queues (First-In, First-Out: FIFO) & `collections.deque`

In a **Queue**, items enter at the back (enqueue) and exit from the front (dequeue).

> [!WARNING]
> Never use a Python `list` as a Queue with `list.pop(0)`. Each `pop(0)` takes $\mathcal{O}(n)$ time. Always use `collections.deque` which provides guaranteed $\mathcal{O}(1)$ push and pop operations from both ends!

```python
from collections import deque

# Fast O(1) Queue:
task_queue = deque()
task_queue.append("TASK-01")       # Enqueue
task_queue.append("TASK-02")
processed = task_queue.popleft()   # Dequeue in O(1) -> "TASK-01"
```

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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Stack-Based Bracket Validator (Level 3)
def is_bracket_syntax_balanced(code_snippet: str) -> tuple[bool, str]:
    matching_pairs = {')': '(', '}': '{', ']': '['}
    opening = {'(', '{', '['}
    stack = []

    for char in code_snippet:
        if char in opening:
            stack.append(char) # Push to stack (LIFO)
        elif char in matching_pairs:
            if not stack:
                return False, f"Unmatched closing bracket '{char}' without opening symbol"
            top = stack.pop()
            if top != matching_pairs[char]:
                return False, f"Mismatched bracket pair: expected closing for '{top}', got '{char}'"

    if stack:
        return False, f"Unclosed opening bracket '{stack[-1]}' remaining"

    return True, "Syntax brackets perfectly balanced"


# 2. Test Execution
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
```

**Explanation of the Solution:**
- A LIFO Stack stores opening symbols as they are encountered.
- When a closing bracket appears, popping the stack verifies that innermost nested expressions resolve first before outer blocks.
</details>
