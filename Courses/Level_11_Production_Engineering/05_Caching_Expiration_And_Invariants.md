# Lesson 5: Caching, Expiration & Invariants

**Prerequisites:** Levels 1–10 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Caching_Expiration_And_Invariants.py`.

Use a cache as a derived representation with an explicit lifetime and identity. A cache hit is useful only when its value belongs to the right request and its staleness is acceptable.

## 1. State the source of truth

A cache stores a reusable result; the underlying database or calculation remains authoritative. Define which changes invalidate the result or how long stale data may be accepted. A fast incorrect answer is not an improvement.

Key construction includes all dimensions that affect the result, such as resource ID, query parameters, and authorization scope when responses are private. A key containing only a path can leak one user's representation to another if identity affects the output.

## 2. Use a monotonic clock for local TTL

A time-to-live is a duration. time.monotonic is appropriate for local elapsed expiration because wall-clock adjustments should not unexpectedly extend a cached lifetime. Store an expiration boundary and treat equality with that boundary as expired under a clearly stated policy.

Injecting a clock callable makes expiration tests deterministic without sleeping. The test advances a controlled clock value; the actual deployment supplies the real monotonic clock. This is an intentional test dependency, not a claim that time was measured when it was not.

## 3. Bound retained entries

Expiration alone does not ensure a small cache if expired entries remain stored or the key space grows faster than cleanup. Set a capacity and an eviction policy. A simple earliest-expiry eviction is understandable but can cost a scan; more demanding caches need suitable data structures and concurrency handling.

A plain dictionary cache is local to one process. Several API workers do not automatically share its values or invalidations. A shared Redis cache changes those operational properties but introduces an external dependency and serialization choices.

## 4. Cache after permission decisions

Apply authentication/authorization before returning protected data, including cached data. Invalidate only after the authoritative change commits, or choose an immutable result whose identity never changes. A failed write should not publish a cache entry representing a change that never committed.

Redis SET with EX can set a value and its expiration in one operation. A separate SET then EXPIRE sequence has a failure window leaving an unexpected lifetime. The capstone caches immutable completed reports, which simplifies invalidation while still requiring access control.

## Implement the local cache boundaries

Import isfinite from math when accepting a numeric TTL: NaN and infinity do not form useful finite expiration durations. Check `type(ttl) in (int, float)`, `isfinite(ttl)`, and ttl > 0; this rejects Boolean TTLs. Require type(capacity) is int and capacity > 0. For earliest-expiry eviction, `min(entries, key=lambda key: entries[key][0])` selects the key whose stored expiration is smallest. min is analogous to the key-based sorted operation, but returns one selected item; only call it on a nonempty mapping. Iterate list(entries) when deleting expired keys so the iteration uses a snapshot.

## Use Redis expiration and a deliberately limited adapter

With `decode_responses=True`, Redis get returns text or None. `cache.set(key, text, ex=30)` stores text with a 30-second expiry in one command. `cache.ttl(key)` observes remaining seconds, or negative missing/no-expiry states; it does not refresh the lifetime. `cache.ping()` checks the service and `cache.close()` releases the client. Serialize a completed immutable report body with json.dumps and parse it with json.loads. If RedisError interrupts get or set, read from the authoritative report row and record the cache problem without losing the report.

A test may inject an IsolatedCache implementing ping/get/set/close using an ordinary dictionary. Its set method can assert the requested ex is 30. If that adapter never advances a clock, it establishes interface usage and cache-hit data only, not real expiration. Test TTL with the local injected-clock cache or the actual Redis stack according to the claim being checked. Always complete authorization before asking either cache for protected report data.

References: [Monotonic clock](https://docs.python.org/3.13/library/time.html#time.monotonic), [Redis SET expiration](https://redis.io/docs/latest/commands/set/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict a lookup exactly at its expiration boundary.
2. **Explain:** Explain why a local TTL should not rely on wall-clock time jumps.
3. **Modify:** Advance an injected clock instead of sleeping in a test.
4. **Debug:** Find a cache key missing a user or query dimension.

<details>
<summary>Hints</summary>

Expire equality at the boundary and keep capacity separate from the TTL rule.

</details>

## Independent task: caching, expiration & invariants

In `Practice/05_Caching_Expiration_And_Invariants.py`, complete this task:

Implement TTLCache(ttl, capacity, clock=time.monotonic) with a finite positive int/float ttl (excluding bool) and positive plain-integer capacity, raising ValueError otherwise. Store string values by string key; reject non-string keys/values in set with ValueError. get returns None when missing/expired; set removes expired entries and evicts the earliest-expiring entry when a new key would exceed capacity. Use an injected clock starting at 0, set total to "150", print it, advance to 5 with ttl 5, and print the expired lookup.

Expected output:

```text
150
None
```
