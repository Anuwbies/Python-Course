"""
================================================================================
Level 1: Beginner Python
Lesson 9: File I/O & Exception Handling
================================================================================
📝 Quick Exercise: DevOps Access Log Audit & Error Rate Analyzer

🏢 Real-Life Scenario:
You are developing an automated server access log auditor for a DevOps cloud
infrastructure team. Production servers dump daily access records in a
comma-delimited format: timestamp,http_method,endpoint,status_code,latency_ms.
Some records in the file may be malformed or corrupted. Your script must read the
log file, validate each entry with specific exception handling, write corrupted
lines to a separate quarantine report, and output an operational summary.

📋 Requirements:
1. setup_sample_logs(log_path): Generates sample test file with valid/corrupted lines.
2. audit_server_logs(input_log_path, error_report_path) -> dict:
   - Uses try...except FileNotFoundError.
   - Reads line by line with context managers.
   - Catches (ValueError, IndexError) on bad lines and writes them to error report.
   - Computes valid requests, 200 OK count, 5xx server errors, success rate, average latency.
3. Execute and display the audit summary.

⚠️ Strict Constraint:
Use ONLY concepts covered in Lessons 1-9 (variables, primitives, input(), numbers,
strings, conditionals, loops, lists, tuples, dictionaries, sets, def functions,
default arguments, file handling with open, try/except/else/finally/raise,
f-strings, and print()). No custom OOP classes.
================================================================================
"""

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