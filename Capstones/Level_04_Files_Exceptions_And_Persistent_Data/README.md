# Level 4 capstone: Persistent expense store

**Prerequisites:** [all lessons in Level 4](../../Courses/Level_04_Files_Exceptions_And_Persistent_Data/README.md). **Submission:** `Practice/project.py`.

Build a storage boundary for the tracker using a versioned JSON document. The format is an object with version 1 and an expenses list. Every expense has a nonempty normalized category and a plain nonnegative integer amount. Reject a corrupt document as a whole rather than replacing it with an empty successful result.

A missing first-use file returns an empty list under this project's explicit policy. Permission failures and malformed existing data remain errors. Saving validates the entire candidate before a unique temporary replacement. This is a single-writer local learning store, not a concurrent database or a power-loss durability guarantee.

The demonstration uses an isolated temporary directory. Your functions must accept caller-supplied paths, so a later application can choose persistent storage without editing function internals.

## Project task

Implement `validate_records(value)` returning normalized copies or raising ValueError; `load_expenses(path)` returning [] only for FileNotFoundError and otherwise validating `{"version": 1, "expenses": [...]}`; and `save_expenses(path, records)` validating before a same-directory temporary-file replacement with cleanup.

Require exactly version/expenses at document level and category/amount on every record. Version must be the plain integer 1. Reject Boolean amounts, negative amounts, missing/extra fields, non-dictionary records, non-list collections, unsupported versions, and categories that are not strings or become blank after stripping. Do not mutate caller records. Other I/O errors propagate.

Demonstrate a missing file, save food/120 and travel/30, load and print count and total, attempt an invalid save, and read the destination again to demonstrate it is unchanged.

Expected output:

```text
Missing entries: 0
Entries: 2
Total: PHP 150
Invalid save rejected
Preserved: True
```
