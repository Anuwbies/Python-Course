# Lesson 3: Iterators, Generators & Lazy Work

**Prerequisites:** Levels 1–6 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Iterators_Generators_And_Lazy_Work.py`.

Produce values on demand and understand who owns the iteration state. Laziness changes when work and errors occur; it does not automatically make an entire pipeline memory-free.

## 1. Distinguish iterable and iterator

An iterable can provide an iterator through iter(). An iterator supplies successive values through next() until it raises StopIteration. A list can create fresh iterators; an existing iterator normally continues from its current position.

```python
values = [10, 20]
iterator = iter(values)
print(next(iterator))  # 10
print(next(iterator))  # 20
```

Another next call would signal exhaustion. A for loop handles that signal as its normal end condition. A custom iterator can implement __iter__ and __next__, but a generator often expresses the same sequential production with less manual state management.

## 2. Yield pauses a function

A function containing yield creates a generator when called. Its body does not run to completion immediately. Each iteration resumes until a yielded value or the end of the function.

```python
def doubled(values):
    for value in values:
        yield value * 2

stream = doubled([1, 2])
print(list(stream))  # [2, 4]
print(list(stream))  # []
```

The second list is empty because the same generator has been consumed. Calling doubled again creates a new generator. Saving the generator object is not the same as saving all produced results.

## 3. Trace deferred failures

Validation inside the generator happens while it is consumed, not necessarily when it is created. A caller's try block must surround the iteration that can fail. Returning a generator from inside an already-closed file context can therefore leave it trying to read a closed resource later.

`yield from source` delegates values from another iterable. A generator expression uses comprehension-like syntax in parentheses. Both can reduce intermediate allocations, but a final list() or a growing grouping dictionary still consumes memory.

## 4. Decide replay and ownership

State whether an API accepts any iterable, requires a reusable sequence, or returns a one-shot stream. A function that loops over its input twice may work with a list and fail logically with a generator because the first pass exhausts it.

Choose deliberate materialization when replay is required and data is bounded. Avoid declaring all generators better than lists: the appropriate representation depends on lifetime, size, replay needs, and the point at which failures should be reported.

References: [Generators](https://docs.python.org/3.13/tutorial/classes.html#generators).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the second list conversion of the same generator.
2. **Explain:** Explain when a validation exception inside a generator will occur.
3. **Modify:** Accept a range as input without converting it to a list first.
4. **Debug:** Fix a caller that consumes a one-shot iterator twice unintentionally.

<details>
<summary>Hints</summary>

The function body runs as the stream is consumed, and each yielded item advances its state.

</details>

## Independent task: iterators, generators & lazy work

In `Practice/03_Iterators_Generators_And_Lazy_Work.py`, complete this task:

Define `nonnegative_values(values)` as a generator yielding each plain nonnegative integer unchanged and raising ValueError when an item is invalid. For valid input `[0, 2, 5]`, print list(stream) twice using the same generator. The second result must reflect exhaustion. Do not build an internal result list.

Expected output:

```text
[0, 2, 5]
[]
```
