# Level 4: Files, Exceptions & Persistent Data

**Stage:** Beginner. **Prerequisites:** Levels 1–3.

Preserve data across runs, distinguish absent data from corrupt or inaccessible data, and explain validation, file lifetime, and save-failure behavior.

## Reading order

| Lesson | Guide | Saved task |
| --- | --- | --- |
| 1 | [Paths, Text Files & With](01_Paths_Text_Files_And_With.md) | [Practice](Practice/01_Paths_Text_Files_And_With.py) |
| 2 | [Modes, Streaming & Line Formats](02_Modes_Streaming_And_Line_Formats.md) | [Practice](Practice/02_Modes_Streaming_And_Line_Formats.py) |
| 3 | [Specific Exceptions & Validation](03_Specific_Exceptions_And_Validation.md) | [Practice](Practice/03_Specific_Exceptions_And_Validation.py) |
| 4 | [JSON & Data Validation](04_JSON_And_Data_Validation.md) | [Practice](Practice/04_JSON_And_Data_Validation.py) |
| 5 | [CSV Records & Interchange](05_CSV_Records_And_Interchange.md) | [Practice](Practice/05_CSV_Records_And_Interchange.py) |
| 6 | [Safer Saves & Cleanup](06_Safer_Saves_And_Cleanup.md) | [Practice](Practice/06_Safer_Saves_And_Cleanup.py) |

Continue with the [Persistent expense store capstone](../../Capstones/Level_04_Files_Exceptions_And_Persistent_Data/README.md).

## Working through this level

Read the detailed explanation, trace the examples, and complete the practice ladder before the independent task. Each file in `Practice/` contains the full task, accepted inputs, and expected behavior as comments. Write your own implementation below those comments. Reference implementations are in `Solutions/`; compare them after an attempt.

Ask the assistant to review your saved submission when ready. Progress is recorded manually after review, including revisions and topics to revisit. Independent-task sections contain only the assignment and its expected behavior.

## Environment and run commands

All examples use the standard library. Reference demonstrations use TemporaryDirectory so their sample files are isolated and cleaned up. Application functions accept explicit paths and can be used with a persistent file chosen by a caller.

## Advancement

Preserve data across runs, distinguish absent data from corrupt or inaccessible data, and explain validation, file lifetime, and save-failure behavior.

Demonstrate the capstone with its documented normal, boundary, and failure cases and explain one small requirement change. Record evidence in [the Level 4 progress record](../../Progress/Level_04_Files_Exceptions_And_Persistent_Data.md). Running a reference does not complete your own submission.

## Scope and next steps

The store assumes one writer. Durable multiuser transactions arrive with databases in Level 10. Automated test organization begins in Level 5.
