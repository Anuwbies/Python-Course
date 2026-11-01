# Lesson 4: Durable Jobs, Retries & Idempotency

**Prerequisites:** Levels 1–10 and Lessons 1–3 of this level. **Practice file:** `Practice/04_Durable_Jobs_Retries_And_Idempotency.py`.

Preserve the intention to do work and define what a retry means. A durable job and an idempotency key reduce specific failure risks; neither guarantees exactly-once effects across arbitrary external systems.

## 1. Save the intention before acknowledging it

An in-memory queue loses pending work on process failure. A durable job row records the payload, identity, state, and attempt information so another worker can resume after restart. When a database change and job creation describe one business action, store them in the same transaction or use an outbox design.

A message saying queued is meaningful only after that intention has committed. A worker must distinguish pending, completed, and permanently failed work instead of assuming that receiving a message means it ran successfully.

## 2. Identify repeated requests

An idempotency key identifies the same logical request. Reusing the key with different payload data should be rejected, not silently accepted as the same effect. A uniqueness constraint provides a database-enforced coordination point; an unprotected check-then-insert is not sufficient under concurrent writers.

For a local database effect, write the result and completion state together. Repeating the same completed job can then return the existing result. An external email or payment has a separate effect boundary and requires that system's idempotency or reconciliation policy.

## 3. Retry only under a bounded policy

Distinguish transient failures from invalid input and programming errors. Limit attempts and apply a delay/backoff policy where repeated immediate work would overload a dependency. Persist attempts so process restarts do not reset an exhausted retry budget.

If an effect transaction rolls back, an attempt record written in that same transaction also rolls back. Decide which information must survive a failed effect. The exercise stores an attempt before the effect transaction; the capstone uses a transaction/savepoint design for an entirely database-local report effect.

## 4. Demonstrate partial-effect rollback

A failure after inserting a result but before marking a job complete is a useful test. If both operations share a transaction, the failure should leave no committed partial result. Then retry and inspect the actual result table, rather than printing a fixed success message.

The exercise assumes one worker and SQLite. The deployment capstone uses PostgreSQL row locking with SKIP LOCKED for independent workers; a successful single-worker SQLite test does not establish that cross-worker locking behavior.

## Build the local durable tables before processing

For the single-worker practice, use jobs(key TEXT PRIMARY KEY, amount INTEGER NOT NULL CHECK(amount >= 0), status TEXT NOT NULL, attempts INTEGER NOT NULL CHECK(attempts BETWEEN 0 AND 3)) and receipts(key TEXT PRIMARY KEY REFERENCES jobs(key), amount INTEGER NOT NULL). Enable SQLite foreign keys. `INSERT OR IGNORE` leaves an existing unique key unchanged; immediately read the stored payload and reject a mismatch rather than treating all conflicts as equivalent. `SELECT COUNT(*)` counts actual committed receipts. `connection.executescript(text)` runs a trusted multi-statement setup script; keep it outside the effect transaction because it has separate transaction behavior. Individual execute calls are also sufficient.

## Coordinate the capstone's database-local effects

An ORM Job can use `id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))`, importing uuid4 from uuid. The callable produces a new UUID string at insertion time, not one shared value at import. A unique request_key identifies one logical summary request. A status CHECK accepts pending/done/failed; attempts is bounded at 0..3. A nullable last_error stores a safe code, and `created_at: Mapped[datetime]` can use `DateTime(timezone=True), server_default=func.now()`. Report.job_id is both its primary key and ForeignKey("jobs.id"), enforcing at most one report per job.

`select(Job).where(Job.status == "pending", Job.attempts < 3).order_by(Job.created_at, Job.id).with_for_update(skip_locked=True).limit(1)` selects and locks one eligible PostgreSQL row. SKIP LOCKED lets another worker choose a different unlocked job; it is not provided by the SQLite test adapter. Hold the transaction until that job's short local effect and status are settled.

The following transaction pattern explains which updates survive a simulated effect failure; Job and Report are the mapped tables described above:

```python
with Session(engine) as session:
    with session.begin():
        job = session.scalar(statement)  # statement selects one locked job
        if job is not None:
            job.attempts += 1
            attempt = job.attempts
            session.flush()  # establish the attempt outside the savepoint
            try:
                with session.begin_nested():
                    session.add(Report(job_id=job.id, body='{"orders": 0}'))
                    session.flush()
                    if simulate_failure:
                        raise RuntimeError("Simulated local failure")
                    job.status = "done"
                    session.flush()
            except RuntimeError:
                job.status = "failed" if attempt >= 3 else "pending"
```

begin_nested creates a savepoint inside the outer transaction. An error rolls back the receipt/result and status changes inside it, while the previously flushed attempt remains available to commit in the outer transaction. Reassign the failure status after rollback. An outer database failure still rolls back the whole unit; this is not an independent audit of every attempted external effect. `select(func.count(Order.id), func.coalesce(func.sum(Order.quantity), 0))` returns a count and zero-safe total without loading all orders.

On an enqueue uniqueness race, session.commit can raise IntegrityError from sqlalchemy.exc. Call session.rollback before looking up the existing request key. Return that existing job only when it really exists; otherwise re-raise the unexpected error. This complements the unique constraint instead of relying on a check-then-insert alone.

## Stop a polling worker cooperatively

`threading.Event` provides set(), is_set(), and wait(seconds); wait returns early when another path sets it. In the launcher's main thread, `signal.signal(signal.SIGINT, request_stop)` and SIGTERM register a small handler with signature `(signum, frame)` that calls stop.set(). Loop while not stop.is_set(), call process_one, then stop.wait(0.2 if work_was_done else 0.5). Catch only documented transient OperationalError for a one-second reconnect wait; unexpected SQL/programming errors remain visible. Dispose the engine in finally. This supports graceful stop between bounded database operations, not forced interruption of arbitrary Python code.

References: [Transactions](https://docs.python.org/3.13/library/sqlite3.html#transaction-control).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which attempt metadata survives a rolled-back effect transaction.
2. **Explain:** Explain why the same key with a different payload is not the same request.
3. **Modify:** Add a bounded attempt policy instead of retrying forever.
4. **Debug:** Find a queued message sent before its durable intention has committed.

<details>
<summary>Hints</summary>

Persist the attempt, then keep the local effect and done state in the same effect transaction.

</details>

## Independent task: durable jobs, retries & idempotency

In `Practice/04_Durable_Jobs_Retries_And_Idempotency.py`, complete this task:

Implement enqueue(connection,key,amount) with a nonblank string key and nonnegative plain-integer payload; return the job key, returning that same key for a repeated matching request and raising ValueError for a different amount. Implement process(connection,key,fail=False) for one worker: missing jobs raise KeyError, completed jobs return False, and exhausted attempts raise RuntimeError before another effect. Attempts are bounded at 3 and persisted before the effect. In one effect transaction insert a unique receipt and mark completion; a simulated RuntimeError before completion rolls back that effect. A successful new effect returns True.

Demonstrate one failed attempt, a successful retry, and a completed replay. Print the committed receipt count and completed replay result.

Expected output:

```text
Attempt failed
Receipts: 1
Replay performed work: False
```
