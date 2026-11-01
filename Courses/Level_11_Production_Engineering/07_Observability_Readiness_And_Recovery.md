# Lesson 7: Observability, Readiness & Recovery

**Prerequisites:** Levels 1–10 and Lessons 1–6 of this level. **Practice file:** `Practice/07_Observability_Readiness_And_Recovery.py`.

Give an operator evidence of what the service is doing and a rehearsed path to recover. Logs, metrics, probes, and backups are useful only when their scope and failure behavior are understood.

## 1. Distinguish liveness and readiness

A liveness probe asks whether the process can run its basic loop. A readiness probe asks whether this instance can serve the operation expected of it, including required dependencies and schema state. Returning ok unconditionally does not establish database readiness.

Probe real bounded operations such as a lightweight query and a cache ping, with timeouts. A slow unbounded probe can itself exhaust the service. Keep sensitive exception details out of public probe responses while preserving useful diagnostics in controlled logs.

## 2. Correlate observations

Request IDs can connect a response, structured log event, and downstream work. Treat externally supplied identifiers as untrusted: bound their length and character set or generate a new value. Do not log authorization headers or secret-bearing URLs.

Latency, request/error counts, queue depth, retry counts, and dependency failures answer different questions. A metric without units or a time window can be misleading. Avoid high-cardinality labels such as every user's token or arbitrary URL query string.

## 3. Rehearse recovery against actual data

A backup command exiting successfully is not a completed recovery rehearsal. Restore into an isolated destination, inspect representative rows and schema revision, and compare the application's required behavior. Document who owns the backup, its retention, and the point in time it represents.

Database data, migration history, cache state, and pending jobs have different recovery needs. A disposable cache can be rebuilt; a durable job table should not silently disappear. Do not delete a volume as a routine restart step.

## 4. Preserve an honest incident boundary

During a dependency failure, show an appropriate readiness failure and avoid acknowledging work that did not commit. After recovery, confirm the actual operation succeeds rather than relying on a restarted process alone.

The exercise uses a real SQLite query and a closed connection to demonstrate readiness failure. The deployment capstone adds PostgreSQL, Redis, a worker, and explicit backup/restore commands. Passing the local exercise does not establish the container stack or its recovery rehearsal.

## Implement request observation without exposing payloads

Import Request from fastapi. A handler registered with `@app.middleware("http")` receives `(request: Request, call_next)` and awaits `call_next(request)` to obtain the downstream response. It can then set response.headers and return that same response. Observe actual status_code rather than printing an assumed success.

For a request ID, import ascii_letters and digits from string and uuid4 from uuid. Build `allowed = set(ascii_letters + digits + "-_.")`; retain a supplied header only if it is nonempty, at most 64 characters, and `set(supplied) <= allowed`. Otherwise generate uuid4().hex. request.headers.get reads the incoming header; response.headers["X-Request-ID"] echoes the bounded identifier. This avoids newlines and arbitrary header contents entering diagnostic records.

`request.method` is the HTTP verb. After routing, `route = request.scope.get("route")` and `getattr(route, "path", "unmatched")` obtain a route template instead of an arbitrary user-supplied URL. getattr returns the named attribute or the supplied fallback. Use perf_counter for monotonic elapsed seconds, then multiply by 1000 for a duration_ms log field. A broad except Exception is appropriate here only to count/log an unexpected request failure and immediately re-raise; never turn it into a successful response. Count successful and failed completed requests on the event loop without an intervening await during the update. A snapshot from dict(metrics) is local to this process and may include the current /metrics request only after its response has completed.

`@asynccontextmanager` on an async lifespan generator can yield once and close the cache/dispose the engine in finally. Pass it as `FastAPI(lifespan=lifespan)`. This applies Level 9's managed async lifetime to real clients; a TestClient context runs it too. Avoid silently sharing those owned clients between independent applications.

## Rehearse the database's recovery tools

Within the completed Compose project, `docker compose exec db pg_dump -U course -d course -Fc -f /tmp/course.dump` writes a PostgreSQL custom-format backup. `createdb -U course restore_demo` makes an isolated destination; `pg_restore -U course -d restore_demo /tmp/course.dump` restores there. Run these latter tools through docker compose exec db as well. `docker compose cp db:/tmp/course.dump ./course.dump` copies the binary file out without text redirection. Inspect `SELECT version_num FROM alembic_version` and representative orders/jobs/reports in the restore database before calling the rehearsal successful. These commands are taught operational actions; their supplied spelling does not establish that they ran on a machine without Docker.

References: [PostgreSQL backups](https://www.postgresql.org/docs/17/backup.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether a live process can still be unready.
2. **Explain:** Explain why a restored backup needs application-level inspection.
3. **Modify:** Add a bounded real dependency probe without exposing its credentials.
4. **Debug:** Find a health route that prints success without querying its dependency.

<details>
<summary>Hints</summary>

The failure result should come from the actual failed probe after the connection closes.

</details>

## Independent task: observability, readiness & recovery

In `Practice/07_Observability_Readiness_And_Recovery.py`, complete this task:

Define health_snapshot(connection) to execute a real `SELECT COUNT(*) FROM orders`, returning ready=True and an actual perf_counter_ns duration on success, or ready=False and a duration for sqlite3.Error. Demonstrate an initialized in-memory connection, then close it and probe again. Print the two actual readiness values. Do not return fixed readiness flags without attempting the query.

Expected output:

```text
True
False
```
