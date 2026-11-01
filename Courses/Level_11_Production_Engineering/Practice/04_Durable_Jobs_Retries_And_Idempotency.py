# Independent task: durable jobs, retries & idempotency
#
# Implement enqueue(connection,key,amount) with a nonblank string key and nonnegative
# plain-integer payload; return the job key, returning that same key for a repeated matching
# request and raising ValueError for a different amount. Implement
# process(connection,key,fail=False) for one worker: missing jobs raise KeyError, completed jobs
# return False, and exhausted attempts raise RuntimeError before another effect. Attempts are
# bounded at 3 and persisted before the effect. In one effect transaction insert a unique
# receipt and mark completion; a simulated RuntimeError before completion rolls back that
# effect. A successful new effect returns True.
#
# Demonstrate one failed attempt, a successful retry, and a completed replay. Print the
# committed receipt count and completed replay result.
#
# Expected output:
#
# Attempt failed
# Receipts: 1
# Replay performed work: False

