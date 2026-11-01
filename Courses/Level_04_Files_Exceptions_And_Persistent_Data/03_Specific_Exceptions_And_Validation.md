# Lesson 3: Specific Exceptions & Validation

**Prerequisites:** Levels 1–3 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Specific_Exceptions_And_Validation.py`.

Handle a failure you can respond to, and let unrelated failures remain visible. Exception handling is part of a function contract, not a blanket instruction to make every error disappear.

## 1. Follow the failing operation

A try block runs normally until an exception is raised. Python then looks for a matching except clause. Statements later in the interrupted try block are skipped; execution continues after the handler when it finishes normally.

```python
try:
    amount = int("tea")
except ValueError:
    print("Amount is not integer text")
```

Keep the try block narrow enough that its handler describes the operation that can fail. A huge try block covering reading, parsing, aggregation, and printing makes it difficult to know what the error actually means.

## 2. Reject invalid values explicitly

Conversion can succeed for a negative integer even when the problem requires a nonnegative amount. `raise ValueError(message)` reports that accepted syntax did not satisfy the value contract.

```python
def parse_amount(text):
    amount = int(text.strip())
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount
```

The function returns a valid integer or raises. It does not return zero on failure, because zero is a valid amount. The caller can catch ValueError and ask again or report a rejected row. Those choices belong at the appropriate application boundary.

## 3. Distinguish error families

FileNotFoundError and PermissionError are specific OSError subclasses. A missing optional first-use file may reasonably produce an empty collection; a file you cannot read is not evidence of an empty collection. ValueError covers inappropriate values; UnicodeDecodeError is a UnicodeError subclass within ValueError, so broad value handlers may also catch decoding problems.

Do not use a bare except to hide everything. It can intercept KeyboardInterrupt and make the program difficult to stop. Catching Exception can be appropriate at a top-level reporting boundary, but it must not pretend that an unknown programming failure was successful input processing.

## 4. Recover without corrupting state

Parse and validate a candidate record before appending it or changing a balance. A rejected record should not partially update a total. For a complete file load, decide whether corruption rejects the entire file or returns a report of skipped records; silently discarding rows can hide important information.

A handled failure should still leave an observable result: a rejection message, a raised error to the caller, or an explicitly structured error report. Avoid returning a success-shaped empty result when the data was actually unavailable.

## Bind an error and separate the success path

`except ValueError as error` gives the caught exception a local name inside its handler. `str(error)` obtains its message. To handle several documented families the same way, use `except (OSError, ValueError) as error:`. The tuple means either family, not both simultaneously.

An `else` after the handlers runs only when the try body finished without an exception. Put success reporting there so an error in the success report itself is not mislabeled as a parsing failure:

```python
try:
    amount = int("25")
except ValueError as error:
    print("Rejected:", str(error))
else:
    print("Accepted:", amount)
```

An unhandled exception propagates to the caller. A bare `raise` inside a handler re-raises the current exception without inventing a new success result. RuntimeError describes a failed operation or unavailable runtime condition when a more specific built-in type does not fit; AssertionError describes a failed development expectation. The next lessons add unconditional cleanup and explicit error causes.

References: [Python errors and exceptions](https://docs.python.org/3.13/tutorial/errors.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict parse_amount for zero, negative text, and a nonnumeric word.
2. **Explain:** Explain why zero is unsuitable as a universal failure result.
3. **Modify:** Add a caller that reports rejected values without adding them to a total.
4. **Debug:** Reduce an overly broad try block so its ValueError handler only describes parsing.

<details>
<summary>Hints</summary>

The else clause runs when the try block finishes without an exception.

</details>

## Independent task: specific exceptions & validation

In `Practice/03_Specific_Exceptions_And_Validation.py`, complete this task:

Define `parse_amount(text)` to return a nonnegative integer. Convert stripped text with int; raise ValueError for negative amounts. For the responses `"0"`, `"-1"`, and `"tea"`, call it inside a loop and print `Accepted: <amount>` or `Rejected` using a specific ValueError handler.

Expected output:

```text
Accepted: 0
Rejected
Rejected
```
