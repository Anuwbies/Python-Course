# Lesson 3: While Loops & Sentinels

**Prerequisites:** Level 1 and Lessons 1–2 of this level. **Practice file:** `Practice/03_While_Loops_And_Sentinels.py`.

Repeat an operation while a condition remains true, and make the stopping rule explicit. A loop is a state transition: the values that control the next iteration must change or the same state repeats forever.

## 1. Trace a finite loop

A `while` statement checks its condition before each iteration. The body may therefore execute zero times. Put initialization before the loop, update inside it, and final reporting after it.

```python
remaining = 3
while remaining > 0:
    print(remaining)
    remaining = remaining - 1
print("Finished")
```

| Before test | Condition | Action |
| --- | --- | --- |
| 3 | True | Print 3 and change to 2 |
| 2 | True | Print 2 and change to 1 |
| 1 | True | Print 1 and change to 0 |
| 0 | False | Leave the loop |

If the update were missing, the condition would remain true. If it were placed after the loop, the loop could never reach it. Read the source in execution order rather than assuming an update eventually happens.

## 2. Accumulate across iterations

An accumulator begins with the neutral value for the calculation: 0 for an addition total. Updating it adds each new contribution to what was already collected. Resetting it inside the loop discards earlier contributions.

```python
number = 1
total = 0
while number <= 4:
    total = total + number
    number = number + 1
print(total)  # 10
```

Track the counter and total separately. The counter controls progress; the accumulator records results. Giving them distinct names helps prevent changing the wrong state variable.

## 3. Stop on an explicit command

A sentinel is a special response used to stop repetition. Read and normalize the text, compare it with the sentinel, and convert to a number only on the numeric path. `break` leaves the nearest loop immediately.

```python
total = 0
while True:
    response = input().strip().lower()
    if response == "done":
        break
    amount = int(response)
    total = total + amount
print(total)
```

This example assumes every response other than `done` is valid integer text. The sentinel must be checked before `int()` because the word is not an integer. Typing `done` first gives a total of 0, making the empty-input sequence meaningful.

## 4. Understand the paths you skip

`continue` skips the rest of the current iteration and returns to the next loop test. In a counter-controlled loop, a continue before the counter update can create an infinite loop. With sentinel input, make sure every continued path reads a new response on the next iteration.

For a small menu, `while True` plus a clearly visible quit branch often makes the stopping rule easier to locate. Do not add repeated input without deciding how the user exits and what state is reported after exit.

References: [Python control flow](https://docs.python.org/3.13/tutorial/controlflow.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Trace the counter example from 3 down to its first false condition.
2. **Explain:** Explain why an accumulator belongs outside the loop initialization.
3. **Modify:** Make the sentinel example ignore negative amounts with a condition.
4. **Debug:** Find the missing update in a counter loop that never finishes.

<details>
<summary>Hints</summary>

Check the sentinel before converting its text to an integer.

</details>

## Independent task: while loops & sentinels

In `Practice/03_While_Loops_And_Sentinels.py`, complete this task:

Read one response per line until the response is `done`. Assume all other responses are nonnegative integer amounts. Add the amounts and print `Total: PHP <total>` once after the loop. Do not display prompts.

Sample input:

```text
120
80
done
```

Expected output:

```text
Total: PHP 200
```
