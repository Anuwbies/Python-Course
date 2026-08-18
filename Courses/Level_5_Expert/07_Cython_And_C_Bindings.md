# Lesson 7: Native C-Extensions, ctypes, cffi & Cython

When algorithms require raw hardware speeds (cryptography, physics simulations, custom hash tables), Python can bind directly to compiled C/C++ libraries or compile directly to native machine code via Cython.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Call shared C libraries (`.dll` / `.so`) using `ctypes`.
2. Use modern `cffi` (C Foreign Function Interface) for type-safe bindings.
3. Write and compile **Cython (`.pyx`)** modules with static C type declarations (`cdef`).
4. Achieve $50\times - 100\times$ speedups on mathematical loops.

---

## 1. Calling C Libraries with `ctypes`

```python
import ctypes
import os

# Load standard C runtime library (Windows: msvcrt.dll, Linux: libc.so.6)
if os.name == 'nt':
    libc = ctypes.cdll.msvcrt
else:
    libc = ctypes.CDLL("libc.so.6")

# Call C printf directly
libc.puts(b"Hello from native C runtime library!")
```

---

## 2. Accelerating Python with Cython (`math_speed.pyx`)

```cython
# cython: boundscheck=False, wraparound=False
def fast_sum_primes(int limit):
    cdef int total = 0
    cdef int i, j
    cdef bint is_prime

    for i in range(2, limit):
        is_prime = True
        for j in range(2, int(i ** 0.5) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            total += i
    return total
```
*(Compiled via `setup.py` with `cythonize`, this runs at pure C hardware speeds!)*

---

## 📝 Quick Exercise

**Prompt**:
Create a simple C function in a `.c` file that calculates the Euclidean distance between two 2D points, compile it into a shared library (`.dll`), and call it from Python using `ctypes`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

### 1. `distance.c`:
```c
#include <math.h>

__declspec(dllexport) double euclidean_distance(double x1, double y1, double x2, double y2) {
    double dx = x2 - x1;
    double dy = y2 - y1;
    return sqrt(dx * dx + dy * dy);
}
```

### 2. Python Caller (`main.py`):
```python
import ctypes

# Load compiled DLL
lib = ctypes.CDLL("./distance.dll")

# Define C signature
lib.euclidean_distance.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
lib.euclidean_distance.restype = ctypes.c_double

dist = lib.euclidean_distance(0.0, 0.0, 3.0, 4.0)
print(f"Calculated distance via C extension: {dist}") # 5.0
```
</details>
