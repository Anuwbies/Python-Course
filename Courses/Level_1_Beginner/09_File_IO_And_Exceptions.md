# Lesson 9: File I/O & Exception Handling

Real-world applications must persist data to storage and handle unexpected errors gracefully without crashing.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Safely open, read, and write files using the `with` context manager.
2. Read text files line-by-line and parse structured data (e.g. CSV).
3. Handle runtime errors using `try`, `except`, `else`, and `finally`.
4. Catch specific exceptions (`ValueError`, `FileNotFoundError`, `ZeroDivisionError`).

---

## 1. File Handling with Context Managers (`with`)

The `with open(...)` syntax guarantees that the file is **automatically closed** even if an error occurs while reading or writing.

### File Open Modes:
- `"r"`: **Read** (default) - raises error if file does not exist.
- `"w"`: **Write** - creates new file or **overwrites** existing file.
- `"a"`: **Append** - adds new data to end of existing file.

```python
# 1. Writing to a file:
with open("students.txt", "w", encoding="utf-8") as file:
    file.write("Alice,95\n")
    file.write("Bob,88\n")
    file.write("Charlie,92\n")

# 2. Reading line-by-line:
with open("students.txt", "r", encoding="utf-8") as file:
    for line in file:
        clean_line = line.strip() # Remove trailing \n
        name, score = clean_line.split(",")
        print(f"Student: {name} | Score: {score}")
```

---

## 2. Exception Handling (`try` / `except`)

Runtime errors (exceptions) crash your program if unhandled. `try...except` blocks allow you to intercept errors and take recovery action.

```python
try:
    user_num = int(input("Enter an integer divisor: "))
    result = 100 / user_num
    print(f"Result: {result}")
except ValueError:
    print("❌ Error: You must enter valid numeric digits.")
except ZeroDivisionError:
    print("❌ Error: Division by zero is mathematically undefined.")
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
```

---

## 3. The Full `try` - `except` - `else` - `finally` Structure

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File was not found on disk!")
else:
    # Runs ONLY if no exceptions were raised in the try block
    print(f"File loaded successfully! Length: {len(content)} characters.")
finally:
    # ALWAYS runs, regardless of whether an error occurred
    print("Closing operations / cleaning up.")
```

---

## 📝 Quick Exercise

**Prompt**:
Write a function `safe_calculate_average(file_path)`:
1. Open and read numbers from `file_path` (one float per line).
2. Compute and return the average.
3. Catch `FileNotFoundError` and return `"Error: File does not exist"`.
4. Catch `ValueError` if any line contains invalid non-numeric data.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def safe_calculate_average(file_path: str):
    try:
        total = 0.0
        count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped: # Skip blank lines
                    total += float(stripped)
                    count += 1
        
        if count == 0:
            return "Error: File is empty."
        return total / count
        
    except FileNotFoundError:
        return "Error: File does not exist."
    except ValueError:
        return "Error: File contains non-numeric data."
    except Exception as err:
        return f"Unexpected error: {err}"
```
</details>

---

## 🧠 Self-Check Quiz

1. **Why is using `with open(...)` preferred over manually calling `f.close()`?**
   - A) It makes file reads $10\times$ faster
   - B) It ensures files are closed automatically even if an exception occurs
   - C) It compresses the file automatically
   - D) Python requires it by law

2. **Which block executes ONLY when no errors occur in the `try` block?**
   - A) `except`
   - B) `finally`
   - C) `else`
   - D) `catch`

3. **What happens if you open a file with `"w"` mode that already exists?**
   - A) It appends to the end
   - B) It throws a `FileExistsError`
   - C) It erases and overwrites the existing file contents
   - D) It opens the file in read-only mode

<details>
<summary><b>View Answers</b></summary>
1: B (Context managers guarantee safe cleanup)<br>
2: C (else only runs when try succeeds without exception)<br>
3: C ('w' mode truncates/overwrites existing files)
</details>
