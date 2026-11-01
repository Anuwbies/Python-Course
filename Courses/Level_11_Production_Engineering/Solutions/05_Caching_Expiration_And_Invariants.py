from math import isfinite
from time import monotonic

class TTLCache:
    def __init__(self, ttl, capacity, clock=monotonic):
        if type(ttl) not in (int, float) or not isfinite(ttl) or ttl <= 0 or type(capacity) is not int or capacity <= 0:
            raise ValueError("Invalid cache bounds")
        self._ttl = ttl
        self._capacity = capacity
        self._clock = clock
        self._entries = {}

    def get(self, key):
        entry = self._entries.get(key)
        if entry is None:
            return None
        expires, value = entry
        if self._clock() >= expires:
            del self._entries[key]
            return None
        return value

    def set(self, key, value):
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("Expected text key and value")
        now = self._clock()
        for existing in list(self._entries):
            if self._entries[existing][0] <= now:
                del self._entries[existing]
        if key not in self._entries and len(self._entries) >= self._capacity:
            oldest = min(self._entries, key=lambda item: self._entries[item][0])
            del self._entries[oldest]
        self._entries[key] = (now + self._ttl, value)

now = [0]
cache = TTLCache(5, 2, clock=lambda: now[0])
cache.set("total", "150")
print(cache.get("total"))
now[0] = 5
print(cache.get("total"))
