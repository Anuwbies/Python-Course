# Lesson 1: Complexity & Measurement

**Prerequisites:** Levels 1–7. **Practice file:** `Practice/01_Complexity_And_Measurement.py`.

Explain how work grows with input size, then measure an implementation under controlled conditions. Complexity and elapsed time answer related but different questions.

## 1. Name the size variable

For a list search, n can mean the number of elements. A linear scan may inspect every element, so worst-case comparisons grow proportionally to n. A constant-time-looking dictionary operation has its own assumptions and does not mean the whole application performs a fixed amount of work.

```python
def contains(values, target):
    for value in values:
        if value == target:
            return True
    return False
```

Finding the first element and failing to find an element are different paths. State best, average, or worst-case claims explicitly. Big-O describes an asymptotic upper-bound relationship under a model, not a promise that one measured run lasts a particular number of milliseconds.

## 2. Count the work that matters

Two nested loops over n values often perform quadratic work, but nesting alone is not proof: loop bounds and early exits determine the count. A loop that halves a search interval has a different growth pattern from one that reduces it by one.

Separate time and auxiliary space. Building a set may improve repeated membership lookups while using additional memory. Including preprocessing in one variant and excluding it from another makes a comparison answer an unclear question.

## 3. Measure an explicit workload

Use time.perf_counter_ns for elapsed durations. Warm up as appropriate, repeat trials, and report a summary such as the median rather than selecting a favorable single run. Record input size, data distribution, interpreter, and whether setup was timed.

Small examples can be dominated by interpreter overhead, allocation, caching, or measurement noise. Scaling measurements across input sizes helps relate observations to the growth claim, but a short timing table is not a universal mathematical proof.

## 4. Establish correctness first

Before comparing speed, establish that the variants return equivalent results for the relevant cases. An algorithm that skips half the required records may appear fast precisely because it is incorrect.

For the independent task, count actual comparisons rather than claiming a speedup. A counter is a simple inspectable model. Later capstone measurements use real elapsed time without imposing a fixed hardware-dependent threshold.

## Collect real repeated timing observations

`statistics.median(samples)` returns the central observation after ordering the samples (or the mean of the middle two). Measure each complete repeated workload, not a guessed duration:

```python
from statistics import median
from time import perf_counter_ns

samples = []
for trial in range(5):
    start = perf_counter_ns()
    for repetition in range(100):
        answer = sum(range(20))
    samples.append(perf_counter_ns() - start)
print("Median workload ns:", median(samples))
```

Each sample here includes 100 calls plus loop overhead. Divide each duration by 100 if reporting an approximate per-call duration, and label that scope. Time any preprocessing separately when the question concerns repeated queries against a reused index. Do not compare an index query-only measurement with a scan that includes unrelated file loading.

References: [High-resolution timing](https://docs.python.org/3.13/library/time.html#time.perf_counter_ns).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the comparison count for a target at the first position and a missing target.
2. **Explain:** Explain which setup costs belong in a one-query versus many-query comparison.
3. **Modify:** Compare counts at two list sizes without using wall-clock time.
4. **Debug:** Find a benchmark that times input generation for only one variant.

<details>
<summary>Hints</summary>

Count a comparison before deciding whether that value ends the search.

</details>

## Independent task: complexity & measurement

In `Practice/01_Complexity_And_Measurement.py`, complete this task:

Define `linear_search(values, target)` returning `(found, comparisons)`, incrementing comparisons for each visited value compared with target. Do not mutate values. Print the results for target 4 and target 9 in `[0, 1, 2, 3, 4]`.

Expected output:

```text
(True, 5)
(False, 5)
```
