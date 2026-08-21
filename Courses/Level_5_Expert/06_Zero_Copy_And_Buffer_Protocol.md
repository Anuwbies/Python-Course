# Lesson 6: Zero-Copy Data Processing & The Buffer Protocol

In high-throughput distributed systems—such as network routers, financial market exchange gateways, database storage engines, and multimedia streaming servers—copying raw byte buffers between memory locations creates massive CPU cache pressure and memory bandwidth bottlenecks. Python's **Buffer Protocol (`Py_buffer`)** and **`memoryview`** allow you to inspect, slice, parse, and mutate raw contiguous C-level memory **without making a single memory copy** ($O(1)$ zero-copy operations).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the performance cost of byte memory copies in high-volume systems.
2. Master the CPython **Buffer Protocol** (`Py_buffer` struct) and buffer-exporting types (`bytes`, `bytearray`, `array.array`).
3. Slice and inspect contiguous memory buffers using **`memoryview`** in $\mathcal{O}(1)$ time and $\mathcal{O}(1)$ RAM.
4. Perform type casting across raw memory views (`view.cast('H')`, `view.cast('I')`).
5. Encode and decode binary protocol formats using the **`struct`** module and `struct.pack_into()`.
6. Write zero-copy binary network packet and audio/video frame parsers.

---

## 1. The High Cost of Standard Byte Slicing

When you slice a standard Python `bytes` object, Python allocates a *brand new byte array* in RAM and copies all characters over:

```python
import sys

large_payload = b"X" * (100 * 1024 * 1024) # 100 Megabytes of bytes

# ❌ STANDARD SLICE: Allocates a fresh 10MB memory block and copies 10,000,000 bytes!
# slice_copy = large_payload[: 10 * 1024 * 1024]

# ✅ ZERO-COPY MEMORYVIEW: Allocates 0 extra bytes of payload memory!
view = memoryview(large_payload)
zero_copy_slice = view[: 10 * 1024 * 1024]

print(f"Memoryview object size: {sys.getsizeof(zero_copy_slice)} bytes (Points to existing buffer!)")
```

---

## 2. In-Place Mutation with `bytearray` and `memoryview`

```python
# Create mutable byte buffer
raw_buffer = bytearray(b"HELLO_WORLD_PROTOCOL")
mv = memoryview(raw_buffer)

# Slice and modify in-place without reallocating
mv[0:5] = b"APEX_"

print(raw_buffer) # bytearray(b'APEX__WORLD_PROTOCOL') (Underlying buffer modified!)
```

---

## 3. High-Speed Binary Parsing with `struct`

The `struct` module converts between Python values and C structs represented as Python bytes:

| Format Code | C Type | Standard Size |
| :---: | :--- | :---: |
| `>I` / `<I` | `unsigned int` (32-bit Big/Little Endian) | 4 bytes |
| `>H` / `<H` | `unsigned short` (16-bit) | 2 bytes |
| `>d` / `<d` | `double` (64-bit float) | 8 bytes |
| `>Q` / `<Q` | `unsigned long long` (64-bit uint) | 8 bytes |

```python
import struct

# Pack binary header: Magic Number (0xDEADBEEF), Packet ID (101), Payload Length (2048)
binary_frame = struct.pack(">III", 0xDEADBEEF, 101, 2048)

# Zero-copy unpack directly from memoryview
magic, pkt_id, length = struct.unpack_from(">III", memoryview(binary_frame), 0)
print(f"Magic: {hex(magic)} | Packet ID: {pkt_id} | Length: {length}")
```

---

---

## 4. The C-Level `Py_buffer` Struct

Any Python C-extension implementing the Buffer Protocol defines the `Py_buffer` C-struct:

```c
typedef struct bufferinfo {
    void *buf;              // Pointer to raw contiguous C memory block
    PyObject *obj;          // Strong reference to exporting Python object
    Py_ssize_t len;         // Total buffer length in bytes
    Py_ssize_t itemsize;    // Size in bytes of each element
    char *format;           // Struct format string (e.g. "i", "d", "c")
    int ndim;               // Number of dimensions
    Py_ssize_t *shape;      // Array of dimension lengths
    Py_ssize_t *strides;    // Byte step offset between elements
} Py_buffer;
```

