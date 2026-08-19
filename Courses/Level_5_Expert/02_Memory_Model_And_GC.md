# Lesson 2: CPython Memory Model, Reference Counting & Cyclic GC

Every variable, function, class, and integer in Python is represented in C memory as a `PyObject` C-struct. Managing memory efficiently across millions of objects requires mastering CPython's dual memory management architecture: **Reference Counting** for immediate deallocation and the **Generational Cyclic Garbage Collector (`gc`)** for resolving reference cycles. In this lesson, you will master `PyObject` memory layout, generational collections, and memory leak elimination using `weakref`.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the C-level memory layout of `PyObject` (`ob_refcnt`, `ob_type`).
2. Track and inspect reference counts using `sys.getrefcount()`.
3. Understand how **Cyclic References** cause memory leaks in pure reference-counting allocators.
4. Master the **Generational Garbage Collector** (Generations 0, 1, 2) and control it via the `gc` module.
5. Prevent cache memory leaks using **Weak References** (`weakref.ref`, `weakref.WeakValueDictionary`).
6. Understand CPython's **`pymalloc`** allocator hierarchy (Arenas $\to$ Pools $\to$ Blocks).

---

## 1. The `PyObject` Header & Reference Counting

Every Python object allocated in heap memory starts with the `PyObject_HEAD` macro in C:

```c
// CPython C-struct representation (Include/object.h)
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;          // 64-bit reference counter
    struct _typeobject *ob_type;   // Pointer to Python type object
} PyObject;
```

```python
import sys

x = ["item1", "item2"]
# sys.getrefcount adds +1 temporary reference when passed as argument
print(f"Reference Count of x: {sys.getrefcount(x)}") # 2 (x + argument pointer)

y = x
print(f"Reference Count after alias: {sys.getrefcount(x)}") # 3 (x + y + argument pointer)

del y
print(f"Reference Count after deletion: {sys.getrefcount(x)}") # 2
```

---

## 2. Reference Cycles & Generational Garbage Collection

When two objects hold references to each other (or an object references itself), their reference counts never drop to zero even after all external variable names are deleted:

```
[ Node A (refcount=1) ] ──points to──> [ Node B (refcount=1) ]
         ▲                                       │
         └──────────────points back to───────────┘
```

CPython's cyclic GC scans container objects in 3 generations:
- **Generation 0**: Newly allocated objects (scanned frequently).
- **Generation 1**: Objects surviving 1 GC collection pass.
- **Generation 2**: Long-lived objects (scanned rarely).

```python
import gc

# Inspect GC collection thresholds:
print(gc.get_threshold()) # Default: (700, 10, 10)
# (700 allocations trigger Gen0, 10 Gen0 collections trigger Gen1, 10 Gen1 trigger Gen2)

# Manually trigger full generational collection:
unreachable_collected = gc.collect()
print(f"Collected {unreachable_collected} cyclical orphan objects.")
```

---

## 3. Weak References with `weakref`

A **Weak Reference** references a target object without incrementing its `ob_refcnt`. When the only remaining references to an object are weak references, the object is immediately deallocated:

```python
import weakref

class CacheData:
    def __init__(self, data: str):
        self.data = data

obj = CacheData("Large 100MB Matrix")
weak_handle = weakref.ref(obj)

print("Weak reference resolves:", weak_handle().data) # Resolves successfully

del obj # Strong reference deleted -> Immediately deallocated!
print("Weak reference after deletion:", weak_handle()) # None (Dead reference)
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise High-Performance In-Memory Cache with Weak References & Cyclic Garbage Collection Diagnostic Engine**, demonstrating refcount auditing, cyclic leak detection, and `WeakValueDictionary` eviction:

```python
# =====================================================================
# REAL-WORLD SYSTEM: High-Performance Weak Cache & Memory Diagnostics
# =====================================================================

import sys
import gc
import weakref

class UserSessionPayload:
    def __init__(self, session_id: str, username: str):
        self.session_id = session_id
        self.username = username

    def __repr__(self) -> str:
        return f"UserSession(id='{self.session_id}', user='{self.username}')"


class ResilientSessionCache:
    """Cache utilizing WeakValueDictionary to prevent memory leaks from abandoned objects."""
    def __init__(self):
        # WeakValueDictionary automatically discards entries when strong references die
        self._weak_store = weakref.WeakValueDictionary()

    def store_session(self, session: UserSessionPayload) -> None:
        self._weak_store[session.session_id] = session

    def get_session(self, session_id: str) -> UserSessionPayload | None:
        return self._weak_store.get(session_id)

    def active_cache_size(self) -> int:
        return len(self._weak_store)


# Cyclic Reference Diagnostic Engine
class DiagnosticCycleNode:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.partner = None # Pointer causing cycle


