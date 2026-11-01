import json
from statistics import median
from struct import Struct
import sys
from time import perf_counter_ns
import tracemalloc

RECORD = Struct(">I")

def validate(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Expected bytes or bytearray")
    if len(data) % RECORD.size:
        raise ValueError("Partial record")

def baseline_checksum(data):
    validate(data)
    total = 0
    for offset in range(0, len(data), RECORD.size):
        total += int.from_bytes(data[offset:offset + RECORD.size], "big")
    return total

def buffer_checksum(data):
    validate(data)
    total = 0
    with memoryview(data) as view:
        for offset in range(0, len(view), RECORD.size):
            total += RECORD.unpack_from(view, offset)[0]
    return total

def median_call_ns(operation, data, trials=7, repetitions=20):
    operation(data)
    samples = []
    for _ in range(trials):
        start = perf_counter_ns()
        for _ in range(repetitions):
            operation(data)
        samples.append((perf_counter_ns() - start) / repetitions)
    return int(median(samples))

def peak_bytes(operation, data):
    if tracemalloc.is_tracing():
        raise RuntimeError("A tracing session is already active")
    tracemalloc.start()
    try:
        operation(data)
        current, peak = tracemalloc.get_traced_memory()
        return peak
    finally:
        tracemalloc.stop()

if __name__ == "__main__":
    for operation in [baseline_checksum, buffer_checksum]:
        assert operation(b"") == 0
        assert operation(RECORD.pack(120) + RECORD.pack(80)) == 200
        try:
            operation(b"x")
        except ValueError:
            pass
        else:
            raise AssertionError("Partial record was accepted")
        mutable = bytearray(RECORD.pack(12))
        before = mutable.copy()
        assert operation(mutable) == 12 and mutable == before
    records = 10000
    data = b"".join(RECORD.pack(value) for value in range(records))
    checksum = records * (records - 1) // 2
    assert baseline_checksum(data) == buffer_checksum(data) == checksum
    probe = getattr(sys, "_is_gil_enabled", None)
    report = {"implementation":sys.implementation.name,"python":sys.version.split()[0],
        "gil_enabled":probe() if probe is not None else None,
        "records":records,"checksum":checksum,
        "baseline_median_ns":median_call_ns(baseline_checksum,data),
        "buffer_median_ns":median_call_ns(buffer_checksum,data),
        "baseline_peak_bytes":peak_bytes(baseline_checksum,data),
        "buffer_peak_bytes":peak_bytes(buffer_checksum,data)}
    print(json.dumps(report, indent=2))
