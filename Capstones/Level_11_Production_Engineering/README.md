# Level 11 capstone: Operational shared-catalog service

**Prerequisites:** [all lessons in Level 11](../../Courses/Level_11_Production_Engineering/README.md). **Submission:** `Practice/project.py`.

Deploy a shared catalog API with authenticated reader/admin operations, a durable report worker, an immutable-report cache, migrations, and useful operational signals. The catalog is shared: authenticated readers may read all orders/reports; only admins create orders and report jobs. This is a coarse role model, not private per-user records.

The deployment includes PostgreSQL, Redis, a one-shot migration service, the API, and a worker. Existing Level 10 revisions are followed by 0003 for jobs/reports. The worker's short database-local report effect and done state share a transaction/savepoint; PostgreSQL SKIP LOCKED coordinates workers. It performs no external payment/email effect, so the local idempotency claim must not be generalized to arbitrary external services.

From the completed Practice directory, set a locally generated TOKEN_SECRET (for example assign the output of `python -c "import secrets; print(secrets.token_urlsafe(32))"` to that environment variable), then run `docker compose config --quiet`, `docker compose up --build --wait`, and `docker compose ps`. The host API is http://127.0.0.1:8000. The classroom database/cache ports remain internal. Requirements and complete deployment configurations are supplied alongside each implementation.

Run the operator command inside the API container with `docker compose exec api python issue_token.py --subject mika --role admin`; retain its output privately as a Bearer token. Create an order with POST /orders and JSON item/quantity, enqueue a report with POST /reports plus Idempotency-Key, then read GET /reports/{id} until done. Generate a reader token separately to demonstrate denied writes and allowed reads. Inspect actual Redis TTL for course:report:<id> after reading a completed report.

The ci.yml file is a local workflow template; activation requires deliberately placing it under the repository's .github/workflows path. Its tests use real isolated SQLite storage with an explicitly named cache adapter, so they do not establish PostgreSQL concurrency or Redis network behavior.

For recovery, stop cache and observe /ready returning 503, restart it, and observe recovery. Back up with `docker compose exec db pg_dump -U course -d course -Fc -f /tmp/course.dump`, create an isolated restore database with `docker compose exec db createdb -U course restore_demo`, then restore with `docker compose exec db pg_restore -U course -d restore_demo /tmp/course.dump`. Inspect row counts and revision there. Use `docker compose cp db:/tmp/course.dump ./course.dump` to retain a binary backup without a shell text-redirection pipeline. `docker compose down` preserves the named database volume.

## Project task

Complete project.py as create_app(engine,cache,key), plus the neighboring storage, server, worker, issuer, migration, and teaching-test files according to their embedded tasks.

Verify HS256 tokens with required sub/role/iat/exp/aud/iss claims and explicit audience/issuer/algorithm policy. Missing/invalid tokens return 401 with a Bearer challenge; reader writes return 403. Require admin for POST /orders, POST /reports, and GET /metrics. OrderInput forbids extra fields, strips text whitespace, requires item length 1..80 and strict integer quantity 1..100, and accepts note defaulting to empty text with max length 120. POST /orders returns assigned id/item/quantity/note, and GET /orders/{identifier} returns those stored fields or 404. Any verified reader/admin may GET shared orders/reports.

POST /reports returns 202 and a durable job ID. A repeated nonblank Idempotency-Key (max80 characters) identifies the same global-summary request and returns the same job. Reports reflect committed orders when processed. Completed immutable report bodies may be cached for 30 seconds after authorization, using an actual Redis SET expiration. Cache failure must not erase authoritative data.

GET /live reports process liveness. GET /ready performs real database revision 0003 and Redis ping probes, returning 503 on documented dependency failures. Middleware retains X-Request-ID only when nonempty, at most 64 characters, and composed of ASCII letters/digits/-_., otherwise generates uuid4().hex. It returns the ID as X-Request-ID and records method, route template, status, and measured duration without credentials. Count/log unexpected request failures and re-raise them. A lifespan context closes the cache and disposes the engine on shutdown. /metrics reports process-local completed-request/error counts.

Demonstrate actual 401, 403, 201, 202, report completion, idempotent replay, bounded failed attempts, cache expiration, dependency failure/recovery, and an isolated database restore. Console IDs, tokens, timing, and counts depend on executed operations; do not print fixed success claims. Use actual Docker commands for container evidence.
