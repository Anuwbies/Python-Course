# 🟡 Level 2: Intermediate Capstone Projects

Welcome to the **Level 2 Intermediate Testing Capstones**! These projects test intermediate software engineering practices in Python, including Abstract Base Classes (ABCs), property setters/getters, custom exceptions, magic dunder methods, generators/iterators, function decorators, context managers, type hinting, and testing with `pytest`.

---

## 📚 Available Projects

| Project | Domain | Key Concepts Tested | Difficulty | Specification |
| :--- | :--- | :--- | :---: | :--- |
| **01: Extensible Expense Tracker & Plugin Engine** | Financial Tech / Tooling | ABCs, Custom Exceptions, Dunders (`__iter__`, `__len__`, `__add__`), Decorators, Context Managers | 🟡 Intermediate | [Project 01 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_2_Intermediate/Project_01_CLI_Expense_Tracker_With_Plugins.md) |
| **02: Markdown-to-HTML Static Site Generator** | Web Tooling / Compilers | Generators, File Streaming, Custom Pipeline Decorators, Context Managers, AST-like nodes | 🟡 Intermediate | [Project 02 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_2_Intermediate/Project_02_Markdown_To_HTML_Static_Site_Generator.md) |
| **03: Memory-Efficient Server Log ETL Analyzer** | Data Pipelines / DevOps | Lazy Generator Pipelines (`yield from`), Custom Iterators, Decorator Timing/Metrics, Pytest Suite | 🟡 Intermediate-Hard | [Project 03 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_2_Intermediate/Project_03_Automated_ETL_Log_Analyzer.md) |

---

## 🎯 Learning Evaluation Rubric
When implementing any Level 2 project, ensure your solution satisfies:
- **Design Patterns**: Effective use of Factory, Strategy, and Decorator design patterns.
- **Type Annotations**: Comprehensive type hinting (`typing.Optional`, `typing.Union`, `typing.Generator`, `typing.Callable`).
- **Resource Management**: Safe handling of file handles and locks using custom `@contextmanager` or `__enter__`/`__exit__`.
- **Automated Testing**: 100% test coverage using `pytest` with parameterized tests, fixtures, and exception assertions.
