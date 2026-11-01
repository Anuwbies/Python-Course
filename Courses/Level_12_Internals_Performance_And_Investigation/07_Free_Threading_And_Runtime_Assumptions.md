# Lesson 7: Free Threading & Runtime Assumptions

**Prerequisites:** Levels 1–9 and Lessons 1–6 of this level. **Practice file:** `Practice/07_Free_Threading_And_Runtime_Assumptions.py`.

Investigate concurrency under the interpreter build actually running. A free-threading-capable build, the current GIL state, and a thread-safe application are three different properties.

## 1. Identify both build and active mode

Python 3.13 introduced an experimental optional free-threaded CPython build. This course pins its examples and documentation to the 3.13 API rather than assuming every later release has identical status or internals.

`sysconfig.get_config_var("Py_GIL_DISABLED")` can identify the build capability. `sys._is_gil_enabled()` reports the active GIL state when that version-specific function exists. A capable build can still run with a GIL, and an extension import may affect the runtime mode according to its compatibility support.

## 2. Keep portable fallback information honest

```python
import sys

probe = getattr(sys, "_is_gil_enabled", None)
gil_enabled = probe() if probe is not None else None
print(sys.implementation.name)
print(gil_enabled)
```

None means the capability was not available through this probe; it must not be silently relabeled as disabled or enabled. Record interpreter version and the libraries already imported at the observation point.

## 3. Preserve application invariants

Internal locks protecting individual containers do not make a sequence of application operations atomic. A check-then-update across fields still needs an explicit lock or another safe design. Code that happened to behave under conventional scheduling can expose races in another build.

A lock-protected counter from Level 9 remains conceptually valid because its invariant does not rely on the GIL. Test failed operations and shared state under the relevant build rather than inferring thread safety from one successful run.

## 4. Measure scaling without promising it

Parallel execution can still be limited by contention, allocation, memory bandwidth, input/output, work imbalance, or extension behavior. Measure sequential and concurrent variants with equivalent results and include startup/synchronization costs when they belong to the operation.

Do not require linear speedup as a course success condition. A useful expert report can explain why additional threads do not help this workload and suggest a different decomposition. Reproducing the environment is essential when sharing that conclusion.

## 5. Treat compatibility as part of the project

A native extension's compatibility declaration, its actual locking, and the application's use of it all matter. Disabling a lock globally does not remove object-lifetime obligations. Review the versioned primary documentation before relying on internal changes.

The task records actual runtime information and computes a real synchronized result. It can run on the conventional build while clearly stating that this does not constitute testing on a free-threaded interpreter.

## Probe optional attributes without assuming they exist

`getattr(object, name, default)` returns an attribute or the supplied fallback if it is absent. Thus `getattr(sys, "_is_gil_enabled", None)` yields either the callable probe or None; call it only after checking which result you got. Import sysconfig and call `sysconfig.get_config_var("Py_GIL_DISABLED")` for the build flag. The latter does not report the current live lock state.

Use an instance-owned Counter and its Lock, as in Level 9, for this task. Passing that object to each thread avoids introducing module-global mutation merely to observe the runtime.

References: [Free-threaded Python 3.13](https://docs.python.org/3.13/howto/free-threading-python.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict why build capability and active GIL state can differ.
2. **Explain:** Explain why a multi-step dictionary workflow can still require a lock.
3. **Modify:** Run the same bounded counter under two documented interpreter builds when available.
4. **Debug:** Remove a claim of linear scaling unsupported by measured workload results.

<details>
<summary>Hints</summary>

Observe the runtime and protect the actual read-modify-write operation.

</details>

## Independent task: free threading & runtime assumptions

In `Practice/07_Free_Threading_And_Runtime_Assumptions.py`, complete this task:

Report sys.implementation.name, the actual active GIL state when its probe exists (otherwise None), and the build's Py_GIL_DISABLED value. Run four joined threads performing 1000 increments each under a shared Lock and print the actual count. The expected count is 4000; interpreter/build fields vary and must not be hardcoded. Record that a conventional-build run does not establish free-threaded compatibility.
