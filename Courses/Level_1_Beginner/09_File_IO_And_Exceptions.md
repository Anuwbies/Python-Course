# Lesson 9: File I/O & Robust Exception Handling

Software applications in production must interact with the host filesystem—reading configuration files, streaming logs, writing reports—while remaining resilient against unexpected hardware, network, or data format failures. In this lesson, you will master Python's file input/output operations using the `with` context manager and build fault-tolerant programs using `try...except...else...finally` exception handling blocks.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Open, read, write, and append to filesystem files safely using the `with open()` context manager.
2. Choose appropriate file access modes (`'r'`, `'w'`, `'a'`) and specify text encodings (`encoding="utf-8"`).
3. Handle runtime exceptions cleanly with `try` and `except` blocks to prevent application crashes.
4. Catch specific exceptions (`FileNotFoundError`, `ValueError`, `PermissionError`, `ZeroDivisionError`).
5. Understand the distinct roles of the `else` and `finally` exception clauses.
6. Explicitly trigger error conditions using the `raise` keyword.

---

## 1. File Handling with Context Managers (`with open`)

Always interact with files using the `with` statement. The context manager guarantees that the underlying file descriptor is immediately closed and flushed when the block exits, even if an unhandled exception occurs inside.

```python
# 1. Writing to a file ('w' mode overwrites existing content):
with open("system_config.txt", "w", encoding="utf-8") as f:
    f.write("PORT=8080\n")
    f.write("ENV=production\n")
    f.write("MAX_WORKERS=16\n")

# 2. Appending data ('a' mode adds to the end of the file):
with open("system_config.txt", "a", encoding="utf-8") as f:
    f.write("DEBUG=false\n")

# 3. Reading line-by-line efficiently without loading large files entirely into RAM:
with open("system_config.txt", "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, start=1):
        clean_line = line.strip()
        print(f"Line {line_number}: {clean_line}")
```

---

## 2. Exception Handling: `try...except`

An **exception** is an event that disrupts the normal flow of instructions. Unhandled exceptions cause the Python interpreter to print a traceback and terminate immediately.

```python
# Unhandled crash:
# raw_num = int("forty-two") # ❌ ValueError: invalid literal for int()

# Handled safely:
try:
    raw_num = int("forty-two")
    print(f"Parsed Number: {raw_num}")
except ValueError as err:
    print(f"⚠️ Parsing Failed: {err}. Using fallback value 0.")
    raw_num = 0
```

---

## 3. The Full `try...except...else...finally` Architecture

Python provides a 4-part exception handling structure:

```
try:
    [ Code that might raise an error ]
except SpecificError as e:
    [ Executes ONLY if a matching error occurred ]
else:
    [ Executes ONLY if NO error occurred in the try block ]
finally:
    [ ALWAYS executes regardless of whether an error occurred or was caught ]
```

```python
def read_metric_file(filepath: str) -> None:
    file_handle = None
    try:
        file_handle = open(filepath, "r", encoding="utf-8")
        content = file_handle.read()
        val = float(content.strip())
        print(f"Metric value: {val}")
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' does not exist on disk.")
    except ValueError:
        print("❌ Error: File content could not be parsed as a floating-point number.")
    else:
        print("✅ Metric successfully ingested and verified.")
    finally:
        if file_handle and not file_handle.closed:
            file_handle.close()
            print("🔒 File handle explicitly closed.")
```

---

## 4. Modern Path Handling with `pathlib.Path`

In modern Python 3.4+, **`pathlib`** is the standard, object-oriented, cross-platform filesystem library that replaces older `os.path` functions:

```python
from pathlib import Path

# Constructing cross-platform paths using the division (/) operator:
base_dir = Path("data") / "telemetry"
config_file = base_dir / "settings.json"

# Creating parent directories safely (mkdir -p equivalent):
base_dir.mkdir(parents=True, exist_ok=True)

# Rapid text writing and reading without explicit with-open boilerplate:
config_file.write_text('{"env": "production", "debug": false}', encoding="utf-8")
print(config_file.read_text(encoding="utf-8"))

# Inspecting file properties:
print(f"Exists: {config_file.exists()}")
print(f"Is File: {config_file.is_file()}")
print(f"File Name: {config_file.name}, Stem: {config_file.stem}, Suffix: {config_file.suffix}")
```

---

## 5. The Python Exception Hierarchy & Anti-Patterns

All exceptions in Python inherit from `BaseException`:

