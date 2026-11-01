# Lesson 1: Profiling & Experimental Design

**Prerequisites:** Levels 1–9. **Practice file:** `Practice/01_Profiling_And_Experimental_Design.py`.

Investigate where an application spends time and design a comparison that can support a limited conclusion. Expert work begins with a reproducible question, not with selecting an advanced mechanism to insert.

## 1. Separate profiling and benchmarking

A profiler attributes work to functions or call paths. A benchmark measures a defined operation under selected conditions. Profiling overhead can change relative costs, so use the profiler to locate candidates and an appropriately isolated benchmark to compare them.

cProfile records call statistics for an executed workload. pstats can sort and present them by cumulative or internal time. Cumulative time includes child calls; internal time focuses on work attributed inside the function. Confusing those columns can lead to optimizing a wrapper whose own work is negligible.

## 2. Preserve the result while observing it

```python
import cProfile
import pstats

profile = cProfile.Profile()
result = profile.runcall(sum, range(1000))
stats = pstats.Stats(profile)
print(result)
print(stats.total_calls)
```

The profiler invokes the real callable and returns its result. A report's call count depends on the workload and interpreter; it is not a fixed property to copy from another machine. Use source locations and meaningful call paths rather than relying on an incidental row order.

## 3. Control the experiment

State the interpreter/build, input size, data distribution, warmup, repetitions, and timed boundary. Excluding file loading can be appropriate for a parse-only question, but must be disclosed. Include setup when evaluating the complete user-visible operation.

Use repeated observations and a robust summary. A single best duration encourages accidental cherry-picking. Record noise and unexpected outcomes rather than adjusting the workload until the preferred version wins.

## 4. Establish semantic equivalence

An optimized variant must preserve returned values, rejected inputs, side effects, and resource ownership. Comparing only a printed checksum can miss skipped validation or changed error behavior. Keep independent known-answer and boundary cases alongside the performance investigation.

A faster microbenchmark may not improve end-to-end latency if the optimized stage is a small fraction of the total workload. Consider how much time that stage actually contributes before spending effort on native extensions or interpreter tricks.

## 5. Make the conclusion falsifiable

Report what improved under which conditions and what did not. A claim such as avoids allocating an input slice per record can be inspected in the implementation, while a claim of lower peak memory needs a measurement with a clearly defined scope.

Do not equate an operation-count reduction with a universal speedup. Cache locality, allocation, C-library work, and interpreter specialization can change the practical tradeoff. The independent task reports actual statistics without a prescribed duration or call count.

References: [Python profilers](https://docs.python.org/3.13/library/profile.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the calculation result before profiling it.
2. **Explain:** Explain cumulative versus internal time with a wrapper and helper.
3. **Modify:** State whether setup belongs inside your timed boundary.
4. **Debug:** Find a benchmark whose preferred variant silently omits validation.

<details>
<summary>Hints</summary>

The result and profile describe the same actual invocation.

</details>

## Independent task: profiling & experimental design

In `Practice/01_Profiling_And_Experimental_Design.py`, complete this task:

Implement a profiled calculation using cProfile.Profile.runcall on sum(range(1000)). Use pstats.Stats to obtain the actual total call count. Print Result: 499500 and Profiled calls: <observed count>. Do not hardcode the call count or timing. Keep any written conclusion limited to the observed workload.
