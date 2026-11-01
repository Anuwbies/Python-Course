# Independent task: Bounded concurrent local-file processor
#
# Implement async count_files(paths, workers=2) returning a dictionary by unique file name. Each
# result is either {"count": integer} or {"error": exception_type_name}. Reject nonpositive
# workers or duplicate names. Use a queue of capacity workers*2, exactly workers worker tasks in
# a TaskGroup, one None sentinel per worker, and task_done in finally. Catch only OSError and
# UnicodeError as per-file failures.
#
# Demonstrate two actual temporary files a.txt containing one two and b.txt containing three,
# plus a missing.txt path. Print alphabetical outcomes. Do not hardcode counts or fabricate a
# missing-file result without attempting the read.
#
# Expected output:
#
# a.txt: 2
# b.txt: 1
# missing.txt: ERROR FileNotFoundError

