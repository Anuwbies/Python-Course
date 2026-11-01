# Independent task: Installable expense-report command
#
# Implement load_amounts(path) with JSON shape/type/range validation, summarize(amounts, budget)
# returning count/total/remaining without mutation, and main(argv=None) accepting a JSON path
# plus required integer --budget. Reject a negative budget and report file/validation errors
# with a nonzero exit status. Display entries, spent, and remaining as labeled lines.
#
# Write pytest cases in a neighboring test_project.py for empty input, ordinary totals,
# overspending, malformed files, Boolean amounts, and input preservation. Use tmp_path for
# files. Complete the supplied pyproject metadata and install locally; do not publish.
#
# For JSON [120, 80] and budget 500, expected stdout is:
#
# Entries: 2
# Spent: PHP 200
# Remaining: PHP 300

