# Independent task: Measured binary-parser optimization study
#
# Implement baseline_checksum(data) using byte slices and int.from_bytes, and
# buffer_checksum(data) using a released memoryview and Struct(">I").unpack_from without input
# slices. Both require bytes/bytearray and a length divisible by four.
#
# Establish known answers for empty input and packed 120/80, partial-record rejection for both
# variants, and unchanged bytearray input. Build 10000 records containing integers 0..9999
# outside the measurement windows; independently derive the expected checksum as n*(n-1)//2.
#
# Warm each variant, collect seven timing trials of twenty calls using perf_counter_ns, and
# report median per-call nanoseconds. Separately measure peak traced allocation for one call of
# each variant with input already resident. Own and stop each tracemalloc session; reject an
# already active tracing session in the helper.
#
# Print a JSON report with implementation, Python version, active GIL state when available,
# records, checksum, both observed median durations, and both observed traced peaks. Expected
# fixed values are records=10000 and checksum=49995000. Timing/memory/build fields vary. Do not
# impose or hardcode a speedup.

