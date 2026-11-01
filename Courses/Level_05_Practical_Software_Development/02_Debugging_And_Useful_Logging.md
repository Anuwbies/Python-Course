# Lesson 2: Debugging & Useful Logging

**Prerequisites:** Levels 1–4 and Lesson 1 of this level. **Practice file:** `Practice/02_Debugging_And_Useful_Logging.py`.

Investigate a discrepancy with evidence and leave useful diagnostic information at meaningful boundaries. Debugging finds the cause; logging preserves enough context to diagnose later executions.

## 1. Reproduce before editing

Reduce a failure to the smallest input that still shows the wrong behavior. Write the expected result independently of the implementation. Inspect the first point where actual state differs from that expectation, rather than changing several lines until a sample happens to pass.

```python
def total_amounts(amounts):
    total = 0
    for amount in amounts:
        total = total + amount
    return total

print(total_amounts([10, 20]))
```

A breakpoint before the update lets you inspect total and amount on each iteration. Step into follows a function call; step over executes a line without descending into it. Temporary prints can also be useful, but remove noisy diagnostics from the function's intended return/output contract afterward.

## 2. Read tracebacks from the failure outward

The final traceback line describes the exception; preceding frames show how execution reached it. Find the nearest relevant frame in your source. A broad handler that prints only something went wrong destroys this context unless it logs the actual exception with its traceback.

`breakpoint()` invokes Python's configured debugger. Use it deliberately during investigation, not as a forgotten pause in a shared reference program. The debugger can change state, so rerun the clean case after the fix to ensure the result was not caused by an interactive edit.

## 3. Use named loggers

The logging module separates diagnostic events from application output. `logging.getLogger(__name__)` gives a logger identified by its module. Configure handlers and formatting in the launcher, rather than having every reusable function reset global configuration.

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Processed %s records", 3)
```

The message may not be displayed until configuration enables that level. Parameterized logging keeps values separate from the format string. Never include credentials or entire sensitive payloads merely because a log is called debug.

## 4. Match levels to meaning

Debug describes investigation details, info ordinary progress, warning a noteworthy recoverable issue, and error a failed operation. Repeating an error as several unrelated messages can obscure the original cause. At an exception boundary, logger.exception includes the traceback for the active exception.

Logs do not establish that an operation happened: place a completion event after the operation succeeds. A message saying saved before the write completes can mislead an operator when the write fails. Keep user reports on stdout and diagnostics on their configured stream so each can be interpreted separately.

## Enable the diagnostic you intend to observe

Configure the launcher before its first logging call:

```python
import logging

logger = logging.getLogger(__name__)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
    logger.info("Loaded %s records", 2)
    print("Ready")
```

INFO is the level constant. The format names the level and rendered message. basicConfig normally installs a stderr handler when no root handler exists; stdout still contains the ordinary report. The `%s` placeholders in logger.info are filled from its following arguments. They are distinct from f-string braces and from the `%(...)s` field names in the logging configuration.

References: [Logging HOWTO](https://docs.python.org/3.13/howto/logging.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Trace the accumulator for an empty list and a two-item list.
2. **Explain:** Explain why a success log belongs after the successful operation.
3. **Modify:** Add a debug event identifying the count without logging every record.
4. **Debug:** Find an error handler that hides the original traceback.

<details>
<summary>Hints</summary>

Configure diagnostics only in the launcher; the function returns its numeric result.

</details>

## Independent task: debugging & useful logging

In `Practice/02_Debugging_And_Useful_Logging.py`, complete this task:

Define `total_amounts(amounts)` for nonnegative integer amounts and log the number of records at info level without printing from the function. Configure logging in the guarded launcher, call the function for `[10, 20]`, and print `Total: 30` to stdout. The diagnostic log should separately identify 2 records.

Expected output:

```text
Total: 30
```
