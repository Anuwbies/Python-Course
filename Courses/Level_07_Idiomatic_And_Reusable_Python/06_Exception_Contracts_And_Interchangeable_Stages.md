# Lesson 6: Exception Contracts & Interchangeable Stages

**Prerequisites:** Levels 1–6 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Exception_Contracts_And_Interchangeable_Stages.py`.

Build reusable stages whose failure behavior is as clear as their successful values. Translate an error only at a meaningful boundary and retain the original cause for diagnosis.

## 1. Name an application-level failure

A custom exception can inherit from a relevant built-in family. For example, InvalidAmount as a ValueError subtype remains catchable by code that handles value problems while allowing a more specific boundary to identify amount failures.

```python
class InvalidAmount(ValueError):
    """An amount cannot be interpreted under the application's rules."""
```

The docstring is a complete class body; this exception deliberately adds a meaningful type without extra state. Do not create a new exception type for every line of code. Use one when callers can make a meaningful decision from that distinction.

## 2. Preserve the cause when translating

A conversion ValueError can be translated with `raise InvalidAmount("Invalid amount text") from error`. The new exception's __cause__ identifies the original problem. The traceback can display both the lower-level cause and the application-level interpretation.

Do not translate an unrelated TypeError from a programming bug into an ordinary invalid-row message just because a large except catches everything. Narrow the operation and catch the documented failure you intend to interpret.

## 3. State pipeline policies

One pipeline can reject the entire input on a bad record. Another can yield accepted records and a separate rejection report. Both need an explicit contract. Silently skipping data makes a successful total ambiguous because callers cannot know what was omitted.

For a lazy stage, the failure is raised during consumption. Include source positions or identifiers where they help a caller locate the bad data. Position reporting must match the parser's actual model, especially when one logical record can span several physical lines.

## 4. Substitute behavior, not just spelling

A pipeline stage can accept any iterable of records and return another iterable, provided its validation, order, ownership, and failure contracts match. A typing Protocol can describe required methods structurally, without forcing inheritance, but annotations still do not enforce the whole semantic contract.

Use ordinary callables or small composed objects when sufficient. An interface should be grounded in the caller's needs rather than an imagined future framework. Reuse works when components agree about both successful values and the cases in which they stop.

## Inspect the type of a preserved cause

An exception's `__cause__` is the explicitly chained exception, or None when no explicit cause was supplied. `type(error.__cause__).__name__` obtains that cause's type object and then its short name, such as `ValueError`. This is a diagnostic observation, not a replacement for catching the actual exception type. `raise AttributeError("missing") from None` deliberately suppresses implicit context in the displayed chain; reserve that choice for a clear boundary rather than hiding an unexplained failure.

References: [Exception chaining](https://docs.python.org/3.13/tutorial/errors.html#exception-chaining).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which handler can catch a custom ValueError subtype.
2. **Explain:** Explain why an explicit cause helps preserve diagnostic information.
3. **Modify:** Add a source identifier to a row error without discarding its cause.
4. **Debug:** Reduce a catch-all handler that incorrectly labels programming bugs as bad data.

<details>
<summary>Hints</summary>

Wrap only the conversion failure and preserve its cause with from.

</details>

## Independent task: exception contracts & interchangeable stages

In `Practice/06_Exception_Contracts_And_Interchangeable_Stages.py`, complete this task:

Define InvalidAmount as a ValueError subtype. Define parse_amount(text), converting integer text, translating conversion ValueError to InvalidAmount with an explicit cause, and rejecting negative results with InvalidAmount. Print parse_amount("12"). For parse_amount("tea"), catch InvalidAmount and print the type name of its explicit cause.

Expected output:

```text
12
ValueError
```
