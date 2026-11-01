# Independent task: csv records & interchange
#
# Define write_expenses(path, records) using DictWriter with the columns category and amount and
# newline="". Assume records are already valid. Define read_expenses(path) using DictReader,
# require exactly those headers, and convert amounts to nonnegative integers while rejecting
# missing/extra fields and blank categories with ValueError. Round-trip [{"category": "food,
# lunch", "amount": 120}] and print the first category and amount as labeled lines.
#
# Expected output:
#
# Category: food, lunch
# Amount: 120

