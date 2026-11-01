# Lesson 5: CSV Records & Interchange

**Prerequisites:** Levels 1–3 and Lessons 1–4 of this level. **Practice file:** `Practice/05_CSV_Records_And_Interchange.py`.

Exchange tabular records without pretending that every comma is a column boundary. Use the CSV parser to handle quoting, and keep column validation separate from numeric conversion.

## 1. A row is not a naive split

A category such as `food, lunch` contains a comma as meaningful text. CSV quoting allows it to remain one field. Manually splitting every line on commas would turn it into two fields and lose the intended record shape.

```python
import csv
from io import StringIO

text = 'category,amount\n"food, lunch",120\n'
reader = csv.DictReader(StringIO(text))
for row in reader:
    print(row["category"])  # food, lunch
```

StringIO exposes a string through a file-like interface for a small in-memory example. The CSV parser still performs real parsing. A row's values are text, so an amount field needs deliberate integer conversion before arithmetic.

## 2. Use the matching file conventions

Open CSV text files with encoding="utf-8" and newline="". The csv module manages its own newline conventions; disabling extra text newline translation avoids unwanted blank records on platforms such as Windows.

DictWriter takes an explicit fieldnames sequence, writes the header with writeheader, and writes records with writerow or writerows. DictReader uses the header to name each column. Validate the expected header rather than trusting whatever labels happen to be present.

## 3. Validate one complete record

Require the category text to be nonempty after cleanup and the amount to be a nonnegative integer. Missing fields, extra fields, and invalid numeric syntax are different input defects but can be reported under a clear invalid-record contract.

For all-or-nothing loading, build a new result list and return it only after every row succeeds. A caller's existing tracker must not be partially replaced as each row arrives. A skip-and-report importer is another legitimate design, but it must retain source positions and rejection reasons explicitly.

## 4. Preserve format responsibilities

The parser handles delimiters and quoting. Your code handles category normalization and numeric rules. Avoid replacing a proper parser with split simply because the first sample has no quoted fields.

A CSV reader can span multiple physical lines for a quoted field. If you report `reader.line_num`, it describes consumed input lines rather than a simple one-record-per-line assumption. Define which position you report so diagnostics can be followed accurately.

## Detect incomplete and overlong CSV rows

For DictReader, `reader.fieldnames` is the header list. Comparing it with `["category", "amount"]` checks both the names and their required order. A short row fills missing values with None; extra values are collected under a None key by default. Therefore `None in row` detects extra fields, and `row.get("amount") is None` detects a missing amount before conversion. An empty field is text `""`, which is a different defect and can be rejected by cleanup or int conversion. Build the returned list only from fully validated rows.

References: [CSV module](https://docs.python.org/3.13/library/csv.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict how many fields the quoted category produces.
2. **Explain:** Explain why CSV amounts arrive as strings.
3. **Modify:** Round-trip a category containing both a comma and an accent.
4. **Debug:** Replace a split-based parser that breaks a quoted field.

<details>
<summary>Hints</summary>

Let the library quote fields and validate records only after parsing them.

</details>

## Independent task: csv records & interchange

In `Practice/05_CSV_Records_And_Interchange.py`, complete this task:

Define `write_expenses(path, records)` using DictWriter with the columns category and amount and newline="". Assume records are already valid. Define `read_expenses(path)` using DictReader, require exactly those headers, and convert amounts to nonnegative integers while rejecting missing/extra fields and blank categories with ValueError. Round-trip `[{"category": "food, lunch", "amount": 120}]` and print the first category and amount as labeled lines.

Expected output:

```text
Category: food, lunch
Amount: 120
```
