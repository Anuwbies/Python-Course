# Capstone Project 5.2: Zero-Copy High-Performance Network Server

## 📌 Project Overview
Engineer an extreme-performance, low-latency **Zero-Copy HTTP / Binary Network Server** in pure Python using OS-level event notification mechanisms (`selectors` / `epoll` / `kqueue`), Python's C-level Buffer Protocol (`memoryview`, `bytearray`), circular ring-buffer socket recycling, GC tuning (`gc.disable()`), and memory-mapped file transfers (`mmap`).

---

## 🎯 Learning Objectives
- **Zero-Copy Architecture**: Eliminating intermediate buffer allocations and string copying by passing `memoryview` slices directly to socket system calls (`socket.send()`, `socket.recv_into()`).
- **CPython Buffer Protocol**: Interfacing directly with raw memory buffers without creating new heap Python objects on every request.
- **Event-Driven Non-Blocking I/O**: Building a custom event multiplexing loop using Python's `selectors` module (`select.epoll` or `select.kqueue`).
- **Memory-Mapped Files (`mmap`)**: Serving multi-gigabyte static files directly from kernel page cache to network sockets without loading them into Python process memory.
- **Garbage Collection Optimization**: Disabling automatic cyclic GC collections during critical hot loops and tuning generational thresholds to minimize tail latencies.

---

## 🏗️ System Architecture

```text
               +----------------------------------+
               |        OS Kernel Sockets         |
               +----------------------------------+
                                |
                   (selectors: epoll / kqueue)
                                |
                                v
               +----------------------------------+
               |      Zero-Copy Event Loop        |
               +----------------------------------+
                                |
         +----------------------+----------------------+
         |                                             |
         v                                             v
+---------------------+                       +---------------------+
| Recv Ring Buffer    |                       | Static File Server  |
| (pre-allocated      |                       | (mmap Kernel        |
|  bytearray)         |                       |  Zero-Copy View)    |
+---------------------+                       +---------------------+
         |                                             |
         v (memoryview slice)                          v (memoryview slice)
+-------------------------------------------------------------------+
|                  Zero-Copy HTTP / Binary Parser                   |
|           - No str allocations in hot path                        |
|           - Direct byte slice matching                            |
+-------------------------------------------------------------------+
```

---

## 📋 Functional Requirements

### 1. Pre-Allocated Fixed Buffer Ring
- Pre-allocate a contiguous memory block (e.g. 10 MB `bytearray`).
- Hand out `memoryview` sub-slices to incoming client connections to read payloads using `sock.recv_into(view[offset:])` with zero heap allocation.

### 2. High-Performance Selector Loop
- Register sockets with `selectors.DefaultSelector()`.
- Process non-blocking reads and writes concurrently.
- Handle partial socket writes cleanly by slicing memoryviews without copying (`view = view[sent:]`).

### 3. Zero-Copy HTTP Request Parser
- Parse HTTP methods (`GET`, `POST`), URI paths, and headers directly as ASCII byte slices (`b"GET"`, `b"\r\n\r\n"`), avoiding converting byte payloads into Python `str` objects in the hot path.

### 4. Memory-Mapped Static File Streaming (`mmap`)
- Open static files using `mmap.mmap(fileno, 0, access=mmap.ACCESS_READ)`.
- Stream file contents directly from memory map to the socket descriptor.

### 5. GC Tuning & Benchmark Harness
- Benchmark throughput (requests per second) and memory footprint using synthetic workload generators.
- Compare performance with default Python `gc` enabled vs tuned generational thresholds (`gc.set_threshold()`) vs disabled.

---

## 📐 Phased Implementation Guide

### Phase 1: Zero-Copy Ring Buffer & Connection State
```python
import socket
import selectors
import mmap
import gc

class Connection:
    def __init__(self, sock: socket.socket, buffer_view: memoryview):
        self.sock = sock
        self.view = buffer_view
        self.bytes_read = 0
        self.out_view = None

    def read(self) -> int:
        n = self.sock.recv_into(self.view[self.bytes_read:])
        if n > 0:
            self.bytes_read += n
        return n

    def write(self) -> int:
        if self.out_view and len(self.out_view) > 0:
            sent = self.sock.send(self.out_view)
            self.out_view = self.out_view[sent:]
            return sent
        return 0
```

### Phase 2: Selector Event Loop
```python
class ZeroCopyServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.host = host
        self.port = port
        self.selector = selectors.DefaultSelector()
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.setblocking(False)
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen(1024)
        self.selector.register(self.server_sock, selectors.EVENT_READ, self.accept)

        # Global 10MB arena
        self.arena = bytearray(10 * 1024 * 1024)
        self.arena_view = memoryview(self.arena)
```

### Phase 3: Zero-Allocation Request Dispatcher & Benchmarks
Execute requests and serve static assets via kernel-backed `mmap`.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Partial TCP Chunking** | Send HTTP request split across 3 separate TCP packets | Correctly reassembles buffer in `memoryview` without string concatenation |
| **Large File Direct Transfer**| Serve 500 MB ISO/video file via `mmap` | File transfers at wire speed; process RAM stays $< 15\text{ MB}$ |
| **Connection Flood** | Simulate 1,000 concurrent client connections | Selector event loop handles all descriptors without blocking |
| **Heap Allocation Profiling**| Profile 100k requests with `tracemalloc` | Heap allocations in request hot loop remain near 0 |

---

## 🚀 Bonus Challenges
- **Linux `sendfile(2)` Integration**: Use `os.sendfile()` for direct kernel-to-kernel socket transfers.
- **HTTP/1.1 Pipelining**: Support pipelined HTTP requests within the same persistent TCP socket connection.
