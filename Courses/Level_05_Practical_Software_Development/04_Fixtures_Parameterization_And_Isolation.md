# Lesson 4: Fixtures, Parameterization & Isolation

**Prerequisites:** Levels 1–4 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Fixtures_Parameterization_And_Isolation.py`.

Use test data deliberately and isolate state between cases. Reusing setup should make a test clearer without concealing which values and resources the test actually depends on.

## 1. Reuse a set of examples

A parameterized test runs the same behavior assertion for several input/expected pairs. `@pytest.mark.parametrize` is decorator syntax: the library attaches case metadata to the following function so the runner can supply each pair. Writing custom decorators is a Level 7 topic; here the public library contract is enough to use its registration mechanism.

```python
import pytest

@pytest.mark.parametrize("amount, expected", [(0, 0), (10, 10)])
def test_identity_amount(amount, expected):
    assert int(str(amount)) == expected
```

Each pair is a distinct reported test case. This is more informative than a loop whose first failure hides all remaining cases. Choose cases because they represent meaningful partitions, not merely because a table can hold many rows.

## 2. Let fixtures declare dependencies

A fixture is a named setup function registered with `@pytest.fixture`. A test requests its value through a parameter with that name. Pytest resolves the dependency; it is not an unexplained global variable inserted into ordinary Python calls.

Use narrow fixture scopes until sharing is justified. A shared mutable collection can leak changes between tests if its scope is wider than expected. A fresh list per test makes the independence explicit.

## 3. Isolate filesystem work

The built-in tmp_path fixture supplies an isolated Path for each test. Write the exact sample file needed by that test, call the real loader, and inspect the returned data. Do not rely on a fixed filename in the repository root or a user's existing documents.

The monkeypatch fixture can temporarily replace environment variables or a dependency at a documented boundary. Replacing the function under test itself with a fake expected answer would remove the behavior the test was meant to exercise.

## 4. Exercise failure and state preservation

For a save operation, checking only that a file exists is weak evidence. Read it back and compare meaningful values. For a rejection path, inspect that prior state was not changed. Tests of malformed data should create that malformed data themselves so the cause is reproducible.

Keep fixture names specific. A large generic setup containing files, database state, and credentials can hide unrelated assumptions. If a test needs only a list, give it a list; if it needs a path, provide a path whose contents are visible in the test.

References: [Pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the number of cases produced by a three-row parameter table.
2. **Explain:** Explain how pytest supplies a fixture parameter.
3. **Modify:** Write one malformed JSON file using tmp_path for a rejection case.
4. **Debug:** Identify shared mutable fixture state that makes test order matter.

<details>
<summary>Hints</summary>

Each case writes its own data and observes the actual loader result.

</details>

## Independent task: fixtures, parameterization & isolation

In `Practice/04_Fixtures_Parameterization_And_Isolation.py`, complete this task:

Define `load_amounts(path)` to load a JSON list of plain nonnegative integers or raise ValueError. Write a parameterized pytest test for `[]`, `[0]`, and `[10, 20]`, writing each input through tmp_path and calling the real loader. Add one rejection test for `[True]`.

Expected behavior: the four collected cases pass independently and require no preexisting files.
