# Lesson 4: For Loops & Ranges

**Prerequisites:** Level 1 and Lessons 1–3 of this level. **Practice file:** `Practice/04_For_Loops_And_Ranges.py`.

Use a for loop when the work is to visit the values of a sequence. Distinguish a value being processed from a counter that only tracks its position.

## 1. Visit each value

A `for` statement asks an iterable for its successive values and assigns each one to the loop variable. Strings can be visited one character at a time. You do not need to manually update an index for this operation.

```python
word = "cat"
for letter in word:
    print(letter)
```

The output is c, a, and t on separate lines. The loop variable is reassigned on each iteration; it does not contain the entire history. Accumulating a history requires a separate result, just as a numeric total does.

## 2. Understand exclusive endpoints

`range(stop)` produces integer values starting at zero and stopping before `stop`. `range(start, stop, step)` makes the start and interval explicit. The stop value is excluded so adjacent intervals can meet without counting their shared boundary twice.

```python
total = 0
for day in range(1, 6):
    total = total + day
print(total)  # 15
```

The visited values are 1, 2, 3, 4, and 5. A range with no values causes zero iterations. A descending range needs a negative step, such as `range(3, 0, -1)`. A step of zero is invalid; it cannot describe forward or backward progress.

## 3. Count or accumulate for a reason

A loop over a string can count particular characters or calculate a total. Initialize the accumulator before the loop and update it only when the current value satisfies the intended condition.

```python
text = "banana"
count = 0
for letter in text:
    if letter == "a":
        count = count + 1
print(count)  # 3
```

This combines branching with iteration without introducing a new collection. The result describes all visited characters, so printing the final count belongs after the loop. Printing inside would report intermediate states instead.

## 4. Choose for or while by the stopping rule

Use a for loop for a known sequence of values and a while loop for repetition driven by a changing condition or external command. Both can express many of the same calculations, but the clearer choice makes the stopping rule visible.

`break` and `continue` keep their meanings inside a for loop. The iteration mechanism still advances to the next value after continue, so the missing-manual-counter problem is avoided. Do not assume a loop variable affects the range itself: assigning to `day` does not alter the sequence of values that the range will supply next.

References: [Python data structures](https://docs.python.org/3.13/tutorial/datastructures.html).

## Practice: predict, explain, modify, debug

1. **Predict:** List the values visited by range(2, 8, 2) before running it.
2. **Explain:** Explain why range(1, 6) includes five but excludes six.
3. **Modify:** Count the letter n in the same word without changing the loop structure.
4. **Debug:** Move a final-total print out of the loop and explain the changed output.

<details>
<summary>Hints</summary>

The exclusive endpoint must be one greater than the final integer you want to visit.

</details>

## Independent task: for loops & ranges

In `Practice/04_For_Loops_And_Ranges.py`, complete this task:

Use a for loop over the integers 1 through 5 inclusive. Calculate their total and print the final total once. Do not write five separate additions.

Expected output:

```text
15
```
