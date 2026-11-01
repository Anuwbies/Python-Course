# Level 2 capstone: Menu-driven expense tracker

**Prerequisites:** [all lessons in Level 2](../../Courses/Level_02_Control_Flow_And_Collections/README.md). **Submission:** `Practice/project.py`.

Extend the budget idea into an in-memory tracker that accepts multiple expenses. A command loop controls the application; a list preserves the individual records; a dictionary supplies grouped totals. There are no files or custom functions in this version.

Normalize commands and category labels with strip/lower. Store each accepted amount once. A summary should work before any expenses have been added: count and total are both zero. Unknown commands should display a clear message and return to the next command rather than terminating.

Run `Practice/project.py` with Python from this folder or with its full repository-relative path. The data lasts only for that process. Keep individual records so later levels can add functions and persistence without changing what an expense means.

## Project task

Implement a loop with commands `add`, `summary`, and `quit`. Print `Command (add/summary/quit):` before each command input. For add, print `Category:` then read the label; print `Amount (whole PHP):` then read integer text. Reject an empty category or a negative amount with `Rejected`; otherwise append a record and print `Added`. All numeric responses are valid integer text. Unknown commands print `Unknown command`.

For summary, print `Entries: <count>`, `Total: PHP <total>`, and category totals as `<category>: PHP <amount>` in alphabetical order. Quit prints `Goodbye`. Use only concepts from Levels 1–2.

Sample input:

```text
add
food
120
add
travel
30
summary
quit
```

Expected output:

```text
Command (add/summary/quit):
Category:
Amount (whole PHP):
Added
Command (add/summary/quit):
Category:
Amount (whole PHP):
Added
Command (add/summary/quit):
Entries: 2
Total: PHP 150
food: PHP 120
travel: PHP 30
Command (add/summary/quit):
Goodbye
```
