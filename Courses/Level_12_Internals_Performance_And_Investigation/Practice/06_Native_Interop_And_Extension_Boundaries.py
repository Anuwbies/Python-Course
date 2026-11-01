# Independent task: native interop & extension boundaries
#
# Load the platform system C library with ctypes.CDLL (msvcrt on Windows, find_library("c")
# elsewhere). Bind abs with c_int argument/result. Implement native_abs(value), requiring a
# plain integer within the representable symmetric signed c_int range, rejecting invalid values
# with ValueError before the native call. Print native_abs(-12), then Rejected for an
# out-of-range integer. Do not load arbitrary user-provided libraries.
#
# Expected output:
#
# 12
# Rejected

