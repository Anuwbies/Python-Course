# Independent task: Managed streaming expense pipeline
#
# Implement RowError(ValueError), parse_rows(lines) yielding normalized category/amount
# dictionaries from nonblank JSON lines, and open_rows(path) as a context manager keeping the
# UTF-8 file open during iteration. Reject invalid JSON, blank categories,
# non-plain-integer/negative amounts, and wrong fields with a line-numbered RowError and an
# explicit cause.
#
# Implement summarize(records) returning a dictionary of totals by category. Decorate it with a
# successful-call counter exposed as calls; increment only after the function returns normally.
# Demonstrate a real file containing food/120, travel/30, food/80, print alphabetical totals,
# and print the completed call count. Do not keep a list of all parsed records.
#
# Expected output:
#
# food: PHP 200
# travel: PHP 30
# Completed calls: 1

