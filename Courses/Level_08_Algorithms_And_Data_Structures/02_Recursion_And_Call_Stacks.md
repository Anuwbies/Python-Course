# Lesson 2: Recursion & Call Stacks

**Prerequisites:** Levels 1–7 and Lesson 1 of this level. **Practice file:** `Practice/02_Recursion_And_Call_Stacks.py`.

Describe a problem in terms of a smaller instance with a reachable base case. Recursion changes the control structure; it does not remove the need to show progress and bound resource use.

## 1. Separate the base and recursive cases

A factorial satisfies 0! = 1 and n! = n times (n-1)! for positive integers. The base case supplies a result without another recursive call. Every recursive step moves toward it.

```python
def factorial(number):
    if number == 0:
        return 1
    return number * factorial(number - 1)

print(factorial(4))  # 24
```

For 4, the calls descend through 3, 2, 1, and 0. Results then return upward: 1, 1, 2, 6, 24. Each call has its own local number and its pending multiplication, retained on the call stack.

## 2. State the valid domain

A negative argument in that definition moves farther from zero and does not reach the base case. Validate the domain before recursing. A noninteger argument is also outside the intended discrete sequence.

Python limits recursion depth and does not promise tail-call elimination. Increasing the limit is not a general solution for a poorly bounded input. An iterative implementation can avoid call-stack growth for a simple factorial or linear traversal.

## 3. Measure all work, not only depth

A recursion tree can contain many calls at the same depth. A naive Fibonacci recursion repeats subproblems and can grow exponentially even though its maximum depth grows linearly. Memoization trades additional storage for avoiding repeated results; it is a design choice whose key and lifetime need a contract.

For tree traversal, total calls may be proportional to nodes while depth depends on tree shape. A balanced tree and a long chain can therefore have similar visit counts but very different stack requirements.

## 4. Convert when the stack is the wrong resource

An explicit stack can represent pending work with a loop. This is especially useful for deeply nested or externally supplied data. Do not replace recursion just to avoid the word; compare clarity, depth, and failure behavior for the actual problem.

When debugging, trace one small input by hand before adding print statements to every recursive call. Identify the base result, progress measure, and combination operation. A missing return can break the upward result flow even when the descent looks correct.

References: [Interpreter recursion limit](https://docs.python.org/3.13/library/sys.html#sys.getrecursionlimit).

## Practice: predict, explain, modify, debug

1. **Predict:** Trace factorial(3) through both descending calls and returned results.
2. **Explain:** Explain why a negative argument must be rejected before the recursion.
3. **Modify:** Write a loop-based version and compare its state requirements.
4. **Debug:** Find a recursive call that fails to make the input smaller.

<details>
<summary>Hints</summary>

Prove that every valid recursive step approaches the base case.

</details>

## Independent task: recursion & call stacks

In `Practice/02_Recursion_And_Call_Stacks.py`, complete this task:

Define factorial(number) for plain nonnegative integers, raising ValueError otherwise. Use a base case and recursion. Print factorial(5), factorial(0), and Rejected after catching the error for -1. The task uses small inputs and does not require arbitrary-depth recursion.

Expected output:

```text
120
1
Rejected
```
