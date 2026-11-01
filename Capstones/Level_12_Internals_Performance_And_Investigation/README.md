# Level 12 capstone: Measured binary-parser optimization study

**Prerequisites:** [all lessons in Level 12](../../Courses/Level_12_Internals_Performance_And_Investigation/README.md). **Submission:** `Practice/project.py`.

Investigate one bounded optimization with a reproducible dataset and equivalent contracts. Compare a baseline that slices each four-byte record with a buffer-oriented parser using Struct.unpack_from. Avoid assuming the buffer version must be faster; the outcome is an observation to explain.

The binary format is a sequence of big-endian unsigned four-byte integers. Both variants accept bytes or bytearray, reject a partial record, preserve input, and return an integer checksum. Input construction is excluded from parse-only timings and traced peaks, and all timing and memory values are collected rather than invented.

Run the reference script to produce a JSON experiment report. The report includes interpreter/build details, data size, checksum, median timing, and traced peaks for both variants. A conventional GIL-enabled run does not establish free-threaded scaling; native or concurrent variants can be a later independently justified extension.

## Project task

Implement baseline_checksum(data) using byte slices and int.from_bytes, and buffer_checksum(data) using a released memoryview and Struct(">I").unpack_from without input slices. Both require bytes/bytearray and a length divisible by four.

Establish known answers for empty input and packed 120/80, partial-record rejection for both variants, and unchanged bytearray input. Build 10000 records containing integers 0..9999 outside the measurement windows; independently derive the expected checksum as n*(n-1)//2.

Warm each variant, collect seven timing trials of twenty calls using perf_counter_ns, and report median per-call nanoseconds. Separately measure peak traced allocation for one call of each variant with input already resident. Own and stop each tracemalloc session; reject an already active tracing session in the helper.

Print a JSON report with implementation, Python version, active GIL state when available, records, checksum, both observed median durations, and both observed traced peaks. Expected fixed values are records=10000 and checksum=49995000. Timing/memory/build fields vary. Do not impose or hardcode a speedup.
