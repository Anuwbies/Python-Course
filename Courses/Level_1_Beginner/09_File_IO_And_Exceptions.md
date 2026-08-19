# Lesson 9: File I/O & Exception Handling

Real-world production software must persist data to permanent storage (files, disks, databases) and handle unexpected runtime anomalies gracefully without crashing. In this lesson, you will master Python's file operations and exception handling architecture.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Safely open, read, write, and append disk files using the `with` **Context Manager**.
2. Parse structured delimited text (CSV and log records) line-by-line using memory-efficient iterators.
3. Catch and handle runtime exceptions using `try`, `except`, `else`, and `finally`.
4. Target specific exception types (`FileNotFoundError`, `ValueError`, `ZeroDivisionError`, `IndexError`, `KeyError`).
5. Extract debugging context from exception objects using `as err`.
6. Explicitly raise exceptions to enforce data validity using `raise`.

---

## 1. File Handling with Context Managers (`with`)

In older codebases, developers manually opened and closed files (`f = open(...) ... f.close()`). If an unhandled error occurred before `f.close()`, the file handle leaked in memory.

In modern Python, always use the **`with` context manager**. It guarantees that the operating system file descriptor is **automatically closed** the moment execution exits the block, even if an exception is thrown.

### Primary File Modes:
- `"r"`: **Read** (default). Opens for reading. Raises `FileNotFoundError` if the file does not exist.
- `"w"`: **Write**. Creates a new file or **completely overwrites/truncates** an existing file.
- `"a"`: **Append**. Adds new content to the end of the file without overwriting existing data.
- Always specify `encoding="utf-8"` to ensure cross-platform compatibility across Windows, macOS, and Linux.

```python
# 1. Writing lines to a file:
with open("system_config.txt", "w", encoding="utf-8") as file:
    file.write("ENVIRONMENT=PRODUCTION\n")
    file.write("DEBUG=FALSE\n")
    file.write("PORT=8080\n")

# 2. Appending a log record:
with open("system_config.txt", "a", encoding="utf-8") as file:
    file.write("MAX_CONNECTIONS=5000\n")

# 3. Memory-Efficient Line-by-Line Reading:
with open("system_config.txt", "r", encoding="utf-8") as file:
    for line in file:
        clean_line = line.strip()  # Strip trailing newline \n
        if clean_line and not clean_line.startswith("#"):
            key, value = clean_line.split("=")
            print(f"Config Key: {key:<16} | Value: {value}")
```

---

## 2. Exception Handling (`try` / `except`)

An **Exception** is an error detected during code execution (such as dividing by zero, converting non-numeric text to `int`, or opening a non-existent file). Unhandled exceptions terminate your program immediately.

The `try...except` block intercepts exceptions and allows your code to recover or log the error gracefully.

```python
try:
    user_input = input("Enter dividend number: ")
    number = float(user_input)
    result = 1000.0 / number
    print(f"1000 / {number} = {result:.2f}")

except ValueError:
    print("[ERROR] Invalid input! You must enter a numeric value.")

except ZeroDivisionError:
    print("[ERROR] Division by zero is mathematically undefined.")

except Exception as generic_err:
    # Catches any unforeseen standard error
    print(f"[ERROR] An unexpected error occurred: {generic_err}")
```

---

## 3. The Complete `try` - `except` - `else` - `finally` Flow

```python
file_handle = None
try:
    file_handle = open("telemetry.log", "r", encoding="utf-8")
    data = file_handle.read()

except FileNotFoundError:
    print("⚠️ Log file does not exist. Initializing empty buffer.")
    data = ""

else:
    # Executes ONLY if the try block succeeded with ZERO exceptions
    print(f"✅ Successfully loaded {len(data)} characters of log data.")

finally:
    # ALWAYS executes, regardless of whether an exception was raised or handled
    if file_handle:
        file_handle.close()
    print("🔒 File cleanup verification finished.")
```

```
[ START try Block ]
       │
   Error occurred?
   ├── YES ──> [ except Block ] ──> [ finally Block ] ──> [ Exit ]
   └── NO  ──> [ else Block   ] ──> [ finally Block ] ──> [ Exit ]
```

---

## 4. Raising Exceptions Manually (`raise`)

You can enforce business logic and invariants by raising built-in exceptions:

```python
def set_server_port(port: int) -> None:
    """Configures application port within safe unprivileged range."""
    if not (1024 <= port <= 65535):
        raise ValueError(f"Port {port} is invalid! Must be between 1024 and 65535.")
    print(f"Server bound to port {port}.")
```

