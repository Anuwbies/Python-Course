# Lesson 4: Closures, Decorators & Metadata

**Prerequisites:** Levels 1–6 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Closures_Decorators_And_Metadata.py`.

Retain a small amount of surrounding state or wrap an existing callable without changing its contract accidentally. Explain the transformation a decorator performs instead of treating the @ symbol as magic.

## 1. Return behavior with retained state

A nested function can refer to a binding in its enclosing function. Returning that nested function retains the environment needed for later calls: a closure. To reassign an existing enclosing binding, use nonlocal; reading it alone does not require the declaration.

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
print(counter())  # 1
print(counter())  # 2
```

Each call to make_counter creates its own enclosing state. The counter is serial mutable state, not automatically thread-safe. Later concurrency lessons add synchronization when several threads can access a shared counter.

## 2. Decorate by replacing a binding

For a function named work, `@decorate` above its definition is broadly equivalent to `work = decorate(work)` after the function is created. The decorator receives a callable and returns the callable that later callers will use.

A wrapper commonly accepts *args and **kwargs, invokes the original with the same arguments, and returns its result. Omitting the return changes a previously numeric function into one returning None. Catching every exception and returning a default would also change its failure contract.

## 3. Preserve useful metadata

`functools.wraps(original)` copies appropriate metadata and provides a __wrapped__ reference for introspection tools. Without it, names and docstrings may identify only the generic wrapper. Function objects can also hold explicit attributes such as wrapper.calls for a documented counter.

A wrapper's state policy matters. Decide whether a counter means attempted calls or successful calls and update it at the corresponding point. A timing decorator must distinguish elapsed time from correctness and avoid promising a stable duration in a sample transcript.

## 4. Avoid hidden architecture

A decorator can apply logging, timing, or access rules at a callable boundary, but a reader should still be able to locate the effect. Stacking several decorators applies them in a particular nesting order; changing order can change which work is counted or timed.

Use an ordinary helper when it makes control flow clearer. Wrapping does not remove the need for tested contracts, and a decorated function still needs meaningful inputs and results independent of its extra instrumentation.

## Follow a wrapper from creation to invocation

`count += 1` is augmented assignment, updating a numeric binding with its old value plus one; it follows the same scope rules as ordinary assignment. A function attribute instead belongs to the callable object, so `wrapper.calls += 1` updates that object's documented counter.

```python
from functools import wraps

def announce(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print("Starting", function.__name__)
        return function(*args, **kwargs)
    return wrapper

@announce
def greet(name):
    return "Hello, " + name

print(greet("Mika"))
```

announce runs at definition time and returns wrapper. Later greet calls invoke wrapper, which forwards the arguments and result. For a successful-call counter, save the delegated result, increment only after that call returns, then return the saved result. An exception prevents that increment naturally. For attempted calls increment before delegation instead; these are different contracts.

References: [Functools wraps](https://docs.python.org/3.13/library/functools.html#functools.wraps).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether two make_counter results share counts.
2. **Explain:** Explain the assignment performed by a simple decorator.
3. **Modify:** Choose whether to count attempted or successful calls and document that choice.
4. **Debug:** Restore a return statement lost while introducing a wrapper.

<details>
<summary>Hints</summary>

Update the attempted-call counter before delegation and return the delegated result.

</details>

## Independent task: closures, decorators & metadata

In `Practice/04_Closures_Decorators_And_Metadata.py`, complete this task:

Implement `count_calls(function)` using functools.wraps. Return a wrapper accepting and forwarding all arguments, preserving the original result and exceptions, and incrementing a public calls attribute on every attempted call. Decorate add(left, right), print add(1,2), add(3,4), then add.calls.

Expected output:

```text
3
7
2
```
