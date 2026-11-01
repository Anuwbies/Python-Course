# Independent task: durable report storage
#
# Define a DeclarativeBase and the orders mapping: id integer primary key, item nonnullable
# String(80), quantity integer, note nonnullable String(120) with Python default empty. Named
# CHECKs require quantity 1..100, trimmed item length 1..80, and note length <=120.
#
# Define Job mapped to jobs: id String(36) primary key with a new uuid4 string default per
# insert; request_key nonnullable unique String(80); status nonnullable String(10) default
# pending constrained to pending/done/failed; attempts nonnullable integer default 0 constrained
# to 0..3; last_error nullable String(80); created_at nonnullable DateTime(timezone=True) with
# database func.now() default. Define Report mapped to reports with job_id String(36) primary
# key and ForeignKey jobs.id, plus nonnullable body Text containing JSON.
#
# Implement process_one(engine, fail=False). In a Session.begin transaction select one pending
# job with attempts<3 ordered by created_at,id and PostgreSQL FOR UPDATE SKIP LOCKED plus
# limit(1). Return False only when none exists. Increment/flush its attempt before a nested
# savepoint. Inside the savepoint, count actual orders and sum their quantity with zero for an
# empty sum; insert Report.body as JSON {"orders": count, "quantity": total}, flush it,
# optionally raise RuntimeError when fail=True, and mark done/clear last_error. On that
# simulated RuntimeError roll back the savepoint, set last_error to processing_failure, and mark
# pending until the third attempt, then failed. Allow other database/programming failures to
# propagate. Return True after handling an eligible job and committing.
#
# Expected behavior: one committed immutable report per completed job, no partial report after a
# failed effect, persisted bounded attempts, and no extra work on completed replay. SQLite tests
# establish local transactions, not PostgreSQL worker locking.

