# Lesson 5: Modules, Imports & Entry Points

**Prerequisites:** Levels 1–2 and Lessons 1–4 of this level. **Practice file:** `Practice/05_Modules_Imports_And_Entry_Points.py`.

Split reusable calculations from the program that launches them. A module is a saved Python file with its own namespace; importing it makes names available but also executes its top-level statements.

## 1. Import a definition rather than copy it

Suppose `budget_tools.py` contains a function named remaining. A neighboring script can use `from budget_tools import remaining` and call it normally. Python loads the module, executes its definitions, and binds the selected name in the importing file.

```python
# The content of budget_tools.py:
def remaining(budget, spent):
    return budget - spent
```

Copying the same calculation into several files creates multiple places to fix. A reusable module makes the relationship explicit. Its filename should not hide a standard-library module such as `json.py`, because import lookup could then load the wrong file.

## 2. Understand namespaces and search paths

`import budget_tools` binds the module name, so the caller uses `budget_tools.remaining(...)`. `from budget_tools import remaining` binds the function directly. Both can work; choose the form that makes the source of a name clear.

For a directly launched script, its directory is normally included in the module search path. The task therefore places its two files next to one another. Importing a module by a filesystem path string is a different operation and is not what an ordinary import statement does.

## 3. Avoid launching a demonstration during import

When imported, a module's top-level print or input runs too. Place a launch-only demonstration under `if __name__ == "__main__":`. Python sets that special name to `"__main__"` for a directly launched script and to the module name when imported.

```python
def remaining(budget, spent):
    return budget - spent

if __name__ == "__main__":
    print(remaining(500, 250))
```

The guard does not stop definitions from being available. It selects whether the demonstration runs. This allows a later test or API to import the function without triggering interactive prompts.

## 4. Keep module boundaries understandable

Put calculations in the reusable file and input/output in the entry script. Avoid circular imports where each file needs the other to finish loading. For the small tracker, the launcher depends on the calculation module; the calculation module has no reason to import the launcher.

Python caches imported modules within a process. Repeating an ordinary import does not normally rerun all top-level code. While developing, restart the script when comparing saved versions rather than assuming an old interactive session has automatically reloaded changes.

References: [Python modules](https://docs.python.org/3.13/tutorial/modules.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether a guarded demonstration runs on import.
2. **Explain:** Explain the difference between a module-qualified name and a directly imported function.
3. **Modify:** Move an input prompt out of a reusable module and into its launcher.
4. **Debug:** Find a local filename that shadows a standard-library module.

<details>
<summary>Hints</summary>

Keep the reusable function and the entry script in the same Practice directory.

</details>

## Independent task: modules, imports & entry points

In `Practice/05_Modules_Imports_And_Entry_Points.py`, complete this task:

Create a neighboring `budget_tools.py` defining `remaining(budget, spent)` as budget minus spent, with no import-time output. In this task's script, import that function and display its result for 500 and 250. Put the demonstration under an entry-point guard.

Expected output:

```text
250
```
