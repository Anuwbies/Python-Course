from struct import Struct

RECORD = Struct(">I")

def decode_u32s(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Expected a byte buffer")
    if len(data) % RECORD.size:
        raise ValueError("Partial record")
    with memoryview(data) as view:
        return [RECORD.unpack_from(view, offset)[0] for offset in range(0, len(view), RECORD.size)]

data = bytearray(8)
RECORD.pack_into(data, 0, 120)
RECORD.pack_into(data, 4, 80)
print(decode_u32s(data))
RECORD.pack_into(data, 0, 200)
print(decode_u32s(data))
