# Lesson 5: Memory-Efficient Streams: Iterators & Generators

In enterprise software systems dealing with gigabytes of web server logs, real-time financial order books, or database query feeds, attempting to load all records into a Python `list` will exhaust system memory (causing fatal `MemoryError` out-of-memory crashes). In this lesson, you will master Python's lazy evaluation engine: the **Iterator Protocol**, generator functions with `yield`, generator expressions, and streaming data pipelines.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the difference between **Iterables** and **Iterators**.
2. Implement custom iterator classes adhering to the **Iterator Protocol** (`__iter__` and `__next__`).
3. Build memory-efficient streaming functions using the `yield` keyword.
4. Compose lazy one-line **Generator Expressions**.
5. Connect multi-stage **Streaming Data Processing Pipelines** with $O(1)$ memory footprint.
6. Handle `StopIteration` gracefully across manual iteration loops.

---

## 1. The Iterator Protocol (`__iter__` and `__next__`)

An **Iterable** is any object that can return an iterator (e.g., `list`, `tuple`, `dict`).
An **Iterator** is an object representing a stream of data that produces one element at a time when `next()` is called on it:

```python
class FibonacciIterator:
    """Memory-efficient iterator producing first N Fibonacci numbers."""
    
    def __init__(self, limit: int):
        self.limit = limit
        self.count = 0
        self.a, self.b = 0, 1

    def __iter__(self):
        # An iterator must return itself from __iter__
        return self

    def __next__(self) -> int:
        if self.count >= self.limit:
            # Signal iteration completion
            raise StopIteration
            
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return result

# Usage in a standard for loop:
for num in FibonacciIterator(6):
    print(num, end=" ") # 0 1 1 2 3 5
print()
```

---

## 2. Generator Functions & The `yield` Keyword

Writing class-based iterators requires managing state variables manually. A **Generator Function** simplifies this by using `yield`:

> [!NOTE]
> When a function calls `yield`, Python freezes its execution state (local variables, instruction pointer) and returns the yielded value to the caller. When `next()` is called again, execution resumes immediately after the `yield` statement.

```python
def date_range_generator(start_year: int, end_year: int):
    """Yields years lazily without preallocating a list in RAM."""
    current = start_year
    while current <= end_year:
        yield current
        current += 1

gen = date_range_generator(2024, 2026)
print(next(gen)) # 2024
print(next(gen)) # 2025
print(next(gen)) # 2026
# next(gen) -> ❌ Raises StopIteration automatically!
```

---

## 3. List vs. Generator Memory Comparison

```python
import sys

# Pre-allocated List: 10,000,000 numbers stored in RAM
# list_data = [x for x in range(10_000_000)] # Consumes ~80 Megabytes of RAM!

# Lazy Generator Expression: Generates numbers on demand
gen_data = (x for x in range(10_000_000))

print(f"Generator memory footprint: {sys.getsizeof(gen_data)} bytes!")
# Output: ~200 bytes regardless of whether range is 10 or 10 billion!
```

---

## 4. Multi-Stage Streaming Pipelines

Generators can be chained like Unix pipes (`cat log | grep ERROR | awk ...`), passing data downstream item-by-item without intermediate list buffers:

```python
raw_log_stream = [
    "2026-08-19 INFO User logged in",
    "2026-08-19 WARN Disk latency high",
    "2026-08-19 ERROR Database replica failed",
    "2026-08-19 ERROR Out of memory exception",
]

# Stage 1: Filter error lines
error_lines = (line for line in raw_log_stream if "ERROR" in line)

# Stage 2: Extract error message body
error_messages = (line.split("ERROR ")[1] for line in error_lines)

# Stage 3: Consume lazily
for msg in error_messages:
    print(f"🚨 Alert Dispatched: {msg}")
```

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Cloud Server Telemetry Ingestion & Anomaly Streaming Pipeline**, combining custom class iterators, generator functions, lazy filtering, and pipeline transformations:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Cloud Server Telemetry Ingestion & Anomaly Streamer
# =====================================================================

import time

