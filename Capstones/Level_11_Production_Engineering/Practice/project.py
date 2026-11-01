# Independent task: Operational shared-catalog service
#
# Complete project.py as create_app(engine,cache,key), plus the neighboring storage, server,
# worker, issuer, migration, and teaching-test files according to their embedded tasks.
#
# Verify HS256 tokens with required sub/role/iat/exp/aud/iss claims and explicit
# audience/issuer/algorithm policy. Missing/invalid tokens return 401 with a Bearer challenge;
# reader writes return 403. Require admin for POST /orders, POST /reports, and GET /metrics.
# OrderInput forbids extra fields, strips text whitespace, requires item length 1..80 and strict
# integer quantity 1..100, and accepts note defaulting to empty text with max length 120. POST
# /orders returns assigned id/item/quantity/note, and GET /orders/{identifier} returns those
# stored fields or 404. Any verified reader/admin may GET shared orders/reports.
#
# POST /reports returns 202 and a durable job ID. A repeated nonblank Idempotency-Key (max80
# characters) identifies the same global-summary request and returns the same job. Reports
# reflect committed orders when processed. Completed immutable report bodies may be cached for
# 30 seconds after authorization, using an actual Redis SET expiration. Cache failure must not
# erase authoritative data.
#
# GET /live reports process liveness. GET /ready performs real database revision 0003 and Redis
# ping probes, returning 503 on documented dependency failures. Middleware retains X-Request-ID
# only when nonempty, at most 64 characters, and composed of ASCII letters/digits/-_., otherwise
# generates uuid4().hex. It returns the ID as X-Request-ID and records method, route template,
# status, and measured duration without credentials. Count/log unexpected request failures and
# re-raise them. A lifespan context closes the cache and disposes the engine on shutdown.
# /metrics reports process-local completed-request/error counts.
#
# Demonstrate actual 401, 403, 201, 202, report completion, idempotent replay, bounded failed
# attempts, cache expiration, dependency failure/recovery, and an isolated database restore.
# Console IDs, tokens, timing, and counts depend on executed operations; do not print fixed
# success claims. Use actual Docker commands for container evidence.

