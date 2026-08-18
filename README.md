# 🐍 Python Mastery Curriculum: Zero to Expert

Welcome to the **Complete Python Mastery Course** repository! This repository contains a structured, 5-tiered curriculum taking students from their very first line of code to CPython internals, async systems architecture, and production engineering.

---

## 🧭 Course Roadmap

| Level | Course Track | Scope & Key Topics | Core Capstone Project | Additional Capstones | Guide Directory |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01** | 🟢 **Beginner (1st Year / CS101)** | Variables, I/O, Operators, Conditionals, Loops, Lists, Dicts, Functions, File I/O, OOP Basics | [Banking System CLI](Courses/Level_1_Beginner/README.md) | [3 Projects](Capstones/Level_1_Beginner/README.md) | [`Courses/Level_1_Beginner`](Courses/Level_1_Beginner/) |
| **02** | 🟡 **Intermediate (Software Craftsmanship)** | Advanced OOP, MRO, `@property`, Dunders, ABCs, Custom Exceptions, Generators, Decorators, Context Managers, `pytest` | [Task & Plugin Engine](Courses/Level_2_Intermediate/README.md) | [3 Projects](Capstones/Level_2_Intermediate/README.md) | [`Courses/Level_2_Intermediate`](Courses/Level_2_Intermediate/) |
| **03** | 🟠 **Advanced (Algorithms & Concurrency)** | Big-O, Custom Trees/Heaps/Graphs, BFS/DFS, Dijkstra, Threading (GIL), Multiprocessing, `asyncio` | [Async Crawler & Indexer](Courses/Level_3_Advanced/README.md) | [3 Projects](Capstones/Level_3_Advanced/README.md) | [`Courses/Level_3_Advanced`](Courses/Level_3_Advanced/) |
| **04** | 🔵 **Professional (Backend Systems)** | FastAPI, Pydantic v2, PostgreSQL, SQLAlchemy 2.0 Async, Alembic, JWT Auth, Celery/Redis, Docker, CI/CD | [E-Commerce Microservice](Courses/Level_4_Professional/README.md) | [3 Projects](Capstones/Level_4_Professional/README.md) | [`Courses/Level_4_Professional`](Courses/Level_4_Professional/) |
| **05** | 🟣 **Expert (CPython Internals & Performance)** | CPython VM Bytecode, `PyObject`, Generational GC tuning, Metaclasses, `memoryview`, Cython/C-Bindings, No-GIL Python 3.13 | [In-Memory Redis Engine](Courses/Level_5_Expert/README.md) | [3 Projects](Capstones/Level_5_Expert/README.md) | [`Courses/Level_5_Expert`](Courses/Level_5_Expert/) |

---

## 📂 Repository Structure

```text
.
├── README.md                            <- Master Course Overview
├── Courses/                             <- In-depth Markdown Lesson Guides
│   ├── README.md                        <- Master Progress Tracker
│   ├── Level_1_Beginner/                <- Lessons 01 - 10 + Quizzes & Solutions
│   ├── Level_2_Intermediate/            <- Lessons 01 - 08 + Quizzes & Solutions
│   ├── Level_3_Advanced/                <- Lessons 01 - 08 + Quizzes & Solutions
│   ├── Level_4_Professional/            <- Lessons 01 - 08 + Quizzes & Solutions
│   └── Level_5_Expert/                  <- Lessons 01 - 08 + Quizzes & Solutions
├── Capstones/                           <- Multi-Domain Capstone Project Hub
│   ├── README.md                        <- Master Capstones Project Matrix
│   ├── Level_1_Beginner/                <- 3 Comprehensive Beginner Capstone Projects
│   ├── Level_2_Intermediate/            <- 3 Comprehensive Intermediate Capstone Projects
│   ├── Level_3_Advanced/                <- 3 Comprehensive Advanced Capstone Projects
│   ├── Level_4_Professional/            <- 3 Comprehensive Professional Capstone Projects
│   └── Level_5_Expert/                  <- 3 Comprehensive Expert Capstone Projects
└── Testing/                             <- Interactive Coding Practice Files
    ├── Level_1_Beginner/
    ├── Level_2_Intermediate/
    ├── Level_3_Advanced/
    ├── Level_4_Professional/
    └── Level_5_Expert/
```

---

## 💡 How to Use This Course
1. Read the lesson guide inside the [`Courses/`](Courses/) folder (e.g. `Courses/Level_1_Beginner/01_Variables_And_Data_Types.md`).
2. Open the corresponding `.py` file inside [`Testing/`](Testing/) (e.g. `Testing/Level_1_Beginner/Lesson_01_Variables_And_Data_Types.py`) to write and run your code.
3. Check your understanding using the built-in quizzes and expandable exercise solutions!
4. Explore and build extra real-world projects in the [`Capstones/`](Capstones/) folder to test your mastery across diverse software domains.