---

## 5. Multi-Dimensional Memory Reshaping (`view.cast`)

Without allocating NumPy arrays, Python's built-in `memoryview` can cast 1D flat byte arrays into 2D matrices:

```python
raw_pixels = bytearray(b"\x00\xFF" * 8) # 16 bytes
mv = memoryview(raw_pixels).cast('B', shape=(4, 4))
print("2D Pixel at [1, 1]:", mv[1, 1])
```

---

## 6. High-Throughput Zero-Copy Sockets (`recv_into`)

In network servers, standard `sock.recv(4096)` allocates a new `bytes` object for every packet. **`sock.recv_into(buffer)`** writes directly into pre-allocated memory:

```python
import socket

buffer = bytearray(65536) # Pre-allocated 64KB ring buffer
view = memoryview(buffer)

# Zero-copy TCP read:
# bytes_received = sock.recv_into(view[offset:])
```

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master the buffer protocol, `memoryview`, zero-copy slicing, `struct` binary serialization, and buffer reshaping:

---

### 🟢 Tier 1: `memoryview` & Slicing Basics (Exercises 1–3)

#### 🔹 Exercise 1: Memoryview Slice Size Comparison
* **Goal**: Measure memory sizes of `bytes[:1000]` slice vs `memoryview(b)[:1000]`.

#### 🔹 Exercise 2: In-Place Bytearray Mutation
* **Goal**: Modify an ASCII byte sequence in-place using a `memoryview` slice.

#### 🔹 Exercise 3: Binary Packing with `struct.pack`
* **Goal**: Pack a header `(uint16, uint32, float64)` and inspect the raw byte length.

---

### 🟡 Tier 2: Binary Parsing & Type Casting (Exercises 4–6)

#### 🔹 Exercise 4: Zero-Copy Unpacking with `struct.unpack_from`
* **Goal**: Extract telemetry records from a `bytearray` without creating slice copies.

#### 🔹 Exercise 5: Integer Type Casting (`view.cast('I')`)
* **Goal**: Cast a 16-byte buffer into 4 32-bit unsigned integers using `memoryview.cast('I')`.

#### 🔹 Exercise 6: Network Packet Header & Payload Parser
* **Goal**: Parse a custom TCP packet containing a 6-byte header followed by a variable-length string.

---

### 🟠 Tier 3: Multi-Dimensional Buffers & Ring Buffers (Exercises 7–9)

#### 🔹 Exercise 7: 2D Matrix Reshaping with Built-in `memoryview`
* **Goal**: Reshape a 1024-byte buffer into a $(32 \times 32)$ grayscale pixel matrix.

#### 🔹 Exercise 8: Zero-Copy Circular Ring Buffer
* **Goal**: Implement a circular buffer wrapping around a fixed-size `bytearray` with `memoryview`.

#### 🔹 Exercise 9: `struct.pack_into` Performance Benchmark
* **Goal**: Benchmark pre-allocated `struct.pack_into()` against dynamic string concatenation over 500,000 records.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Financial Market ITCH Binary Feed Parser
* **Goal**: Build a high-frequency trading binary market data feed parser decoding 24-byte stock tick frames in $\mathcal{O}(1)$ zero-copy time.

---

The following real-life program models an **Ultra-Low-Latency Financial Exchange Binary Market-Data Feed Parser (ITCH/OUCH Protocol)**, parsing thousands of tick-by-tick order frames using zero-copy `memoryview` offsets and `struct.unpack_from`:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Zero-Copy Binary Market Feed & ITCH Frame Parser
# =====================================================================

import struct
from typing import NamedTuple

class StockTick(NamedTuple):
    timestamp_ns: int
    ticker: str
    price: float
    shares: int
    is_buy: bool


