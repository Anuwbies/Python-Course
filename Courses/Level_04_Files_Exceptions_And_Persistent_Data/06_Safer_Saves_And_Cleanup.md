# Lesson 6: Safer Saves & Cleanup

**Prerequisites:** Levels 1–3 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Safer_Saves_And_Cleanup.py`.

Preserve known-good data until a replacement is ready, and make resource cleanup run on both success and failure. Separate validation, visibility, and durability instead of promising that one file operation solves every failure.

## 1. See the truncation window

Writing directly over the destination can destroy its previous contents before the replacement is complete. Validating first prevents one class of error, but disk errors or interrupted writes can still occur after opening the destination.

A safer single-writer pattern writes a unique temporary file in the destination's directory, closes it, then replaces the destination. Keeping the temporary file on the same filesystem is important for replacement semantics. A predictable shared filename such as expenses.tmp can collide with another writer, so use tempfile to create a unique one.

## 2. Use finally for unconditional cleanup

An else clause runs when the try block finishes normally. A finally clause runs when control leaves the try statement, including during exceptions or returns. Use it for cleanup, not to override a returned result or suppress a failure accidentally.

```python
handle_name = None
try:
    handle_name = "temporary resource"
    print("Working")
finally:
    print("Cleanup")
```

A return inside finally can replace an earlier result or hide an exception. File with statements already close handles, so do not add a manual close path unless a resource truly requires it.

## 3. Close before replacement

NamedTemporaryFile with delete=False provides a named file that can be closed and then renamed, including on Windows. Record its path before leaving the with block, replace only after the handle is closed, and unlink a leftover candidate in finally with missing_ok=True.

The original remains untouched if preparation fails before replacement. Concurrent writers still need an explicit coordination policy; this pattern alone is not a multiwriter database. Replacement visibility does not automatically promise durability across sudden power loss, which can require filesystem-specific flushing and recovery design.

## 4. Keep the original cause visible

When translating a low-level error into an application-level error, `raise NewError(...) from error` retains an explicit cause. Do this only when it creates a useful boundary; wrapping every exception in the same generic message makes diagnosis harder.

For the exercise, allow unexpected I/O failures to propagate and preserve the destination when validation fails. The demonstration should inspect the actual saved data afterward instead of printing a preservation message without reading it.

## Perform the replacement, not just its outline

The candidate handle's `.name` gives the generated filename. `.parent` chooses the destination's directory. `candidate.replace(destination)` replaces the directory entry; `candidate.unlink(missing_ok=True)` removes a leftover candidate and tolerates its absence after a successful move.

```python
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

with TemporaryDirectory() as folder:
    destination = Path(folder) / "message.txt"
    candidate = None
    try:
        with NamedTemporaryFile("w", encoding="utf-8", dir=destination.parent,
                                delete=False) as handle:
            candidate = Path(handle.name)
            handle.write("prepared replacement")
        candidate.replace(destination)
    finally:
        if candidate is not None:
            candidate.unlink(missing_ok=True)
    print(destination.read_text(encoding="utf-8"))
```

The indentation matters: replace runs after the inner with has closed the handle. Validate and serialize an application's entire candidate before entering this preparation block. A nonexistent parent directory is outside this example's contract.

References: [Temporary files](https://docs.python.org/3.13/library/tempfile.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Identify when direct write mode can first erase old contents.
2. **Explain:** Explain what finally guarantees and what replacement does not guarantee.
3. **Modify:** Make a failed validation leave the prior destination unchanged.
4. **Debug:** Find a return in finally that hides an exception from the caller.

<details>
<summary>Hints</summary>

Create the candidate in the same directory and leave the final destination alone until preparation succeeds.

</details>

## Independent task: safer saves & cleanup

In `Practice/06_Safer_Saves_And_Cleanup.py`, complete this task:

Define `save_amounts(path, amounts)` for a list of plain nonnegative integers. Validate and serialize before touching the destination. Write the JSON to a unique NamedTemporaryFile in the destination directory, close it, replace the destination, and remove a leftover temporary file in finally. In an isolated directory save `[10]`, attempt to save `[-1]` and catch ValueError, then read and print the actual destination contents as parsed JSON.

Expected output:

```text
Invalid save rejected
[10]
```
