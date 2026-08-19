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

## 4. Raising Exceptions Manually (`raise`)

You can raise exceptions when domain invariants or validation rules are violated:

```python
def set_server_port(port: int) -> None:
    if not (1 <= port <= 65535):
        raise ValueError(f"Port {port} is invalid! Must be between 1 and 65535.")
    print(f"Server bound to port {port}.")
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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import os

CSV_FILE = "daily_transactions.csv"

# 1. Create sample transaction feed (Lesson 9)
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

# 2. Transaction Ingestion Engine (Lessons 1-9)
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

# 3. Run and Display Report
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

# Cleanup
if os.path.exists(CSV_FILE):
    os.remove(CSV_FILE)
```

**Explanation of the Solution:**
- `try...except (ValueError, KeyError)` catches both invalid column formatting, bad numeric conversions, and unrecognized account keys without crashing the batch loop.
- Balances are accurately reconciled in a dictionary with proper overdraft protection checks.
</details>
