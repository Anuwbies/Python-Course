# Independent task: buffers, memoryviews & binary formats
#
# Define decode_u32s(data) accepting bytes or bytearray with length divisible by 4, raising
# TypeError for another input type and ValueError for a partial record. Use a released
# memoryview and Struct(">I").unpack_from without bytes slices or tobytes. Demonstrate a
# bytearray packed with 120 and 80, print decoded values, change the first record to 200 with
# pack_into, and print decoded values again.
#
# Expected output:
#
# [120, 80]
# [200, 80]