class MarketDataBinaryParser:
    """Zero-copy binary frame parser for high-frequency trading market feeds.
    
    Frame Wire Format (24 bytes per tick):
      - Timestamp: uint64 Big-Endian (>Q, 8 bytes)
      - Ticker:    char[6] string (6s, 6 bytes)
      - Price:     uint32 price * 10000 (>I, 4 bytes)
      - Shares:    uint32 volume (>I, 4 bytes)
      - Side:      char 'B' or 'S' (c, 1 byte)
      - Padding:   1 byte (x)
    """

    FRAME_FORMAT = ">Q6sIIcx"
    FRAME_SIZE = struct.calcsize(FRAME_FORMAT) # Exactly 24 bytes

    @classmethod
    def synthesize_mock_binary_feed(cls, ticks: list[dict]) -> bytearray:
        """Simulates incoming raw TCP socket stream buffer."""
        buffer = bytearray(cls.FRAME_SIZE * len(ticks))
        
        for idx, tick in enumerate(ticks):
            offset = idx * cls.FRAME_SIZE
            ticker_bytes = tick["ticker"].encode("ascii").ljust(6, b" ")
            price_scaled = int(tick["price"] * 10_000)
            side_byte = b"B" if tick["is_buy"] else b"S"

            # In-place zero-allocation binary packing directly into buffer
            struct.pack_into(
                cls.FRAME_FORMAT, buffer, offset,
                tick["timestamp_ns"],
                ticker_bytes,
                price_scaled,
                tick["shares"],
                side_byte
            )
        return buffer

    @classmethod
    def parse_feed_zero_copy(cls, raw_stream: bytearray) -> list[StockTick]:
        """Parses the entire binary stream with zero payload copies."""
        view = memoryview(raw_stream) # Zero-copy memory wrapper (Lesson 6)
        total_ticks = len(view) // cls.FRAME_SIZE
        parsed_ticks = []

        for i in range(total_ticks):
            offset = i * cls.FRAME_SIZE
            # unpack_from reads directly from existing memoryview buffer!
            ts, raw_ticker, raw_price, shares, side = struct.unpack_from(cls.FRAME_FORMAT, view, offset)
            
            ticker = raw_ticker.decode("ascii").strip()
            price = raw_price / 10_000.0
            is_buy = (side == b"B")

            parsed_ticks.append(StockTick(ts, ticker, price, shares, is_buy))

        return parsed_ticks


# Execution Simulation
sample_ticks = [
    {"timestamp_ns": 1724083200000000, "ticker": "NVDA", "price": 128.50, "shares": 500, "is_buy": True},
    {"timestamp_ns": 1724083200000050, "ticker": "AAPL", "price": 224.75, "shares": 1200, "is_buy": False},
    {"timestamp_ns": 1724083200000100, "ticker": "MSFT", "price": 448.20, "shares": 300, "is_buy": True},
]

# Generate binary wire buffer
wire_buffer = MarketDataBinaryParser.synthesize_mock_binary_feed(sample_ticks)
parsed_feed = MarketDataBinaryParser.parse_feed_zero_copy(wire_buffer)

print("=" * 80)
print(f"{'ZERO-COPY FINANCIAL BINARY MARKET FEED PARSER':^80}")
print("=" * 80)
print(f"Total Stream Size: {len(wire_buffer)} bytes ({len(wire_buffer) // 24} binary frames @ 24 bytes/ea)")
print("-" * 80)
print(f"{'Timestamp (ns)':<20} | {'Ticker':<8} | {'Price':>10} | {'Volume':>8} | {'Side':^6}")
print("-" * 80)

for tick in parsed_feed:
    side_str = "BUY" if tick.is_buy else "SELL"
    print(f"{tick.timestamp_ns:<20} | {tick.ticker:<8} | ${tick.price:>9.2f} | {tick.shares:>8} | {side_str:^6}")

