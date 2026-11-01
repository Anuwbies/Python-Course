# Lesson 3: Pytest & Behavior Cases

**Prerequisites:** Levels 1–4 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Pytest_And_Behavior_Cases.py`.

Organize executable expectations so a change can be assessed consistently. A useful test checks an externally meaningful behavior and fails when that behavior is broken.

## 1. Discover small test functions

Pytest is a third-party test runner. Install it in the project environment, then invoke it with that interpreter using `-m pytest`. Files normally start with test_, and test functions normally start with test_. An explicitly named file can also be collected even when its course filename starts with a lesson number.

```python
def remaining(budget, spent):
    return budget - spent

def test_overspending_stays_negative():
    assert remaining(100, 120) == -20
```

The test calls the actual function. Returning a fixed status from a fake helper or printing passed does not test the implementation. A test name should identify the intended behavior so a failure is understandable without rereading every statement.

## 2. Choose cases from the contract

A normal case checks ordinary use. A boundary case probes a limit, such as zero or an empty collection. A rejection case checks how an invalid input is reported. Include repeated calls when state or mutation could leak between uses.

Choose expectations independently. Copying the exact implementation formula into the expected side can reproduce the same mistake and make the test pass. For a small calculation, derive a concrete answer by hand; for a larger one, use a separately justified property or trusted reference.

## 3. Expect a documented exception

`with pytest.raises(ValueError):` describes an operation that must raise that error type. The block fails if no exception occurs or the wrong type escapes. Check meaningful error details when they are part of the contract, without relying on unstable incidental traceback text.

The with syntax is the same resource-management structure already used for files, but this library context manager observes exception behavior. Its implementation is not required to write a simple test correctly; understand exactly what success and failure mean for the block.

## 4. Interpret a passing run honestly

A passing suite covers the cases it actually executes. It does not prove the absence of bugs or establish a coverage percentage. Coverage tools measure executed source lines or branches; a high percentage can still accompany weak assertions.

Keep tests repeatable and independent. Do not depend on execution order, a file left by yesterday's run, or a network service unrelated to the behavior under test. More advanced fixtures and isolated resources follow in the next lesson.

References: [Pytest first tests](https://docs.pytest.org/en/stable/getting-started.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which test fails if the implementation clamps negative balances to zero.
2. **Explain:** Explain why printing passed is not a substitute for an assertion.
3. **Modify:** Add an empty or zero boundary case using the contract.
4. **Debug:** Repair a test whose expected result duplicates the same faulty formula.

<details>
<summary>Hints</summary>

Make each test call the real parser and place only the rejecting call inside raises.

</details>

## Independent task: pytest & behavior cases

In `Practice/03_Pytest_And_Behavior_Cases.py`, complete this task:

Implement `parse_amount(text)` returning a nonnegative integer and raising ValueError for negative or malformed text. In the same file, write three pytest functions for a normal value, zero, and negative rejection using pytest.raises. Run the file explicitly with pytest.

Expected behavior: all three tests pass; changing the function to accept negative values makes the rejection test fail. No fixed console transcript or timing is required.
