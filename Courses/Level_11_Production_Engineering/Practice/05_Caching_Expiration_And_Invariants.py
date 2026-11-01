# Independent task: caching, expiration & invariants
#
# Implement TTLCache(ttl, capacity, clock=time.monotonic) with a finite positive int/float ttl
# (excluding bool) and positive plain-integer capacity, raising ValueError otherwise. Store
# string values by string key; reject non-string keys/values in set with ValueError. get returns
# None when missing/expired; set removes expired entries and evicts the earliest-expiring entry
# when a new key would exceed capacity. Use an injected clock starting at 0, set total to "150",
# print it, advance to 5 with ttl 5, and print the expired lookup.
#
# Expected output:
#
# 150
# None

