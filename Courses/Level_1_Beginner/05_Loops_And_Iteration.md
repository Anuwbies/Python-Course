# Lesson 5: Loops & Iteration (`while`, `for`, `range`)

Loops allow your program to repeat a block of code multiple times without code duplication. In this lesson, you will master condition-controlled loops (`while`) and count-controlled sequence loops (`for`).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Construct and control `while` loops safely.
2. Iterate using `for` loops and the `range()` generator.
3. Control loop flow with `break` (exit) and `continue` (skip).
4. Implement the **Accumulator Pattern** to aggregate sums, counts, and averages.

---

## 1. The `while` Loop (Condition-Controlled)

A `while` loop runs repeatedly as long as its condition evaluates to `True`.

```python
count = 1

while count <= 5:
    print(f"Current count: {count}")
    count += 1  # Crucial: update loop variable to avoid infinite loop!

print("Loop finished!")
```

### Interactive Menu Pattern with `while`:
```python
user_choice = ""

while user_choice != "quit":
    user_choice = input("Enter command ('play', 'help', 'quit'): ").strip().lower()
    if user_choice == "play":
        print("🎮 Starting game...")
    elif user_choice == "help":
        print("ℹ️ Help instructions...")
```

---

## 2. The `for` Loop and `range()` (Sequence-Controlled)

The `for` loop iterates over items in any sequence (ranges, lists, strings).

### The `range()` Function:
- `range(stop)`: `range(5)` $\rightarrow$ `0, 1, 2, 3, 4` (starts at `0`, stops before `5`)
- `range(start, stop)`: `range(1, 6)` $\rightarrow$ `1, 2, 3, 4, 5`
- `range(start, stop, step)`: `range(0, 10, 2)` $\rightarrow$ `0, 2, 4, 6, 8`

```python
# Counting up:
for i in range(1, 6):
    print(f"Step {i}")

# Stepping in reverse:
for i in range(5, 0, -1):
    print(f"Countdown: {i}")
print("🚀 Blast off!")

# Iterating over characters in a string:
for char in "Python":
    print(char)
```

---

## 3. Loop Control: `break` and `continue`

- **`break`**: Immediately exits and terminates the enclosing loop.
- **`continue`**: Skips the remaining code in the current iteration and jumps to the next cycle.

```python
# 'break' example: Searching for a target
for num in range(1, 100):
    if num == 7:
        print("Found lucky 7! Stopping search.")
        break
    print(f"Inspecting {num}")

# 'continue' example: Skipping even numbers
for num in range(1, 10):
    if num % 2 == 0:
        continue  # Skip even numbers
    print(f"Odd number: {num}")
```

---

## 4. The Accumulator Pattern

A fundamental computer science pattern where a variable accumulates results across iterations:

```python
# Summing numbers 1 through 100:
total_sum = 0
for n in range(1, 101):
    total_sum += n

print(f"Sum of 1..100 is: {total_sum}")  # 5050
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_5.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Lessons/Lesson_5.py):

```python
# Classic FizzBuzz algorithm (1 to 20):
for i in range(1, 21):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

---

## 📝 Quick Exercise

**Prompt**:
Write a **Multiplication Table Generator**:
1. Prompt the user for an integer $N$ (e.g., `7`).
2. Use a `for` loop from `1` to `10`.
3. Output the table formatted:
   ```text
   7 x 1 = 7
   7 x 2 = 14
   ...
   7 x 10 = 70
   ```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
num = int(input("Enter number for multiplication table: "))

print(f"--- Multiplication Table for {num} ---")
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")
```
</details>

---

## 🧠 Self-Check Quiz

1. **How many times will `for i in range(0, 10, 3):` execute?**
   - A) 3 times (`0, 3, 6`)
   - B) 4 times (`0, 3, 6, 9`)
   - C) 10 times
   - D) 3 times (`3, 6, 9`)

2. **What happens when `break` is executed inside an inner nested loop?**
   - A) It exits all loops completely
   - B) It exits only the innermost loop
   - C) It crashes the program
   - D) It restarts the loop from beginning

3. **What is the value of `x` after this loop finishes?**
   ```python
   x = 0
   for i in range(1, 5):
       if i == 3:
           continue
       x += i
   ```
   - A) `10`
   - B) `7`
   - C) `6`
   - D) `3`

<details>
<summary><b>View Answers</b></summary>
1: B (Values generated are 0, 3, 6, 9)<br>
2: B (break only terminates the closest enclosing loop)<br>
3: B (Adds 1 + 2 + 4 = 7; skips 3)
</details>