---

## 💻 Code Example & Reference

See the full working code for this lesson in [Lesson_09_File_IO_And_Exceptions.py](file:///C:/Users/asiro/Desktop/Capstone/Python/Testing/Level_1_Beginner/Lesson_09_File_IO_And_Exceptions.py):

```python
# Safe CSV Grade Parser
def parse_grades_file(file_path: str) -> dict:
    grades = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                clean = line.strip()
                if not clean:
                    continue
                try:
                    name, score_str = clean.split(",")
                    grades.append(float(score_str))
                except (ValueError, IndexError) as parse_err:
                    print(f"⚠️ Skipping corrupted line #{line_num}: '{clean}' ({parse_err})")

        if not grades:
            return {"count": 0, "average": 0.0}

        return {"count": len(grades), "average": sum(grades) / len(grades)}

    except FileNotFoundError:
        print(f"[ERROR] File '{file_path}' not found on disk.")
        return {"count": 0, "average": 0.0}
```

---

## 📝 Quick Exercise: DevOps Access Log Audit & Error Rate Analyzer

### 🏢 Real-Life Scenario
You are developing an automated server access log auditor for a DevOps cloud infrastructure team. Production servers dump daily access records in a comma-delimited format: `timestamp,http_method,endpoint,status_code,latency_ms`. Some records in the file may be malformed, corrupted, or contain non-numeric latencies due to network dropouts. Your script must read the log file, validate each entry with specific exception handling, write corrupted lines to a separate quarantine report, and output a high-level operational performance summary.

### 📋 Requirements
1. Create a helper function `setup_sample_logs(log_path: str)` to write a sample test file containing valid lines, corrupted lines, and HTTP error codes:
   ```text
   2026-08-19 10:00:01,GET,/api/v1/users,200,45.2
   2026-08-19 10:00:02,POST,/api/v1/auth,200,120.8
   CORRUPTED_LINE_WITHOUT_COMMAS
   2026-08-19 10:00:04,GET,/api/v1/products,200,invalid_latency
   2026-08-19 10:00:05,GET,/api/v1/orders,500,850.5
   2026-08-19 10:00:06,POST,/api/v1/checkout,200,210.0
   2026-08-19 10:00:07,DELETE,/api/v1/cache,503,45.0
   ```
2. Define `audit_server_logs(input_log_path: str, error_report_path: str) -> dict`:
   - Enclose file opening in a `try...except FileNotFoundError` block.
   - Use `with open(input_log_path, "r", encoding="utf-8") as infile, open(error_report_path, "w", encoding="utf-8") as errfile:`
   - Iterate over each line:
     - Skip empty lines.
     - Inside an inner `try...except (ValueError, IndexError) as parse_err:`
       - Unpack: `timestamp, method, endpoint, status_str, latency_str = line.strip().split(",")`
       - Cast `status_code = int(status_str)` and `latency_ms = float(latency_str)`
       - Accumulate metrics: `valid_count`, `total_latency`, `status_200_count` (if `status_code == 200`), `server_error_count` (if `status_code >= 500`).
     - In the `except (ValueError, IndexError)` block:
       - Increment `corrupted_count`.
       - Write to `errfile`: `f"CORRUPTED RECORD: {line.strip()}\n"`
   - Compute `avg_latency = round(total_latency / valid_count, 2)` if `valid_count > 0` else `0.0`.
   - Compute `success_rate = (status_200_count / valid_count) * 100.0` if `valid_count > 0` else `0.0`.
   - Return a dictionary of audit metrics.
3. Run the audit, display the operational report, and verify that non-existent input files are handled safely.

> [!IMPORTANT]
> **Strict Constraint**: Use **only** concepts covered in Lessons 1 through 9 (variables, primitives, `input()`, numbers, strings, conditionals, loops, lists, tuples, dictionaries, sets, `def` functions, default arguments, file handling `with open`, `try/except/else/finally/raise`, f-strings, and `print()`). Do **not** use custom OOP classes.

### 🎯 Expected Output
```text
==================================================
           DEVOPS ACCESS LOG AUDIT REPORT         
==================================================
Source Log File:    server_access_log.txt
Total Valid Lines:  5 requests
Corrupted Lines:    2 quarantined to error_log.txt
--------------------------------------------------
PERFORMANCE METRICS:
HTTP 200 OK Count:  3 requests
5xx Server Errors:  2 requests
200 OK Success Rate:60.00%
Average Latency:    254.30 ms
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
def setup_sample_logs(log_path: str) -> None:
    """Generates a test log file containing both valid and corrupted records."""
    log_content = (
        "2026-08-19 10:00:01,GET,/api/v1/users,200,45.2\n"
        "2026-08-19 10:00:02,POST,/api/v1/auth,200,120.8\n"
        "CORRUPTED_LINE_WITHOUT_COMMAS\n"
        "2026-08-19 10:00:04,GET,/api/v1/products,200,invalid_latency\n"
        "2026-08-19 10:00:05,GET,/api/v1/orders,500,850.5\n"
        "2026-08-19 10:00:06,POST,/api/v1/checkout,200,210.0\n"
        "2026-08-19 10:00:07,DELETE,/api/v1/cache,503,45.0\n"
    )
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(log_content)


def audit_server_logs(input_log_path: str, error_report_path: str) -> dict:
    """Safely audits server access logs, handles bad records, and writes error logs."""
    try:
        valid_count = 0
        corrupted_count = 0
        status_200_count = 0
        server_error_count = 0
        total_latency = 0.0

        with open(input_log_path, "r", encoding="utf-8") as infile, open(error_report_path, "w", encoding="utf-8") as errfile:
            for line in infile:
                clean_line = line.strip()
                if not clean_line:
                    continue

                try:
                    parts = clean_line.split(",")
                    if len(parts) != 5:
                        raise IndexError(f"Expected 5 fields, found {len(parts)}")

                    timestamp, method, endpoint, status_str, latency_str = parts
                    status_code = int(status_str)
                    latency_ms = float(latency_str)

                    # Valid record processed
                    valid_count += 1
                    total_latency += latency_ms

                    if status_code == 200:
                        status_200_count += 1
                    elif status_code >= 500:
                        server_error_count += 1

                except (ValueError, IndexError) as parse_err:
                    corrupted_count += 1
                    errfile.write(f"REJECTED [{parse_err}]: {clean_line}\n")

        avg_latency = round(total_latency / valid_count, 2) if valid_count > 0 else 0.0
        success_rate = round((status_200_count / valid_count) * 100.0, 2) if valid_count > 0 else 0.0

        return {
            "source_file": input_log_path,
            "valid_count": valid_count,
            "corrupted_count": corrupted_count,
            "status_200_count": status_200_count,
            "server_error_count": server_error_count,
            "success_rate": success_rate,
            "avg_latency_ms": avg_latency
        }

    except FileNotFoundError:
        print(f"[ERROR] FileNotFoundError: Could not locate log file '{input_log_path}'.")
        return {}


# Execution & Testing
log_file = "server_access_log.txt"
err_file = "error_quarantine_log.txt"

setup_sample_logs(log_file)
audit = audit_server_logs(log_file, err_file)

if audit:
    print("==================================================")
    print("           DEVOPS ACCESS LOG AUDIT REPORT         ")
    print("==================================================")
    print(f"Source Log File:    {audit['source_file']}")
    print(f"Total Valid Lines:  {audit['valid_count']} requests")
    print(f"Corrupted Lines:    {audit['corrupted_count']} quarantined to {err_file}")
    print("--------------------------------------------------")
    print("PERFORMANCE METRICS:")
    print(f"HTTP 200 OK Count:  {audit['status_200_count']} requests")
    print(f"5xx Server Errors:  {audit['server_error_count']} requests")
    print(f"200 OK Success Rate:{audit['success_rate']:.2f}%")
    print(f"Average Latency:    {audit['avg_latency_ms']:.2f} ms")
    print("==================================================")
```
</details>

---

## 🧠 Self-Check Quiz

1. **Why is `with open(...) as f:` preferred over `f = open(...)`?**
   - A) It makes file reading faster.
   - B) It automatically guarantees file closure upon block exit, preventing resource leaks even during errors.
   - C) It is required for Python to compile.
   - D) It encrypts file content on disk.

2. **Which block executes ONLY when no exceptions occur inside the `try` block?**
   - A) `except`
   - B) `finally`
   - C) `else`
   - D) `catch`

3. **What exception type is raised by `float("ninety_nine")`?**
   - A) `TypeError`
   - B) `ValueError`
   - C) `KeyError`
   - D) `IOError`

<details>
<summary><b>View Answers</b></summary>
1: B (Context managers guarantee safe cleanup of file handles)<br>
2: C (The 'else' block runs exclusively when the 'try' block succeeds with zero exceptions)<br>
3: B (Passing an unparseable alphabetic string to float() or int() raises a ValueError)
</details>
