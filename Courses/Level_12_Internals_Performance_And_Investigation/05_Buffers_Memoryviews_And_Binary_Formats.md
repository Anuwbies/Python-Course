# Lesson 5: Buffers, Memoryviews & Binary Formats

**Prerequisites:** Levels 1–9 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Buffers_Memoryviews_And_Binary_Formats.py`.

Interpret binary data with an explicit layout while avoiding unnecessary input copies. A shared view changes ownership and mutation considerations even when it improves one allocation pattern.

## 1. Define the byte layout

A binary format must state field width, byte order, signedness, and record boundaries. `struct.Struct(">I")` describes a big-endian unsigned four-byte integer. Native layout choices can include platform-dependent alignment and are unsuitable when a portable wire format is intended.

```python
from struct import Struct

record = Struct(">I")
data = record.pack(120)
print(record.unpack(data)[0])
```

The unpack result is a tuple of decoded fields. A buffer with the wrong length should be rejected under the format contract; silently ignoring trailing bytes would accept a corrupted record sequence.

## 2. Share a buffer without copying its contents

A memoryview exposes compatible buffer data. Slicing a view can create another view, whereas slicing a bytes object normally creates another bytes value. Calling tobytes deliberately materializes a copy and changes the allocation claim.

Bytes is immutable; bytearray is mutable. A view of a bytearray can observe writes to that buffer. While exported views are active, resizing the underlying bytearray can raise BufferError. Release views when their lifetime ends rather than retaining them accidentally in caches or closures.

## 3. Parse by offset

Struct.unpack_from reads at an offset from an existing buffer. It can avoid constructing an input slice per record, but still creates decoded Python objects. Do not call the whole pipeline zero-allocation merely because the raw input was not copied.

Use a view's appropriate shape and byte-size information when accepting arbitrary buffers. The task deliberately accepts only bytes or bytearray, giving it a one-dimensional byte-oriented contract. More general formats require checks for contiguity, element size, and layout.

## 4. Keep ownership and concurrency explicit

A shared mutable buffer can change between reads. Validate who may mutate it while a parser runs, especially in free-threaded or native code. A readonly view prevents writes through that view but does not necessarily make an independently mutable owner immutable.

A parser returning a view also extends the owner's effective lifetime. A parser returning integers can release its view before returning. Choose based on the caller's needs and account for retained memory as well as temporary allocations.

## 5. Measure the actual tradeoff

Avoiding small slices might reduce allocation churn yet perform similarly or slower for a particular interpreter and workload. Validate identical decoded values before timing. Keep input creation outside a parse-only measurement and explain that scope.

The capstone compares a slice-based checksum with a buffer-based checksum and reports real timing and traced memory. Neither implementation is named fast because the result depends on measured conditions.

## Construct bytes and read fields without struct

A bytes literal such as `b""` is an empty immutable byte sequence. `bytearray(8)` allocates eight zero bytes in a mutable buffer. Bytes and bytearray support indexing, slicing, and len; a slice `data[offset:offset + 4]` is a separate byte sequence for that record. `int.from_bytes(record_bytes, "big")` interprets it as an unsigned big-endian integer by default. That provides an independent slice-based baseline for the capstone.

`Struct.size` reports the required byte width. `record.pack(value)` returns newly packed bytes; `record.pack_into(buffer, offset, value)` writes into an existing writable buffer. `record.unpack_from(buffer, offset)` reads a tuple at an offset. The offset is in bytes, and the existing buffer must have enough space. For example, after `record = Struct(">I")`, `record.pack_into(bytearray_buffer, 0, 200)` replaces its first four-byte record.

`with memoryview(data) as view:` releases that exported view on exit. It does not close or delete the original buffer. To build a bounded input outside a measurement window, `b"".join(record.pack(value) for value in range(count))` concatenates packed byte values. This is the byte-sequence counterpart of string join, not text encoding. Keep byte order and record-width validation identical in baseline and buffer parsers.

References: [Struct](https://docs.python.org/3.13/library/struct.html), [Memoryview](https://docs.python.org/3.13/library/stdtypes.html#memory-views).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict what changes when the underlying bytearray is modified.
2. **Explain:** Explain why unpack_from can avoid an input slice but still allocate result objects.
3. **Modify:** Reject a trailing partial record before parsing.
4. **Debug:** Find a hidden tobytes call contradicting a no-input-copy claim.

<details>
<summary>Hints</summary>

Validate the complete record boundary and keep the view lifetime inside the function.

</details>

## Independent task: buffers, memoryviews & binary formats

In `Practice/05_Buffers_Memoryviews_And_Binary_Formats.py`, complete this task:

Define decode_u32s(data) accepting bytes or bytearray with length divisible by 4, raising TypeError for another input type and ValueError for a partial record. Use a released memoryview and Struct(">I").unpack_from without bytes slices or tobytes. Demonstrate a bytearray packed with 120 and 80, print decoded values, change the first record to 200 with pack_into, and print decoded values again.

Expected output:

```text
[120, 80]
[200, 80]
```