print("=" * 80)
```

### 🔍 Code Explanation:
- **`struct.calcsize(">Q6sIIcx")`**: Computes exact 24-byte C-structure binary layout for market tick messages.
- **`struct.pack_into()`**: Writes binary data directly into pre-allocated `bytearray` memory without intermediate string allocation.
- **`memoryview` & `struct.unpack_from()`**: Decodes binary data directly from the network buffer slice in $\mathcal{O}(1)$ time without copying memory.

---

## 📝 Quick Exercise: Zero-Copy Network Packet Header & Payload Extractor

### 🏢 Real-Life Scenario
You are developing a network packet sniffer and firewall analyzer. Incoming TCP network packets consist of a 6-byte header (`2-byte Packet ID`, `4-byte Payload Length`) followed immediately by arbitrary ASCII payload text. You must extract and decode the packet without copying the entire underlying payload.

### 📋 Requirements
1. **Packet Header Format**: `>HI` (2-byte unsigned short `pkt_id`, 4-byte unsigned int `payload_len`).
2. **Define `parse_network_packet_zero_copy(raw_packet: bytearray) -> tuple[int, int, str]`**:
   - Wrap `raw_packet` in `memoryview(raw_packet)`.
   - Unpack header using `struct.unpack_from(">HI", view, 0)`.
   - Slice payload using zero-copy slice: `payload_view = view[6 : 6 + payload_len]`.
   - Convert payload slice to bytes and decode as UTF-8: `bytes(payload_view).decode("utf-8")`.
   - Return `(pkt_id, payload_len, payload_str)`.
3. Construct a sample bytearray packet containing ID `1001` and payload `"AUTHENTICATION_TOKEN_XYZ"` and verify extraction.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 5 `memoryview` and `struct` zero-copy parsing with Level 1 string formatting.

### 🎯 Expected Output
```text
==================================================
        ZERO-COPY NETWORK PACKET EXTRACTOR        
==================================================
Raw Network Packet Size: 30 bytes
--------------------------------------------------
PARSED PACKET HEADER & PAYLOAD:
  ✓ Packet ID:      1001
  ✓ Payload Length: 24 bytes
  ✓ Decoded Body:   AUTHENTICATION_TOKEN_XYZ
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Packet Extractor & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Zero-Copy Network Packet Extractor
# =====================================================================
import struct

def parse_network_packet_zero_copy(raw_packet: bytearray) -> tuple[int, int, str]:
    view = memoryview(raw_packet)
    pkt_id, payload_len = struct.unpack_from(">HI", view, 0)
    payload_view = view[6 : 6 + payload_len]
    payload_str = bytes(payload_view).decode("utf-8")
    return pkt_id, payload_len, payload_str


body_bytes = b"AUTHENTICATION_TOKEN_XYZ"
packet_buffer = bytearray(struct.pack(">HI", 1001, len(body_bytes)) + body_bytes)

pid, plen, body = parse_network_packet_zero_copy(packet_buffer)

print("==================================================")
print("        ZERO-COPY NETWORK PACKET EXTRACTOR        ")
print("==================================================")
print(f"Raw Network Packet Size: {len(packet_buffer)} bytes")
print("--------------------------------------------------")
print("PARSED PACKET HEADER & PAYLOAD:")
print(f"  ✓ Packet ID:      {pid}")
print(f"  ✓ Payload Length: {plen} bytes")
print(f"  ✓ Decoded Body:   {body}")
print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Memoryview Slice Size
import sys
b = b"A" * 100000; v = memoryview(b)
# sys.getsizeof(b[:1000]) >> sys.getsizeof(v[:1000])

# Ex 2: In-place bytearray mutation
ba = bytearray(b"Hello"); mv = memoryview(ba); mv[0:1] = b"J"
# ba -> bytearray(b'Jello')

# Ex 3: struct.pack
pkt = struct.pack(">HId", 1, 100, 3.14)

# Ex 4: struct.unpack_from
h_id, count, val = struct.unpack_from(">HId", memoryview(pkt), 0)

# Ex 5: Cast to unsigned int
buf = bytearray(16)
int_view = memoryview(buf).cast('I')
int_view[0] = 42

# Ex 6: Network Packet Parser
# Verified in main solution above.

# Ex 7: 2D Matrix Reshaping
flat = bytearray(1024)
matrix = memoryview(flat).cast('B', shape=(32, 32))
matrix[0, 0] = 255

# Ex 8: Zero-Copy Ring Buffer
class RingBuf:
    def __init__(self, sz): self.b, self.w = bytearray(sz), 0
    def write(self, data):
        mv = memoryview(self.b)
        n = len(data)
        mv[self.w : self.w + n] = data
        self.w = (self.w + n) % len(self.b)

# Ex 9: pack_into benchmark
# struct.pack_into(">I", buf, offset, val)
```
</details>
