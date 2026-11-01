# Level 3 capstone: Reusable expense-tracker functions

**Prerequisites:** [all lessons in Level 3](../../Courses/Level_03_Functions_Scope_And_Modules/README.md). **Submission:** `Practice/project.py`.

Refactor the tracker's data transformations into functions with explicit effects. Keep entries as category/amount dictionaries in a list. The interface should support both a future interactive menu and a future persistence layer without reading input inside a calculation.

This project's demonstration uses known records so the review can focus on function contracts, copying, repeated calls, and returned values. Keep the implementation in one script for now, with a guarded demonstration. The modules lesson shows how to split it afterward without changing those interfaces.

## Project task

Define `add_expense(records, category, amount)` to strip/lower the category and return a new outer list with a new record appended. Return None for a blank category or negative amount; assume amount is an integer. Do not change the incoming list or its existing records.

Define `summarize(records)` to return `{"count": count, "total": total, "by_category": totals}`. Define `print_summary(summary)` to display entries, total, and alphabetical category totals. Calculation helpers must not print.

In a guarded demonstration, start with an empty original list, add food/120 and travel/30 through returned lists, and print the original count followed by the final summary. Include assertions for an empty summary, rejection, and preservation of the original list.

Expected output:

```text
Original entries: 0
Entries: 2
Total: PHP 150
food: PHP 120
travel: PHP 30
```
