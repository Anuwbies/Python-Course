# Level 5 capstone: Installable expense-report command

**Prerequisites:** [all lessons in Level 5](../../Courses/Level_05_Practical_Software_Development/README.md). **Submission:** `Practice/project.py`.

Turn the tracker's calculations into a documented command-line application. The command reads a JSON list of plain nonnegative integer amounts and prints a budget report. Keep parsing, calculation, and display separate enough to test real behavior without invoking an interactive menu.

Use an environment and install pytest for the accompanying tests. A supplied pyproject file in each project directory describes an editable local installation; it exposes expense-report through project:main. From the repository root, install your own implementation with `python -m pip install -e Capstones/Level_05_Practical_Software_Development/Practice`, then run `expense-report path/to/amounts.json --budget 500`. The reference installation is separate and should not be installed under the same command at the same time.

The sample file is `Data/amounts.json` relative to this capstone folder. Tests are a learning deliverable for the application's contracts, not a course-grading tool. Run them from the corresponding Practice or Solutions directory so the adjacent project module is the intended import.

## Project task

Implement `load_amounts(path)` with JSON shape/type/range validation, `summarize(amounts, budget)` returning count/total/remaining without mutation, and `main(argv=None)` accepting a JSON path plus required integer --budget. Reject a negative budget and report file/validation errors with a nonzero exit status. Display entries, spent, and remaining as labeled lines.

Write pytest cases in a neighboring test_project.py for empty input, ordinary totals, overspending, malformed files, Boolean amounts, and input preservation. Use tmp_path for files. Complete the supplied pyproject metadata and install locally; do not publish.

For JSON `[120, 80]` and budget 500, expected stdout is:

```text
Entries: 2
Spent: PHP 200
Remaining: PHP 300
```
