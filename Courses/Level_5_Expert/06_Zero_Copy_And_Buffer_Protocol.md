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

## 💻 Code Example & Reference

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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import struct

# 1. Zero-Copy Packet Parser (Level 5)
def parse_network_packet_zero_copy(raw_packet: bytearray) -> tuple[int, int, str]:
    view = memoryview(raw_packet) # O(1) buffer view
    pkt_id, payload_len = struct.unpack_from(">HI", view, 0)
    
    # Zero-copy slice of payload section
    payload_view = view[6 : 6 + payload_len]
    payload_str = bytes(payload_view).decode("utf-8")

    return pkt_id, payload_len, payload_str


# 2. Execution Simulation
# Construct mock packet: Header (6 bytes) + Body
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
```

**Explanation of the Solution:**
- `struct.unpack_from(">HI", view, 0)` inspects the first 6 bytes of the buffer without splitting or copying the byte stream.
- Slicing `view[6: 6 + payload_len]` produces a lightweight `memoryview` slice referencing existing RAM.
</details>
