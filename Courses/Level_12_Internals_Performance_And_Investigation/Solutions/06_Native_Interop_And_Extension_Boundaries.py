import ctypes
from ctypes.util import find_library
import os

name = "msvcrt" if os.name == "nt" else find_library("c")
if not name:
    raise RuntimeError("System C library unavailable")
library = ctypes.CDLL(name)
absolute = library.abs
absolute.argtypes = [ctypes.c_int]
absolute.restype = ctypes.c_int
bits = ctypes.sizeof(ctypes.c_int) * 8
maximum = 2 ** (bits - 1) - 1

def native_abs(value):
    if type(value) is not int or not -maximum <= value <= maximum:
        raise ValueError("Outside the supported C int range")
    return absolute(value)

print(native_abs(-12))
try:
    native_abs(2 ** bits)
except ValueError:
    print("Rejected")