# 1. Custom Class Iterator for Server Metric Samples (Lesson 5)
class TelemetrySensorBatch:
    def __init__(self, raw_samples: list[dict]):
        self._samples = raw_samples
        self._index = 0

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self) -> dict:
        if self._index >= len(self._samples):
            raise StopIteration
        sample = self._samples[self._index]
        self._index += 1
        return sample


# 2. Generator Functions for Stream Processing (Lesson 5)
def stream_raw_telemetry(sensor_stream):
    """Simulates real-time telemetry streaming."""
    for record in sensor_stream:
        yield record

def filter_healthy_nodes(record_stream):
    """Passes only unhealthy or degraded nodes downstream."""
    for record in record_stream:
        # Check if CPU > 80% or Memory > 85% or Status is Degraded
        if record["cpu_pct"] > 80.0 or record["mem_pct"] > 85.0 or record["status"] != "HEALTHY":
            yield record

def enrich_anomaly_metadata(anomaly_stream):
    """Enriches anomaly records with incident urgency and remediation steps."""
    for anomaly in anomaly_stream:
        urgency = "CRITICAL" if (anomaly["cpu_pct"] > 90.0 or anomaly["mem_pct"] > 90.0) else "WARNING"
        remediation = "Auto-scale horizontal cluster node" if anomaly["cpu_pct"] > 85.0 else "Flush memory cache buffer"
        
        yield {
            **anomaly,
            "urgency": urgency,
            "remediation_action": remediation,
            "detected_at": "2026-08-19 14:35:00"
        }


# 3. Execution Pipeline
raw_metrics = [
    {"node_id": "srv-01", "cpu_pct": 34.5, "mem_pct": 45.0, "status": "HEALTHY"},
    {"node_id": "srv-02", "cpu_pct": 92.4, "mem_pct": 78.0, "status": "HEALTHY"}, # High CPU
    {"node_id": "srv-03", "cpu_pct": 12.0, "mem_pct": 89.5, "status": "HEALTHY"}, # High RAM
    {"node_id": "srv-04", "cpu_pct": 45.0, "mem_pct": 50.0, "status": "HEALTHY"},
    {"node_id": "srv-05", "cpu_pct": 98.0, "mem_pct": 94.0, "status": "DEGRADED"}, # Critical Fault
]

# Assemble the streaming pipeline
source_batch = TelemetrySensorBatch(raw_metrics)
stream_stage_1 = stream_raw_telemetry(source_batch)
stream_stage_2 = filter_healthy_nodes(stream_stage_1)
stream_stage_3 = enrich_anomaly_metadata(stream_stage_2)

print("=" * 80)
print(f"{'CLOUD INFRASTRUCTURE TELEMETRY STREAMING PIPELINE':^80}")
print("=" * 80)
print(f"{'Node ID':<10} | {'CPU Load':>10} | {'RAM Load':>10} | {'Urgency':^12} | {'Remediation Action':<30}")
print("-" * 80)

total_anomalies_detected = 0
for incident in stream_stage_3:
    total_anomalies_detected += 1
    print(
        f"{incident['node_id']:<10} | "
        f"{incident['cpu_pct']:>9.1f}% | "
        f"{incident['mem_pct']:>9.1f}% | "
        f"{incident['urgency']:^12} | "
        f"{incident['remediation_action']:<30}"
    )

