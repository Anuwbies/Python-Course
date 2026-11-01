# Independent task: observability, readiness & recovery
#
# Define health_snapshot(connection) to execute a real SELECT COUNT(*) FROM orders, returning
# ready=True and an actual perf_counter_ns duration on success, or ready=False and a duration
# for sqlite3.Error. Demonstrate an initialized in-memory connection, then close it and probe
# again. Print the two actual readiness values. Do not return fixed readiness flags without
# attempting the query.
#
# Expected output:
#
# True
# False

