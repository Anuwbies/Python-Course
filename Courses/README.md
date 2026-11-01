# Python: Beginner to Expert

This twelve-level course progresses from a first saved script to independent investigation of Python systems and performance. All twelve levels now have detailed lessons, cumulative practice tasks, separate reference implementations, and a capstone. The course contains 79 lessons and twelve capstones.

Start with [Level 1: Python Foundations](Level_01_Python_Foundations/README.md). Lessons live in `Courses/`, projects in `Capstones/`, and manual progression in the top-level `Progress/` folder. The [environment and run guide](Environment_And_Run_Guide.md) explains interpreters, dependencies, and the scope of reference execution.

## Reading order

| Level | Stage and focus | Lessons | Material | Student record |
| --- | --- | --- | --- | --- |
| 01 | Beginner: Python Foundations | 8 | [Lessons](Level_01_Python_Foundations/README.md) | [Progress](../Progress/Level_01_Python_Foundations.md) |
| 02 | Beginner: Control Flow & Collections | 7 | [Lessons](Level_02_Control_Flow_And_Collections/README.md) | [Progress](../Progress/Level_02_Control_Flow_And_Collections.md) |
| 03 | Beginner: Functions, Scope & Modules | 6 | [Lessons](Level_03_Functions_Scope_And_Modules/README.md) | [Progress](../Progress/Level_03_Functions_Scope_And_Modules.md) |
| 04 | Beginner: Files, Exceptions & Persistent Data | 6 | [Lessons](Level_04_Files_Exceptions_And_Persistent_Data/README.md) | [Progress](../Progress/Level_04_Files_Exceptions_And_Persistent_Data.md) |
| 05 | Intermediate: Practical Software Development | 6 | [Lessons](Level_05_Practical_Software_Development/README.md) | [Progress](../Progress/Level_05_Practical_Software_Development.md) |
| 06 | Intermediate: Object-Oriented Programming & Design | 6 | [Lessons](Level_06_Object_Oriented_Programming_And_Design/README.md) | [Progress](../Progress/Level_06_Object_Oriented_Programming_And_Design.md) |
| 07 | Intermediate: Idiomatic & Reusable Python | 6 | [Lessons](Level_07_Idiomatic_And_Reusable_Python/README.md) | [Progress](../Progress/Level_07_Idiomatic_And_Reusable_Python.md) |
| 08 | Advanced: Algorithms & Data Structures | 7 | [Lessons](Level_08_Algorithms_And_Data_Structures/README.md) | [Progress](../Progress/Level_08_Algorithms_And_Data_Structures.md) |
| 09 | Advanced: Concurrency & Async | 6 | [Lessons](Level_09_Concurrency_And_Async/README.md) | [Progress](../Progress/Level_09_Concurrency_And_Async.md) |
| 10 | Professional: Backend Development & Databases | 7 | [Lessons](Level_10_Backend_Development_And_Databases/README.md) | [Progress](../Progress/Level_10_Backend_Development_And_Databases.md) |
| 11 | Professional: Production Engineering | 7 | [Lessons](Level_11_Production_Engineering/README.md) | [Progress](../Progress/Level_11_Production_Engineering.md) |
| 12 | Expert: Internals, Performance & Investigation | 7 | [Lessons](Level_12_Internals_Performance_And_Investigation/README.md) | [Progress](../Progress/Level_12_Internals_Performance_And_Investigation.md) |

Levels 1–9 build the general language and development foundations. Level 10 specializes in backend development, followed by Level 11's deployment and operations work. Level 12's internals/performance investigation requires the general foundations; backend/operations experience is helpful but not mandatory for its independent parser study.

## How lessons are organized

Read the detailed explanation and trace the examples. Work through predict/explain/modify/debug practice, then implement the independent task. That task section contains only its assignment, accepted inputs, requirements, and expected behavior.

Every Python file in `Practice/` carries its complete task as comments, so you can work directly in the file. Write your implementation below those comments. There are no TODO markers, fixed-question quizzes, or automatic course graders. Reference code is in `Solutions/`; neither directory needs a README. Some systems tasks also supply configuration assets and companion source files with their own embedded tasks.

Tasks use the current lesson and earlier material. Prerequisites and scope are stated explicitly; later-level concepts should not be necessary to complete an earlier task. Expected output is exact for deterministic examples. Timings, IDs, interpreter details, and external-service outcomes are described as observed behavior when a fixed transcript would be misleading.

Ask the assistant to review your saved work when ready. Review focuses on the real implementation, its normal/boundary/failure behavior, and your explanation of a small change. Record the outcome manually in [Progress](../Progress/README.md). Curriculum availability does not mark any student work complete.

## Capstones

Each level requires one [capstone](../Capstones/README.md). Early projects build a calculator, tracker, reusable functions, and persistence. Later projects cover installable tools, object models, pipelines, search, concurrency, databases, deployment, and measured optimization.

The API and deployment references include real requests, database operations, and migration files. Docker-dependent behavior must be demonstrated with actual containers. A printed status is not evidence of a running service; in-process tests and isolated adapters have explicitly stated limits.

See [concept progression and task prerequisites](Concept_Progression.md) for the cumulative boundaries of each level and capstone.
