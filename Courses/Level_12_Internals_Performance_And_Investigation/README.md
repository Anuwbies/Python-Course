# Level 12: Internals, Performance & Investigation

**Stage:** Expert. **Prerequisites:** Levels 1–9.

Independently investigate unfamiliar runtime behavior, consult versioned primary sources, design reproducible experiments, preserve correctness, and explain observed performance/ownership tradeoffs.

## Reading order

| Lesson | Guide | Saved task |
| --- | --- | --- |
| 1 | [Profiling & Experimental Design](01_Profiling_And_Experimental_Design.md) | [Practice](Practice/01_Profiling_And_Experimental_Design.py) |
| 2 | [Object Lifetimes, GC & Memory Measurement](02_Object_Lifetimes_GC_And_Memory_Measurement.md) | [Practice](Practice/02_Object_Lifetimes_GC_And_Memory_Measurement.py) |
| 3 | [Bytecode & Interpreter Behavior](03_Bytecode_And_Interpreter_Behavior.md) | [Practice](Practice/03_Bytecode_And_Interpreter_Behavior.py) |
| 4 | [Descriptors & Class Creation](04_Descriptors_And_Class_Creation.md) | [Practice](Practice/04_Descriptors_And_Class_Creation.py) |
| 5 | [Buffers, Memoryviews & Binary Formats](05_Buffers_Memoryviews_And_Binary_Formats.md) | [Practice](Practice/05_Buffers_Memoryviews_And_Binary_Formats.py) |
| 6 | [Native Interop & Extension Boundaries](06_Native_Interop_And_Extension_Boundaries.md) | [Practice](Practice/06_Native_Interop_And_Extension_Boundaries.py) |
| 7 | [Free Threading & Runtime Assumptions](07_Free_Threading_And_Runtime_Assumptions.md) | [Practice](Practice/07_Free_Threading_And_Runtime_Assumptions.py) |

Continue with the [Measured binary-parser optimization study capstone](../../Capstones/Level_12_Internals_Performance_And_Investigation/README.md).

## Working through this level

Read the detailed explanation, trace the examples, and complete the practice ladder before the independent task. Each file in `Practice/` contains the full task, accepted inputs, and expected behavior as comments. Write your own implementation below those comments. Reference implementations are in `Solutions/`; compare them after an attempt.

Ask the assistant to review your saved submission when ready. Progress is recorded manually after review, including revisions and topics to revisit. Independent-task sections contain only the assignment and its expected behavior.

## Environment and run commands

References target Python 3.13 and mostly its standard library. The native scalar example requires the platform system C library, not a new compiler. Free-threaded experiments require that distinct interpreter build; ordinary execution reports its actual current mode. Record platform and build for every comparison.

## Advancement

Independently investigate unfamiliar runtime behavior, consult versioned primary sources, design reproducible experiments, preserve correctness, and explain observed performance/ownership tradeoffs.

Demonstrate the capstone with its documented normal, boundary, and failure cases and explain one small requirement change. Record evidence in [the Level 12 progress record](../../Progress/Level_12_Internals_Performance_And_Investigation.md). Running a reference does not complete your own submission.

## Scope and next steps

Completing the level means demonstrating independent investigation under stated conditions. It does not require adding every advanced mechanism to one project or asserting unmeasured scaling. Building a new compiled extension is a separate toolchain-dependent extension of the native-boundary lesson.