```
BaseException
 ├── SystemExit (Triggered by sys.exit())
 ├── KeyboardInterrupt (Triggered by Ctrl+C)
 └── Exception (Base class for all non-exit exceptions)
      ├── StandardError
      │    ├── ArithmeticError (ZeroDivisionError, OverflowError)
      │    ├── LookupError (IndexError, KeyError)
      │    ├── ValueError
      │    ├── TypeError
      │    └── OSError (FileNotFoundError, PermissionError)
      └── ...
```

> [!CAUTION]
> **Never use a bare `except:` or `except BaseException:`!**
> Catching `BaseException` will intercept `KeyboardInterrupt` (preventing you from stopping a runaway loop with `Ctrl+C`) and `SystemExit`.
> Always catch specific exceptions (e.g. `except (ValueError, FileNotFoundError):`), or at most `except Exception:` for top-level fallback logging.

---

## 6. Raising Exceptions & Exception Chaining (`from`)

You can raise exceptions when domain invariants are violated, and preserve original traceback context using `raise ... from err`:

```python
def parse_positive_int(raw_text: str) -> int:
    try:
        val = int(raw_text)
        if val <= 0:
            raise ValueError(f"Value must be strictly positive, got {val}")
        return val
    except ValueError as err:
        # Explicit exception chaining preserving root cause context:
        raise RuntimeError("Configuration parsing failure") from err
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Security Access Log Parser & Intrusion Detection Ingestor**, combining all file I/O, string parsing, and exception handling mechanics taught in this lesson:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Security Access Log Ingestion & Threat Auditor
# =====================================================================

import os

AUDIT_LOG_FILENAME = "security_access.log"
ALERT_REPORT_FILENAME = "security_alerts.txt"

# 1. Generate sample log file to disk (Lesson 9 File I/O)
sample_log_data = """2026-08-19 14:00:01,192.168.1.50,admin,AUTH_SUCCESS
2026-08-19 14:01:22,203.0.113.195,root,AUTH_FAILURE
2026-08-19 14:01:25,203.0.113.195,root,AUTH_FAILURE
2026-08-19 14:01:29,203.0.113.195,root,AUTH_FAILURE
2026-08-19 14:02:10,192.168.1.88,marcus,AUTH_SUCCESS
CORRUPTED_LINE_WITHOUT_CSV_COMMAS_OR_PROPER_DATA
2026-08-19 14:03:00,203.0.113.195,root,AUTH_FAILURE
2026-08-19 14:04:15,10.0.0.12,guest,INVALID_PAYLOAD_FORMAT,EXTRA_FIELD
"""

with open(AUDIT_LOG_FILENAME, "w", encoding="utf-8") as f:
    f.write(sample_log_data)

# 2. Resilient Log Parser with Exception Handling (Lessons 1-9)
def parse_security_logs(filepath: str) -> dict:
    """Parses access logs, sanitizing corrupted entries and detecting threats."""
    stats = {
        "total_lines": 0,
        "valid_events": 0,
        "corrupted_lines": 0,
        "failed_logins_by_ip": {},
        "threat_ips": set()
    }
    
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_no, raw_line in enumerate(file, start=1):
                stats["total_lines"] += 1
                line = raw_line.strip()
                if not line:
                    continue
                
                try:
                    parts = line.split(",")
                    if len(parts) != 4:
                        raise ValueError(f"Expected 4 CSV fields, found {len(parts)}")
                    
                    timestamp, ip_address, username, status = parts
                    stats["valid_events"] += 1
                    
                    if status == "AUTH_FAILURE":
                        current_failures = stats["failed_logins_by_ip"].get(ip_address, 0) + 1
                        stats["failed_logins_by_ip"][ip_address] = current_failures
                        
                        # Trigger threat flag if failures exceed threshold
                        if current_failures >= 3:
                            stats["threat_ips"].add(ip_address)
                            
                except ValueError as parse_err:
                    stats["corrupted_lines"] += 1
                    # Log internal warning without crashing loop
                    # print(f"⚠️ [Line {line_no}] Parse Error: {parse_err}")
                    
    except FileNotFoundError:
        print(f"❌ Critical Error: Could not locate log file '{filepath}'.")
        return stats
    except PermissionError:
        print(f"❌ Security Error: Insufficient OS permissions to read '{filepath}'.")
        return stats
    else:
        print("✅ Log file successfully ingested and analyzed.")
    finally:
        print("🔒 Log ingestion stream closed.")
        
    return stats

# 3. Execute Analysis and Write Threat Alert Report
audit_results = parse_security_logs(AUDIT_LOG_FILENAME)

with open(ALERT_REPORT_FILENAME, "w", encoding="utf-8") as report_file:
    report_file.write("==================================================\n")
    report_file.write("          SECURITY INTRUSION ALERT REPORT         \n")
    report_file.write("==================================================\n")
    report_file.write(f"Total Lines Processed:  {audit_results['total_lines']}\n")
    report_file.write(f"Valid Security Events:  {audit_results['valid_events']}\n")
    report_file.write(f"Corrupted Lines Skipped:{audit_results['corrupted_lines']}\n")
    report_file.write("--------------------------------------------------\n")
    report_file.write("DETECTED BRUTE FORCE ATTACK IPs (>=3 Failures):\n")
    for threat_ip in audit_results["threat_ips"]:
        fail_count = audit_results["failed_logins_by_ip"][threat_ip]
        report_file.write(f"  🚨 Threat IP: {threat_ip:<18} ({fail_count} Failed Attempts)\n")
    report_file.write("==================================================\n")

# Display generated report content
with open(ALERT_REPORT_FILENAME, "r", encoding="utf-8") as f:
    print("\n" + f.read())

# Cleanup temporary disk files
if os.path.exists(AUDIT_LOG_FILENAME):
    os.remove(AUDIT_LOG_FILENAME)
if os.path.exists(ALERT_REPORT_FILENAME):
    os.remove(ALERT_REPORT_FILENAME)
```

