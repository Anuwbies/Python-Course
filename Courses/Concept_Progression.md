# Concept progression and task prerequisites

Read the numbered lessons in order. Each independent task uses the current lesson and earlier required lessons; its practice file contains the complete task. Complete the level's lessons before its capstone. Reference solutions follow the same concept boundary.

Levels 1–11 form a cumulative sequence. Level 12 requires Levels 1–9 plus its own lessons; the backend and deployment levels are optional for its runtime investigation. Platform-dependent exercises retain their stated environment requirements.

| Level | Concepts taught before its capstone | Capstone boundary |
| --- | --- | --- |
| [1](Level_01_Python_Foundations/README.md) | Straight-line statements, values, arithmetic, strings, conversion and display | A valid-input calculator; no conditions, loops, functions, or imports |
| [2](Level_02_Control_Flow_And_Collections/README.md) | Comparisons, branches, loops, sequence operations, sets/dictionaries and aggregation | A menu and in-memory grouped history; numeric text is assumed valid |
| [3](Level_03_Functions_Scope_And_Modules/README.md) | Functions, contracts, scope/copying, assertions, imports and entry-point guards | Reusable transformations preserving caller data |
| [4](Level_04_Files_Exceptions_And_Persistent_Data/README.md) | Paths/UTF-8, file APIs, exceptions, JSON/CSV validation, cleanup and replacement | A validated versioned JSON store with safe single-writer replacement |
| [5](Level_05_Practical_Software_Development/README.md) | Environments, logging, pytest/fixtures, annotations, argparse and packaging | An installable CLI with isolated behavioral tests |
| [6](Level_06_Object_Oriented_Programming_And_Design/README.md) | Classes, invariants, composition, abstract interfaces, properties and dataclasses | An in-memory catalog/borrowing model with explicit ownership |
| [7](Level_07_Idiomatic_And_Reusable_Python/README.md) | Comprehensions, callables, flexible signatures, generators, wrappers and context managers | A managed lazy parser with source errors and a completed-call counter |
| [8](Level_08_Algorithms_And_Data_Structures/README.md) | Cost models, timing trials, recursion, stacks/queues, search, heaps and graph paths | Equivalent scan/index query contracts with actual measured durations |
| [9](Level_09_Concurrency_And_Async/README.md) | Threads/locks, processes/futures, coroutines, timeouts, TaskGroup and bounded queues | Fixed workers processing real files with explicit errors and cancellation ownership |
| [10](Level_10_Backend_Development_And_Databases/README.md) | Typed HTTP contracts, SQL/transactions, ORM/session APIs, revision setup and integration tests | A persistent API with real migration history and schema readiness |
| [11](Level_11_Production_Engineering/README.md) | Validated configuration, token APIs/dependencies, deployment clients, durable locking/savepoints, caches, CI and observation | A composed operational service using mechanisms already demonstrated in the lessons |
| [12](Level_12_Internals_Performance_And_Investigation/README.md) | Profiling, object lifetime/tracing, code inspection, descriptors, binary/native boundaries and runtime probes | Equivalent binary parsers with measured timing/memory and documented environment |

When extending a task, first teach any new operation in the preceding explanation with its input, result, side effects, and failure behavior. Naming a library or linking its documentation alone is not an introduction to a required API. Keep task contracts explicit about accepted types, empty cases, ordering, mutation, and errors.

Operational configuration files supplied as scaffolding are explained in the relevant lessons. Local SQLite/cache-adapter tests establish those local contracts; real PostgreSQL locking, Redis expiration/network behavior, container recovery, and a free-threaded interpreter require their stated environments.
