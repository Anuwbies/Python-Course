# Lesson 5: Iterators, Generators & Memory-Efficient Streaming

When working with gigabyte-sized log files, databases with millions of rows, or infinite data streams, loading everything into a list crashes your system with an `OutOfMemoryError`. In this lesson, you will master **Iterators** and **Generators (`yield`)** for lazy, memory-efficient data processing.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the Iterator Protocol (`__iter__` and `__next__`).
2. Write Generator Functions using the `yield` keyword.
3. Build memory-efficient data pipelines using Generator Expressions.
4. Process massive datasets lazily without memory spikes.

---

## 1. How Iteration Works: The Iterator Protocol

Any object you can loop over in Python implements two magic methods:
1. `__iter__()`: Returns the iterator object itself.
2. `__next__()`: Returns the next element or raises `StopIteration` when finished.

```python
numbers = [10, 20, 30]
iterator = iter(numbers)

print(next(iterator)) # 10
print(next(iterator)) # 20
print(next(iterator)) # 30
# print(next(iterator)) # ❌ Raises StopIteration
```

---

## 2. Generator Functions & The `yield` Keyword

A **Generator** is a special function that produces a sequence of values lazily over time. When Python hits `yield`, it pauses execution, returns the value, and saves its entire local state. When requested again via `next()`, it resumes right where it left off!

```python
def count_up_to(max_val: int):
    count = 1
    while count <= max_val:
        yield count # Pauses and yields value
        count += 1

counter = count_up_to(3)
print(type(counter)) # <class 'generator'>
print(next(counter)) # 1
print(next(counter)) # 2
print(next(counter)) # 3
```

---

## 3. Real-World Comparison: Memory Benchmark

Comparing generating 10 million numbers using a List vs a Generator:

```python
import sys

# 1. List: Allocates all 10,000,000 integers in RAM upfront
list_data = [x for x in range(10_000_000)]
print(f"List RAM Usage: {sys.getsizeof(list_data) / (1024 * 1024):.2f} MB")
# Output: ~80 MB of RAM!

# 2. Generator Expression: Evaluates 1 item at a time on-demand
gen_data = (x for x in range(10_000_000))
print(f"Generator RAM Usage: {sys.getsizeof(gen_data)} bytes")
# Output: ~104 bytes regardless of how many billions of items!
```

---

## 4. Building Lazy Streaming Pipelines

You can chain generators together like Unix pipes to process massive log files without consuming RAM:

```python
def read_raw_logs(file_path: str):
    """Lazily yields lines from a log file."""
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

def filter_errors(log_lines):
    """Filters only lines containing ERROR."""
    for line in log_lines:
        if "ERROR" in line:
            yield line

def extract_ip(error_lines):
    """Extracts the IP address from error logs."""
    for line in error_lines:
        yield line.split()[0]
```

---

## 📝 Quick Exercise

**Prompt**:
Write an infinite generator `fibonacci()`:
1. Yields Fibonacci numbers indefinitely: `0, 1, 1, 2, 3, 5, 8, 13...`
2. Use a `for` loop combined with `enumerate()` to print the first 15 Fibonacci numbers.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Generate first 15 numbers:
for idx, fib_val in enumerate(fibonacci()):
    if idx >= 15:
        break
    print(f"F({idx}) = {fib_val}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **What happens to the local variables of a generator function when it hits `yield`?**
   - A) They are deleted by garbage collection
   - B) They are frozen and preserved until the next call
   - C) They are reset to 0
   - D) They are converted to strings
   *(Answer: B)*

2. **What exception indicates that an iterator has no more elements?**
   - A) `IndexError`
   - B) `StopIteration`
   - C) `EndOfFile`
   - D) `KeyError`
   *(Answer: B)*

3. **What is the syntax for a generator expression?**
   - A) `[x for x in data]`
   - B) `{x for x in data}`
   - C) `(x for x in data)`
   - D) `<x for x in data>`
   *(Answer: C)*