### 🔍 Code Explanation:
- **`with open(..., "w")` & `"r"`**: Demonstrates safe file creation and streaming iteration across records.
- **Nested `try...except`**: The outer `try` handles operating system I/O errors (`FileNotFoundError`, `PermissionError`), while the inner `try` catches record-level `ValueError` parsing issues, preventing a single malformed row from crashing the entire batch.
- **Dictionary & Set Aggregation**: `failed_logins_by_ip` tracks counts while `threat_ips` collects unique attacker IP addresses.
- **`finally` Block**: Always runs to verify that the parsing phase is complete.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master context managers, file stream I/O, `pathlib`, custom error validation, exception hierarchies, and resilient error recovery:

---

### 🟢 Tier 1: File Writing & Reading Basics (Exercises 1–3)

#### 🔹 Exercise 1: Single-Line Config Writer & Reader
* **Goal**: Use `with open("server_port.cfg", "w")` to write `"PORT=8080"`.
* **Requirement**: Reopen in `"r"` mode, read the string, and print the parsed integer port.

#### 🔹 Exercise 2: Multi-Line Activity Log Appender
* **Goal**: Open a file `"audit_trail.log"` in `"a"` (append) mode.
* **Requirement**: Append three timestamped event lines. Reopen in `"r"` mode and print total line count.

#### 🔹 Exercise 3: Safe Division with ZeroDivisionError Guard
* **Goal**: Write a function `safe_divide(numerator: float, denominator: float) -> float`.
* **Requirement**: Catch `ZeroDivisionError` and return `0.0`.

---

### 🟡 Tier 2: Pathlib & Multi-Exception Handling (Exercises 4–6)

#### 🔹 Exercise 4: Modern `pathlib.Path` Ingestor
* **Goal**: Use `Path("config.json")`.
* **Requirement**: Write JSON text using `.write_text()`, verify existence with `.exists()`, read text with `.read_text()`, and delete with `.unlink()`.

#### 🔹 Exercise 5: Multi-Exception Block with `else` and `finally`
* **Goal**: Prompt for a filename and integer divisor.
* **Requirement**: Structure a full `try...except (FileNotFoundError, ValueError, ZeroDivisionError)...else...finally` block that reliably reports whether execution succeeded.

#### 🔹 Exercise 6: Line-by-Line Filter Stream
* **Goal**: Write a 10-line text file containing mixed log levels (`INFO`, `WARNING`, `ERROR`).
* **Requirement**: Stream line by line and write only `ERROR` lines to `"errors_only.log"`.

---

### 🟠 Tier 3: Custom Invariants & Exception Chaining (Exercises 7–9)

#### 🔹 Exercise 7: User Age Domain Invariant Validator
* **Goal**: Write a function `validate_user_age(age_str: str) -> int`.
* **Rules**: If non-digit, catch and raise `ValueError("Age must be integer")`. If `not (0 <= age <= 120)`, raise `ValueError("Age out of human bounds")`.

