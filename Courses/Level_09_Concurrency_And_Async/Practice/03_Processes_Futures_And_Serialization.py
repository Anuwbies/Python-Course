# Independent task: processes, futures & serialization
#
# Define square(number) at module scope. In a guarded main block, use ProcessPoolExecutor with
# two workers to map it over [1,2,3]. Materialize and print the results in input order. Use an
# executor context manager and do not launch a pool during import.
#
# Expected output:
#
# [1, 4, 9]

