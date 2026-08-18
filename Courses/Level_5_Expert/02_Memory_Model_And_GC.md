# Lesson 2: Memory Model, PyObject Internals & Cyclic Garbage Collection

In this lesson, we explore CPython's low-level memory allocation, object headers, reference counting, and the 3-generation cyclic garbage collector.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the anatomy of a `PyObject` in C (`ob_refcnt`, `ob_type`).
2. Track reference counts using `sys.getrefcount()`.
3. Understand reference cycles and how Python's **Generational Cyclic GC** (`gc` module) resolves them.
4. Slash object memory overhead by $70\%$ using `__slots__`.

---

## 1. Reference Counting & The `PyObject` Struct

In CPython, every object is represented by a C struct starting with `PyObject`:

```c
// Under the hood in CPython (Include/object.h)
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;       // Number of references pointing to this object
    struct _typeobject *ob_type; // Pointer to the object's type
} PyObject;
```

```python
import sys

a = []
print(sys.getrefcount(a) - 1) # 1 reference (a)

b = a
print(sys.getrefcount(a) - 1) # 2 references (a, b)

del b
print(sys.getrefcount(a) - 1) # 1 reference (when reaches 0, C free() is called immediately!)
```

---

## 2. Memory Optimization with `__slots__`

Standard Python objects allocate a dynamic dictionary `__dict__` (~150 bytes per object). `__slots__` allocates a flat C array of pointers instead:

```python
import sys

class StandardPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ('x', 'y') # No __dict__ allocated!
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = StandardPoint(1.0, 2.0)
p2 = SlottedPoint(1.0, 2.0)

print(f"Standard instance size + dict: {sys.getsizeof(p1) + sys.getsizeof(p1.__dict__)} bytes") # ~152 bytes
print(f"Slotted instance size: {sys.getsizeof(p2)} bytes") # ~48 bytes (68% RAM reduction!)
```

---

## 📝 Quick Exercise

**Prompt**:
Create a cyclic reference between two objects `a.other = b` and `b.other = a`. Delete `del a, b` and use the `gc.collect()` module to inspect how many unreachable cyclic objects are collected.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.other = None

# Disable automatic collection to observe cycle explicitly
gc.disable()

a = Node("A")
b = Node("B")
a.other = b
b.other = a

# Delete local variable references (objects still reference each other in a cycle!)
del a, b

unreachable_count = gc.collect()
print(f"Cyclic Garbage Collector freed {unreachable_count} unreachable objects in reference cycle!")

gc.enable()
```
</details>