#### 🔹 Exercise 8: Exception Chaining with `raise ... from`
* **Goal**: Write a function `load_database_port(filepath: str) -> int`.
* **Requirement**: If file reading or parsing fails, catch the error and `raise RuntimeError("Database config unavailable") from err`.

#### 🔹 Exercise 9: CSV Record Cleaner with Skipped Malformed Lines
* **Goal**: Given a CSV string with varying column lengths and bad numbers.
* **Requirement**: Parse line by line; accumulate valid records into a list of dicts while logging line numbers of corrupted rows into a `skipped_lines` list.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Bank Transaction CSV Ingestion & Balance Reconciler
* **Goal**: Read and validate CSV financial transactions, update account balances in memory, guard against overdrafts and corrupted rows, and print reconciliation summary.

---

## 📝 Quick Exercise: Bank Account Transaction CSV Importer & Balance Reconciler

### 🏢 Real-Life Scenario
You are developing the transaction ingestion service for a core banking core platform. The bank receives automated daily CSV transaction feeds from ATM and POS networks. Because raw network feeds can occasionally contain corrupt rows, negative numbers, missing columns, or bad characters, your module must safely parse valid transactions, update customer balances, skip bad rows without crashing, and write an audited reconciliation report to disk.

### 📋 Requirements
1. **Prepare test CSV file on disk (`daily_transactions.csv`)**:
   ```python
   csv_content = """TXN-101,SAVINGS,DEPOSIT,500.00
   TXN-102,CHECKING,WITHDRAW,150.00
   TXN-CORRUPT-BAD-FORMAT
   TXN-103,CHECKING,DEPOSIT,invalid_amount
   TXN-104,SAVINGS,WITHDRAW,200.00
   TXN-105,CHECKING,WITHDRAW,1200.00
   TXN-106,INVESTMENT,DEPOSIT,1000.00
   """
   ```
2. **Define `process_transactions_csv` function**:
   - Signature: `def process_transactions_csv(filepath: str) -> dict`
   - Initial balances dictionary:
     `balances = {"SAVINGS": 1500.00, "CHECKING": 800.00, "INVESTMENT": 5000.00}`
   - Open and read the CSV file line by line inside a `try...except` block.
   - For each line:
     - Split by `,`. If parts count is not 4, raise and catch `ValueError`.
     - Cast the 4th element (amount) to `float`. If amount is non-numeric or $\le 0$, catch `ValueError`.
     - Check if account exists in `balances`. If not, catch `KeyError`.
     - If `action == "DEPOSIT"`: Add amount to account balance.
     - If `action == "WITHDRAW"`: If `amount <= balances[account]`, deduct amount; else record as an overdraft rejection.
3. Output the reconciliation summary to console using formatted f-strings.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine concepts from **Lessons 1 through 9** (variables, types, casting, math, conditionals, loops, lists, tuples, dicts, functions, `with open()`, and `try...except`).

