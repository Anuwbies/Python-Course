# Capstone Project 2.3: Memory-Efficient Server Log ETL Analyzer

## 📌 Project Overview
Build a high-performance **Server Log ETL (Extract, Transform, Load) Pipeline & Anomaly Detector** capable of streaming multi-gigabyte access logs (such as Nginx/Apache Combined Log Format) in constant $O(1)$ memory, extracting structured event metrics, filtering malicious bot activity/brute-force attacks, and generating visual analytics dashboards.

---

## 🎯 Learning Objectives
- **Generator Pipelines**: Chaining multiple single-purpose generator functions (`yield`) to build a streaming ETL workflow.
- **Custom Iterator Class**: Implementing `__iter__` and `__next__` on custom streaming classes with rewind/reset capability.
- **Decorator-Driven Metrics**: Writing decorators to measure throughput (lines processed per second) and memory allocations (`tracemalloc`).
- **Custom Exception Classes**: Handling corrupted log lines, malformed IP addresses, and parsing timeouts.
- **Pytest Suite**: Testing stream processing with mock generators and parameterized log entries.

---

## 🏗️ System Architecture

```text
[ Multi-GB Raw Log File ]
            |
            v  (Line-by-line file reader stream)
   [ LogReader Iterator ]
            |
            v  (Regex extraction & timestamp parsing)
   [ LogParser Generator ]
            |
            v  (Data cleaning & GeoIP/Status mapping)
   [ Transformer Generator ]
            |
            +------------------------+------------------------+
            |                                                 |
            v                                                 v
  [ Anomaly Detector ]                             [ Aggregator & Exporter ]
  - Brute Force (>20 401s)                         - Top 10 IP addresses
  - Path Traversals (../)                          - Status code breakdown
  - Error Rate Spikes                              - Export JSON/Markdown
```

---

## 📋 Functional Requirements

### 1. Nginx/Apache Log Regex Specification
Parse standard Combined Log Format lines:
```text
192.168.1.105 - - [18/Aug/2026:14:32:10 +0000] "GET /api/v1/users HTTP/1.1" 200 4512 "-" "Mozilla/5.0"
```
Extracted fields:
- `ip_address`: str
- `timestamp`: datetime
- `http_method`: str (`GET`, `POST`, `PUT`, `DELETE`, etc.)
- `endpoint`: str
- `status_code`: int (e.g. `200`, `401`, `404`, `500`)
- `bytes_sent`: int
- `user_agent`: str

### 2. Streaming Generator Pipeline Architecture
Data must flow lazily without loading the whole file into RAM:
```python
def read_log_lines(filepath: str) -> Generator[str, None, None]: ...
def parse_log_entries(lines: Generator[str, None, None]) -> Generator[LogRecord, None, None]: ...
def filter_by_status(records: Generator[LogRecord, None, None], min_status: int) -> Generator[LogRecord, None, None]: ...
def detect_brute_force_ips(records: Generator[LogRecord, None, None], threshold: int = 10) -> Generator[SecurityAlert, None, None]: ...
```

### 3. Anomaly Detection Engine
- **Brute Force Detection**: Flags IP addresses triggering $\ge 15$ HTTP `401 Unauthorized` or `403 Forbidden` responses within a 60-second window.
- **Path Traversal / SQL Injection Probe**: Flags requests containing patterns such as `../`, `etc/passwd`, `' OR 1=1`, `<script>`.
- **404 Spiders**: Identifies crawlers generating excessive `404 Not Found` errors across non-existent admin endpoints.

### 4. Custom Memory & Throughput Decorator
```python
@benchmark_stream(log_frequency=10000)
def process_pipeline(filepath: str):
    # Logs lines/second and current RAM usage via tracemalloc
```

---

## 📐 Phased Implementation Guide

### Phase 1: Structured LogRecord & Exceptions
```python
from dataclasses import dataclass
from datetime import datetime

class LogParsingError(Exception):
    def __init__(self, line_num: int, raw_line: str, reason: str):
        super().__init__(f"Line {line_num} parse error: {reason}")
        self.line_num = line_num
        self.raw_line = raw_line

@dataclass(frozen=True)
class LogRecord:
    ip_address: str
    timestamp: datetime
    method: str
    endpoint: str
    status_code: int
    bytes_sent: int
    user_agent: str
```

### Phase 2: Pipeline Generators
Implement generator stages that yield transformed records and yield security alert objects.

### Phase 3: Analytics Aggregator
Aggregate overall throughput, bandwidth consumption, top visited URLs, and security threats.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Malformed Log Line** | Log entry missing timestamp or HTTP method | Raises `LogParsingError` or yields to error sink without terminating stream |
| **Large File Simulation** | Stream a 1,000,000 line synthetic file | Memory consumption stays constant ($< 25\text{ MB}$ RAM) |
| **Rapid Brute Force** | 20 failed login attempts in 5 seconds from `10.0.0.1` | Successfully yields `SecurityAlert(type="BRUTE_FORCE", ip="10.0.0.1")` |
| **Corrupted Byte Stream**| File containing invalid UTF-8 byte sequences | Handles decoding gracefully with error replacement |

---

## 🚀 Bonus Challenges
- **Real-Time Tail (`tail -f`)**: Implement an active file follower generator that yields new lines in real-time as they are written by web servers.
- **Terminal UI**: Display live streaming progress bars and metrics in terminal using ANSI escape codes.
