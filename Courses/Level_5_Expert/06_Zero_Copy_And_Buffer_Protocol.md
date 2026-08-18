# Lesson 6: Zero-Copy Data Handling: memoryview & Buffer Protocol

When handling gigabytes of binary data (video streaming, high-frequency network packets, cryptography), copying byte arrays in memory wastes gigabytes of RAM and CPU cycles. The **Python Buffer Protocol** and `memoryview` enable true zero-copy slicing.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand the C-level Python Buffer Protocol.
2. Slice large binary datasets without memory duplication using `memoryview`.
3. Mutate underlying memory in-place with `bytearray`.
4. Perform zero-copy socket reads and file writes.

---

## 1. Zero-Copy Slicing with `memoryview`

```python
import sys

# 1. Standard bytes slicing: DUPLICATES memory on every slice!
large_bytes = b"X" * (50 * 1024 * 1024) # 50 MB byte string
slice_copy = large_bytes[100:100_000]    # Allocates a new byte object in RAM

# 2. memoryview: Creates a lightweight pointer view without copying bytes!
mv = memoryview(large_bytes)
zero_copy_slice = mv[100:100_000] # Allocates ONLY ~200 bytes for the view struct!

print(f"Underlying buffer size: {len(zero_copy_slice)} bytes")
print(f"Memoryview object size: {sys.getsizeof(zero_copy_slice)} bytes")
```

---

## 2. In-Place Binary Modification

```python
# Mutable buffer
data = bytearray(b"Hello World")
mv = memoryview(data)

# Modify byte at index 6 directly in the original buffer:
mv[6:11] = b"Python"

print(data) # bytearray(b'Hello Python') - Modified in-place!
```

---

## 📝 Quick Exercise

**Prompt**:
Create a binary protocol header parser that extracts a 4-byte message ID and 4-byte payload size from an incoming byte stream using `memoryview` and `struct.unpack_from` without allocating new substrings.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import struct

# Simulated binary packet: [4-byte ID: 1001] [4-byte length: 256] [payload...]
raw_packet = bytearray(struct.pack(">II", 1001, 256) + b"A" * 256)
mv = memoryview(raw_packet)

# Unpack directly from the memoryview buffer with zero intermediate string allocation
msg_id, payload_len = struct.unpack_from(">II", mv, offset=0)
payload_view = mv[8 : 8 + payload_len]

print(f"Parsed Header -> Message ID: {msg_id}, Payload Length: {payload_len} bytes")
print(f"Payload view length: {len(payload_view)} bytes (zero-copy)")
```
</details>
