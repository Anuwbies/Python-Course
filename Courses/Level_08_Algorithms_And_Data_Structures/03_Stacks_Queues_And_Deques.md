# Lesson 3: Stacks, Queues & Deques

**Prerequisites:** Levels 1–7 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Stacks_Queues_And_Deques.py`.

Select the order in which pending work is processed. Last-in-first-out and first-in-first-out order lead to different algorithms even when they hold the same values.

## 1. Use a list as a stack

Appending and popping at the end implements a stack: the most recently added value is removed first. This suits nested delimiters because the most recent opening delimiter must be closed next.

```python
stack = []
stack.append("outer")
stack.append("inner")
print(stack.pop())  # inner
print(stack.pop())  # outer
```

Popping an empty stack raises IndexError. A parser should check its state before popping so an unmatched closing delimiter is reported according to its own contract, not as an accidental container failure.

## 2. Use deque for a queue

A queue processes older work first. collections.deque provides efficient append at the right and popleft at the left. Repeatedly removing index zero from a list shifts its remaining elements and can add avoidable work.

```python
from collections import deque
queue = deque(["first", "second"])
queue.append("third")
print(queue.popleft())  # first
```

Deque is appropriate for a single-process algorithmic queue; cross-thread coordination and blocking semantics require the corresponding concurrency tools later. A container choice alone does not supply a complete synchronization policy.

## 3. Track an invariant while scanning

For a parentheses-only balance check, the stack represents unmatched opening parentheses. On an opening character push; on a closing character reject an empty stack or pop one opener. At the end, an empty stack means no unmatched opener remains.

A count-only approach can handle one delimiter kind if it also rejects a negative running count, but it is insufficient to validate mixed delimiter nesting such as brackets and parentheses. The representation should reflect the rule you need to enforce.

## 4. Keep the source and work state separate

An algorithm can build its own stack or queue without modifying the caller's original sequence. That makes repeated calls meaningful and prevents a search from consuming a user's saved history.

State which non-delimiter characters are ignored or rejected. For this task they are ignored; a stricter language parser would need a richer syntax contract. Empty input is balanced because it contains no unmatched delimiters.

References: [Deque](https://docs.python.org/3.13/library/collections.html#collections.deque).

## Cost model

For a text of n characters, the parentheses scan visits each character once, giving O(n) time. Its stack can hold n unmatched opening characters, giving O(n) auxiliary space in the worst case. List append/end-pop have amortized constant-time behavior in the intended implementation model; deque end operations avoid shifting all remaining values.

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the removal order for the same values in a stack and queue.
2. **Explain:** Explain the unmatched-openers invariant during a scan.
3. **Modify:** Check empty input and a string beginning with a closing parenthesis.
4. **Debug:** Repair an implementation that pops before checking whether the stack is empty.

<details>
<summary>Hints</summary>

The stack contains only opening parentheses not yet matched.

</details>

## Independent task: stacks, queues & deques

In `Practice/03_Stacks_Queues_And_Deques.py`, complete this task:

Define balanced_parentheses(text) using a stack. Return True when parentheses are balanced, ignoring other characters, and False for an unmatched closer or remaining opener. Print results for `(a(b)c)`, `)(`, and the empty string.

Expected output:

```text
True
False
True
```