print("-" * 80)
print(f"{'TOTAL ANOMALIES FLAGGED IN STREAM:':<40} {total_anomalies_detected} incidents")
print("=" * 80)
```

### 🔍 Code Explanation:
- **`TelemetrySensorBatch`**: Implements `__iter__` and `__next__` to demonstrate custom iterator mechanics.
- **Generator Pipelines**: `stream_raw_telemetry -> filter_healthy_nodes -> enrich_anomaly_metadata` stream records downstream on-demand without creating temporary intermediate lists.
- **Memory Optimization**: Records flow through the loop one at a time, keeping RAM consumption constant ($O(1)$) regardless of stream volume.

---

## 📝 Quick Exercise: E-Commerce Transaction Log Streaming & Fraud Filter Pipeline

### 🏢 Real-Life Scenario
You are developing the real-time transaction monitoring pipeline for an e-commerce credit processor. The system ingests a stream of raw payment transactions, filters out low-value benign transactions, detects high-risk transactions (amount $> \$5,000$ or international origin with volume $> \$1,000$), and yields formatted fraud review alerts.

### 📋 Requirements
1. **Define Generator `stream_transactions(raw_data: list[str])`**:
   - Takes a list of CSV strings: `"TXN_ID,USER_ID,AMOUNT,COUNTRY,CARD_TYPE"`.
   - Strips whitespace and yields parsed dictionary records:
     `{"txn_id": parts[0], "user_id": parts[1], "amount": float(parts[2]), "country": parts[3], "card_type": parts[4]}`.
2. **Define Generator `filter_suspicious_transactions(transaction_stream)`**:
   - Yields transactions where `amount >= 5000.0` OR (`country != "US"` and `amount >= 1000.0`).
3. **Define Generator `generate_fraud_alerts(flagged_stream)`**:
   - Yields formatted incident alert strings with risk category and audit timestamp.
4. Execute the pipeline over test data and print the streaming output.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 2 generators, `yield`, and streaming pipelines with Level 1 string splitting, casting, conditionals, and f-strings.

### 🎯 Expected Output
```text
==================================================
        REAL-TIME FRAUD STREAMING AUDITOR         
==================================================
🚨 [FLAGGED] Txn TXN-102 | User: USR-44 | $1,250.00 | Country: GB | Reason: High-Value Cross-Border
🚨 [FLAGGED] Txn TXN-104 | User: USR-91 | $8,500.00 | Country: US | Reason: Excessive Domestic Amount
--------------------------------------------------
Total Suspicious Transactions Detected: 2
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
# 1. Pipeline Generator Stages (Level 2)
def stream_transactions(raw_csv_records: list[str]):
    for record in raw_csv_records:
        line = record.strip()
        if not line:
            continue
        parts = line.split(",")
        yield {
            "txn_id": parts[0],
            "user_id": parts[1],
            "amount": float(parts[2]),
            "country": parts[3],
            "card_type": parts[4]
        }

def filter_suspicious_transactions(transaction_stream):
    for txn in transaction_stream:
        if txn["amount"] >= 5000.0 or (txn["country"] != "US" and txn["amount"] >= 1000.0):
            yield txn

def generate_fraud_alerts(flagged_stream):
    for txn in flagged_stream:
        reason = "Excessive Domestic Amount" if txn["amount"] >= 5000.0 else "High-Value Cross-Border"
        yield f"🚨 [FLAGGED] Txn {txn['txn_id']} | User: {txn['user_id']} | ${txn['amount']:,.2f} | Country: {txn['country']} | Reason: {reason}"


# 2. Execution Run
raw_feed = [
    "TXN-101,USR-12,45.00,US,VISA",
    "TXN-102,USR-44,1250.00,GB,MASTERCARD",
    "TXN-103,USR-08,120.00,US,AMEX",
    "TXN-104,USR-91,8500.00,US,VISA",
    "TXN-105,USR-19,300.00,CA,VISA",
]

# Connect generator pipeline
parsed_stream = stream_transactions(raw_feed)
filtered_stream = filter_suspicious_transactions(parsed_stream)
alert_stream = generate_fraud_alerts(filtered_stream)

print("==================================================")
print("        REAL-TIME FRAUD STREAMING AUDITOR         ")
print("==================================================")

alert_count = 0
for alert in alert_stream:
    alert_count += 1
    print(alert)

print("--------------------------------------------------")
print(f"Total Suspicious Transactions Detected: {alert_count}")
print("==================================================")
```

**Explanation of the Solution:**
- `stream_transactions` parses raw text incrementally without pre-allocating dictionary arrays.
- `filter_suspicious_transactions` filters records on-the-fly and yields suspicious records downstream.
- `generate_fraud_alerts` decorates data for human console evaluation.
</details>
