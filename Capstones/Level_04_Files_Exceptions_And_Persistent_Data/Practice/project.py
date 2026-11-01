# Independent task: Persistent expense store
#
# Implement validate_records(value) returning normalized copies or raising ValueError;
# load_expenses(path) returning [] only for FileNotFoundError and otherwise validating
# {"version": 1, "expenses": [...]}; and save_expenses(path, records) validating before a
# same-directory temporary-file replacement with cleanup.
#
# Require exactly version/expenses at document level and category/amount on every record.
# Version must be the plain integer 1. Reject Boolean amounts, negative amounts, missing/extra
# fields, non-dictionary records, non-list collections, unsupported versions, and categories
# that are not strings or become blank after stripping. Do not mutate caller records. Other I/O
# errors propagate.
#
# Demonstrate a missing file, save food/120 and travel/30, load and print count and total,
# attempt an invalid save, and read the destination again to demonstrate it is unchanged.
#
# Expected output:
#
# Missing entries: 0
# Entries: 2
# Total: PHP 150
# Invalid save rejected
# Preserved: True

