# Lesson 2: Object Lifetimes, GC & Memory Measurement

**Prerequisites:** Levels 1–9 and Lesson 1 of this level. **Practice file:** `Practice/02_Object_Lifetimes_GC_And_Memory_Measurement.py`.

Distinguish object reachability, implementation memory management, and what a memory tool actually observes. A shallow size, traced allocation peak, and process resident memory are different measurements.

## 1. Follow references rather than names alone

An assignment binds a name to an object. Deleting a name removes that binding, not necessarily the object. Other containers, closures, frames, or caches may still reference it. Inspect the reference graph relevant to the symptom instead of assuming one del statement frees everything.

CPython ordinarily combines reference counting with a cyclic garbage collector. That is an implementation behavior, not a language promise about the exact moment every object is destroyed. Avoid relying on immediate destruction to close critical resources; context managers express their lifetime explicitly.

## 2. Recognize cycles and weak references

A cycle can remain after external strong references disappear. The cyclic collector can reclaim appropriate unreachable cycles. A weakref observes an object without keeping it alive; not every built-in type supports weak references directly.

```python
import gc
import weakref

class Node:
    pass

node = Node()
node.link = node
observed = weakref.ref(node)
del node
gc.collect()
print(observed() is None)
```

This experiment checks the actual result after collection. Garbage-collection details vary across Python versions and builds; inspect current runtime configuration rather than copying a generation diagram from another release. Disabling collection can hide a performance cost while increasing retained cycles.

## 3. Interpret sizes at the right boundary

sys.getsizeof reports an object's shallow size according to its implementation. A list's number does not include the full transitive size of every referenced object. Adding shallow sizes can also double-count shared objects unless the traversal tracks identities.

Tracemalloc observes traced Python allocation activity after tracing begins. Its peak is not the same as total process RSS, and native allocations may not all appear under the same accounting. Record whether the input dataset was allocated before the measurement window.

## 4. Own the measurement lifetime

Start tracing before the operation of interest, collect current/peak values, and stop it in finally if your tool owns that tracing session. Do not silently reset another caller's active tracing state. A reusable measurement helper should state whether it requires tracing to be inactive on entry.

Allocation measurements themselves have overhead. Run timing and memory experiments separately when the instrumentation would distort the timing question. A peak on one bounded workload does not establish a universal memory bound.

## 5. Diagnose retention, not only churn

High temporary allocation and long-lived retention have different causes. Compare snapshots or retained references when memory grows across repeated requests; a one-call peak alone may miss a cache that never releases keys.

The exercise combines an inspectable cycle with an actual traced allocation. It does not tune collector thresholds or promise that forcing collection improves application performance.

## Own an actual tracing session

`tracemalloc.is_tracing()` reports whether tracing is already active. `tracemalloc.start()` begins it; `get_traced_memory()` returns `(current_bytes, peak_bytes)` measured since tracing started or its peak was reset. Stop only the session your helper owns:

```python
import tracemalloc

if tracemalloc.is_tracing():
    raise RuntimeError("Tracing is already active")
tracemalloc.start()
try:
    values = list(range(100))
    current, peak = tracemalloc.get_traced_memory()
finally:
    tracemalloc.stop()
print("Observed peak bytes:", peak)
```

Keep the allocation alive until the observation when measuring its retained contribution. For a parse-only capstone, build the input before start and invoke just one parser inside the window. An already-active-session guard prevents this helper from stopping a caller's measurement accidentally.

## Use a deliberately empty class body

`class Node: pass` defines an ordinary class with no custom methods yet. pass is a no-operation statement that supplies the required nonempty block; it is not a task placeholder here. Instances of this ordinary unslotted class support attributes and weak references. Keep the weakref result separate from strong references when checking whether an unreachable cycle was collected.

References: [Tracemalloc](https://docs.python.org/3.13/library/tracemalloc.html), [Garbage collector](https://docs.python.org/3.13/library/gc.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether a weak reference keeps a cyclic object alive.
2. **Explain:** Explain why a list's shallow size is not its full transitive footprint.
3. **Modify:** Measure an operation with input allocated outside the traced window.
4. **Debug:** Find a memory comparison that mixes process RSS with tracemalloc peak values.

<details>
<summary>Hints</summary>

Keep the weak reference separate from strong ownership and report the tool's actual measurement scope.

</details>

## Independent task: object lifetimes, gc & memory measurement

In `Practice/02_Object_Lifetimes_GC_And_Memory_Measurement.py`, complete this task:

Create a weak-referenceable Node whose link refers to itself, remove the external strong reference, invoke gc.collect, and print whether the weak reference is cleared. Separately start tracemalloc, allocate list(range(10000)), obtain the observed peak, stop tracing in finally, and print the actual list length and peak bytes. Do not hardcode a memory size.