def demonstrate_memory_diagnostics():
    print("=" * 80)
    print(f"{'CPYTHON MEMORY MODEL & CYCLIC GC DIAGNOSTIC SUITE':^80}")
    print("=" * 80)

    # 1. Weak Reference Cache Validation
    print("--- 1. WEAK REFERENCE CACHE BEHAVIOR ---")
    cache = ResilientSessionCache()

    # Create active sessions
    session_1 = UserSessionPayload("SESS-01", "Elena Rostova")
    session_2 = UserSessionPayload("SESS-02", "Marcus Vance")

    cache.store_session(session_1)
    cache.store_session(session_2)
    print(f"Active Cache Size: {cache.active_cache_size()} sessions")
    print(f"Direct Lookup SESS-01: {cache.get_session('SESS-01')}")

    # Delete local strong reference to session_1
    print("\nDropping local strong reference 'del session_1'...")
    del session_1

    print(f"Active Cache Size after strong ref drop: {cache.active_cache_size()} sessions (Auto-evicted! ⚡)")
    print(f"Lookup SESS-01 after eviction: {cache.get_session('SESS-01')}")

    # 2. Reference Counting & Cyclic GC Verification
    print("\n--- 2. REFERENCE CYCLE DETECTION & GC RECLAMATION ---")
    # Disable GC temporarily to observe cycle leak
    gc.disable()

    node_a = DiagnosticCycleNode("Node-A")
    node_b = DiagnosticCycleNode("Node-B")

    # Create reference cycle (A -> B -> A)
    node_a.partner = node_b
    node_b.partner = node_a

    print(f"Node A RefCount before drop: {sys.getrefcount(node_a) - 1}") # Exclude getrefcount arg

    # Drop external variable handles
    del node_a
    del node_b
    print("Dropped external handles 'node_a' and 'node_b' (Cycle remains trapped in memory).")

    # Re-enable and force cyclic GC collection
    gc.enable()
    collected_objects = gc.collect()
    print(f"✅ Cyclic GC Collection Run: Reclaimed {collected_objects} unreachable cyclic objects!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_memory_diagnostics()
```

### 🔍 Code Explanation:
- **`WeakValueDictionary`**: Stores weak references to values; when caller variables drop their strong references, the dictionary silently purges the key without memory leak.
- **Reference Cycle Creation**: `node_a.partner = node_b` and `node_b.partner = node_a` prevents `ob_refcnt` from reaching zero upon `del`.
- **`gc.collect()`**: Scans generational heap memory, detects self-referencing container loops, breaks the cycles, and releases the trapped C memory.

---

## 📝 Quick Exercise: Cyclic Reference Memory Leak Detector & Collector

### 🏢 Real-Life Scenario
You are developing an automated memory profiling utility for an enterprise microservice backend. You must create a diagnostic function that detects when a data structure creates circular references, counts unreachable objects, and forces garbage collection.

### 📋 Requirements
1. **Define Class `CircularTaskNode`**:
   - `__init__(self, task_id: str)`: Attributes `task_id`, `next_task = None`.
2. **Define `detect_and_clear_cycle_leak(node_count: int) -> dict`**:
   - Disables GC (`gc.disable()`).
   - Allocates a circular ring of `node_count` nodes where each node's `next_task` points to the next, and the last points to the first.
   - Drops the root pointer (`del root`).
   - Re-enables GC (`gc.enable()`).
   - Executes `gc.collect()` and records how many objects were cleaned.
   - Returns summary dictionary.
3. Test with a 10-node cycle and display the memory recovery metrics.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 5 CPython memory model and `gc` with Level 2 classes and Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        CPYTHON CYCLIC LEAK DETECTOR TEST         
==================================================
Created circular chain of 10 nodes.
Dropped root handle (0 strong external references).
--------------------------------------------------
GC Collection Execution:
  ✓ Cyclic Objects Collected: 10
  ✓ Memory State: Clean & Reclaimed ✅
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import gc

# 1. Circular Node (Level 5)
class CircularTaskNode:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.next_task = None


# 2. Cycle Detector Function (Level 5)
def detect_and_clear_cycle_leak(node_count: int) -> dict:
    gc.disable()

    # Create circular ring
    nodes = [CircularTaskNode(f"TASK-{i}") for i in range(node_count)]
    for i in range(node_count):
        nodes[i].next_task = nodes[(i + 1) % node_count]

    root = nodes[0]
    del nodes # Drop list handle

    # Drop remaining root reference (Ring is now isolated in memory)
    del root

    gc.enable()
    collected = gc.collect()

    return {
        "node_count": node_count,
        "collected_objects": collected
    }


# 3. Execution Simulation
print("==================================================")
print("        CPYTHON CYCLIC LEAK DETECTOR TEST         ")
print("==================================================")
print("Created circular chain of 10 nodes.")
print("Dropped root handle (0 strong external references).")
print("--------------------------------------------------")

results = detect_and_clear_cycle_leak(10)
print("GC Collection Execution:")
print(f"  ✓ Cyclic Objects Collected: {results['collected_objects']}")
print("  ✓ Memory State: Clean & Reclaimed ✅")
print("==================================================")
```

**Explanation of the Solution:**
- Manually creating an isolated cycle and disabling GC demonstrates how circular references prevent standard reference counting deallocation.
- Re-enabling and executing `gc.collect()` breaks the circular chain and reclaims the leaked objects.
</details>
