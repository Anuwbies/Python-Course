# Lesson 6: Native Interop & Extension Boundaries

**Prerequisites:** Levels 1–9 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Native_Interop_And_Extension_Boundaries.py`.

Cross a native-library interface only with an explicit ABI and ownership contract. A Python type annotation is not a declaration of the C calling convention or machine-width representation.

## 1. Distinguish binding and extension development

ctypes binds functions exported by an existing shared library. A CPython extension module implements Python-facing objects or functions using the C API and requires a suitable build/toolchain and compatibility policy. Using ctypes does not mean you created or compiled a new extension module.

Native code can accelerate appropriate work or integrate an existing library, but crossing the boundary has overhead. A one-element call repeated millions of times may perform worse than batching data into one native operation. Measure the boundary you actually use.

## 2. Declare the ABI explicitly

A binding specifies the calling convention, argument types, and return type. For the C library's abs, use a cdecl CDLL binding with c_int argument and result. A wrong declaration can corrupt the process rather than raise a convenient Python exception.

Use ctypes.util.find_library for a supported system C library on Unix-like platforms; Windows provides the msvcrt library interface for this example. Fail clearly when the library is unavailable instead of guessing arbitrary filenames or loading untrusted paths.

## 3. Validate machine-width limits

Python integers are not restricted to the C int width. Determine the width with ctypes.sizeof(c_int), derive its signed maximum, and reject values that would overflow the accepted native domain. The most negative C int has no positive c_int counterpart, so exclude it from this abs wrapper's domain.

The task therefore accepts integers from negative maximum through positive maximum and rejects Booleans through an exact-type check. This is an intentional narrower interface, not a claim that arbitrary Python integers can be safely converted and passed through.

## 4. Respect memory and error ownership

Native pointer results need a clear lifetime and deallocation rule. A C library may require its own free function; using a different allocator can be invalid. A borrowed pointer does not necessarily keep its owner alive. This exercise uses only a scalar value result to keep those ownership issues out of the executed task.

Native error reporting can use return codes, errno, platform error state, or callbacks. Interpret the library's documented policy rather than assuming every failure becomes a Python exception automatically.

## 5. Understand threading and extension compatibility

Some native calls can execute without the conventional GIL while Python object access still requires appropriate rules. Free-threaded builds add explicit compatibility requirements for extensions and do not make arbitrary C libraries thread-safe.

When building a new extension, document the interpreter/ABI, platform, build prerequisites, buffer ownership, and concurrency policy. Do not release locks around code that still relies on unsafe borrowed Python state. These responsibilities are part of the optimization tradeoff, not incidental installation details.

## Bind the function with executable ABI declarations

After `library = ctypes.CDLL(name)`, `absolute = library.abs` obtains the exported function. Assign `absolute.argtypes = [ctypes.c_int]` and `absolute.restype = ctypes.c_int` before calling it. `ctypes.sizeof(ctypes.c_int) * 8` converts its byte width to bits; `2 ** (bits - 1) - 1` is the maximum signed positive value. `os.name == "nt"` identifies the Windows branch for this library-selection example. All validation belongs before the native invocation, since an incorrect machine-level call is not a safe way to test a Python error handler.

References: [Ctypes](https://docs.python.org/3.13/library/ctypes.html), [C extension guide](https://docs.python.org/3.13/extending/index.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict why a huge Python integer must be rejected before the C call.
2. **Explain:** Explain the difference between binding a library and building an extension module.
3. **Modify:** Identify a pointer ownership contract before writing a wrapper.
4. **Debug:** Find a native function missing an explicit return type.

<details>
<summary>Hints</summary>

Determine the actual C type width and exclude the asymmetric minimum before calling abs.

</details>

## Independent task: native interop & extension boundaries

In `Practice/06_Native_Interop_And_Extension_Boundaries.py`, complete this task:

Load the platform system C library with ctypes.CDLL (msvcrt on Windows, find_library("c") elsewhere). Bind abs with c_int argument/result. Implement native_abs(value), requiring a plain integer within the representable symmetric signed c_int range, rejecting invalid values with ValueError before the native call. Print native_abs(-12), then Rejected for an out-of-range integer. Do not load arbitrary user-provided libraries.

Expected output:

```text
12
Rejected
```
