# Independent task: Reusable expense-tracker functions
#
# Define add_expense(records, category, amount) to strip/lower the category and return a new
# outer list with a new record appended. Return None for a blank category or negative amount;
# assume amount is an integer. Do not change the incoming list or its existing records.
#
# Define summarize(records) to return {"count": count, "total": total, "by_category": totals}.
# Define print_summary(summary) to display entries, total, and alphabetical category totals.
# Calculation helpers must not print.
#
# In a guarded demonstration, start with an empty original list, add food/120 and travel/30
# through returned lists, and print the original count followed by the final summary. Include
# assertions for an empty summary, rejection, and preservation of the original list.
#
# Expected output:
#
# Original entries: 0
# Entries: 2
# Total: PHP 150
# food: PHP 120
# travel: PHP 30