### 🎯 Expected Output
```text
==================================================
       DAILY TRANSACTION AUDIT & RECONCILER       
==================================================
Total Raw Rows:        7
Successfully Processed:4
Corrupt Rows Skipped:  2
Overdraft Rejections:  1
--------------------------------------------------
FINAL RECONCILED ACCOUNT BALANCES:
  - CHECKING:    $650.00
  - INVESTMENT:  $6,000.00
  - SAVINGS:     $1,800.00
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Transaction CSV & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Bank Transaction Ingestion Engine
# =====================================================================
import os

CSV_FILE = "daily_transactions.csv"

sample_csv = """TXN-101,SAVINGS,DEPOSIT,500.00
TXN-102,CHECKING,WITHDRAW,150.00
TXN-CORRUPT-BAD-FORMAT
TXN-103,CHECKING,DEPOSIT,invalid_amount
TXN-104,SAVINGS,WITHDRAW,200.00
TXN-105,CHECKING,WITHDRAW,1200.00
TXN-106,INVESTMENT,DEPOSIT,1000.00
"""

with open(CSV_FILE, "w", encoding="utf-8") as f:
    f.write(sample_csv)

def process_transactions_csv(filepath: str) -> dict:
    balances = {"SAVINGS": 1500.00, "CHECKING": 800.00, "INVESTMENT": 5000.00}
    stats = {"total_rows": 0, "success": 0, "corrupt": 0, "overdraft": 0}

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for raw_line in file:
                line = raw_line.strip()
                if not line:
                    continue
                stats["total_rows"] += 1

                try:
                    parts = line.split(",")
                    if len(parts) != 4:
                        raise ValueError(f"Invalid column count: {len(parts)}")
                    
                    txn_id, account, action, amount_str = parts
                    amount = float(amount_str)
                    if amount <= 0:
                        raise ValueError("Amount must be positive.")
                    
                    if account not in balances:
                        raise KeyError(f"Unknown account type: {account}")

                    if action == "DEPOSIT":
                        balances[account] += amount
                        stats["success"] += 1
                    elif action == "WITHDRAW":
                        if balances[account] >= amount:
                            balances[account] -= amount
                            stats["success"] += 1
                        else:
                            stats["overdraft"] += 1
                    else:
                        raise ValueError(f"Unknown action: {action}")

                except (ValueError, KeyError):
                    stats["corrupt"] += 1

    except FileNotFoundError:
        print(f"❌ Error: File {filepath} not found.")

    return {"stats": stats, "balances": balances}

results = process_transactions_csv(CSV_FILE)
st = results["stats"]
bal = results["balances"]

print("==================================================")
print("       DAILY TRANSACTION AUDIT & RECONCILER       ")
print("==================================================")
print(f"Total Raw Rows:        {st['total_rows']}")
print(f"Successfully Processed:{st['success']}")
print(f"Corrupt Rows Skipped:  {st['corrupt']}")
print(f"Overdraft Rejections:  {st['overdraft']}")
print("--------------------------------------------------")
print("FINAL RECONCILED ACCOUNT BALANCES:")
for acc_name in sorted(bal.keys()):
    print(f"  - {acc_name:<12} ${bal[acc_name]:,.2f}")
print("==================================================")

if os.path.exists(CSV_FILE):
    os.remove(CSV_FILE)

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1:
with open("port.cfg", "w") as f: f.write("PORT=8080\n")
with open("port.cfg", "r") as f: port = int(f.read().strip().split("=")[1])
print(f"Parsed Port: {port}")
os.remove("port.cfg")

# Ex 2:
with open("audit.log", "a") as f:
    f.write("EVT-1: Init\nEVT-2: Auth\nEVT-3: Ready\n")
with open("audit.log", "r") as f: lines = len(f.readlines())
print(f"Audit Lines: {lines}")
os.remove("audit.log")

# Ex 3:
def safe_divide(n: float, d: float) -> float:
    try: return n / d
    except ZeroDivisionError: return 0.0

# Ex 4:
from pathlib import Path
p = Path("test_cfg.json")
p.write_text('{"status": "ok"}', encoding="utf-8")
print(f"Pathlib Content: {p.read_text()}")
p.unlink()

# Ex 5:
try:
    val = 100 / int("10")
except (ValueError, ZeroDivisionError) as err:
    print(f"Handled error: {err}")
else:
    print(f"Calculated result: {val}")
finally:
    print("Execution complete.")

# Ex 6:
raw_logs = "INFO: boot\nERROR: disk full\nWARNING: mem high\nERROR: timeout\n"
Path("all.log").write_text(raw_logs)
with open("all.log", "r") as src, open("err.log", "w") as dst:
    for l in src:
        if l.startswith("ERROR:"): dst.write(l)
print(f"Errors Filtered:\n{Path('err.log').read_text()}")
Path("all.log").unlink(); Path("err.log").unlink()

# Ex 7:
def validate_user_age(age_str: str) -> int:
    try: a = int(age_str)
    except ValueError: raise ValueError("Age must be integer")
    if not (0 <= a <= 120): raise ValueError("Age out of human bounds")
    return a

# Ex 8:
def load_database_port(filepath: str) -> int:
    try:
        with open(filepath) as f: return int(f.read().strip())
    except Exception as err:
        raise RuntimeError("Database config unavailable") from err

# Ex 9:
csv_data = "user1,25\nbad_row\nuser2,not_num\nuser3,30"
records, skipped = [], []
for idx, row in enumerate(csv_data.split("\n"), start=1):
    parts = row.split(",")
    if len(parts) == 2 and parts[1].isdigit():
        records.append({"user": parts[0], "age": int(parts[1])})
    else:
        skipped.append(idx)
print(f"Valid: {records} | Skipped Row Indices: {skipped}")
```
</details>

