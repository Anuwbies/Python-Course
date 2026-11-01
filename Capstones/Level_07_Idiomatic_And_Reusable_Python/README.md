# Level 7 capstone: Managed streaming expense pipeline

**Prerequisites:** [all lessons in Level 7](../../Courses/Level_07_Idiomatic_And_Reusable_Python/README.md). **Submission:** `Practice/project.py`.

Build a lazy JSON-lines parser, a context-managed input source, and a grouping stage. Each nonblank physical line is one complete JSON expense object with category and amount. This differs from a general multi-line JSON document, so define the line format explicitly.

The file must remain open while its lazy records are consumed. A malformed record raises RowError containing its line number and an explicit cause; the pipeline does not silently skip it. Aggregation returns a new summary only after successful consumption, so a caller can decide whether to publish it.

The reference counts completed summarize calls with a decorator and demonstrates a real temporary input file. Memory usage grows with the number of categories, not necessarily with every record; calling list on the parser would deliberately materialize all records and change that property.

## Project task

Implement RowError(ValueError), `parse_rows(lines)` yielding normalized category/amount dictionaries from nonblank JSON lines, and `open_rows(path)` as a context manager keeping the UTF-8 file open during iteration. Reject invalid JSON, blank categories, non-plain-integer/negative amounts, and wrong fields with a line-numbered RowError and an explicit cause.

Implement `summarize(records)` returning a dictionary of totals by category. Decorate it with a successful-call counter exposed as calls; increment only after the function returns normally. Demonstrate a real file containing food/120, travel/30, food/80, print alphabetical totals, and print the completed call count. Do not keep a list of all parsed records.

Expected output:

```text
food: PHP 200
travel: PHP 30
Completed calls: 1
```
