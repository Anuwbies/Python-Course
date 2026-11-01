# Lesson 1: Environments, Dependencies & Git

**Prerequisites:** Levels 1–4. **Practice file:** `Practice/01_Environments_Dependencies_And_Git.py`.

Make a project reproducible by separating its interpreter, installed dependencies, source files, and saved history. A working program on one machine is only the beginning of a usable project.

## 1. Know which interpreter is running

`sys.executable` identifies the launched interpreter. `sys.prefix` identifies its environment prefix, while `sys.base_prefix` normally identifies the underlying installation. In a conventional venv they differ. These values describe the running process, not the interpreter currently selected in another editor tab.

```python
import sys
print(sys.version_info.major)
print(sys.executable)
```

A module import uses this interpreter's search path. Installing a package for a different interpreter does not make it available automatically. Use `python -m pip` with the same interpreter you use to run the project.

## 2. Isolate third-party packages

From the repository root, create a project environment inside the course folder:

```powershell
python -m venv Courses/Level_05_Practical_Software_Development/.venv
Courses/Level_05_Practical_Software_Development/.venv/Scripts/python.exe -m pip install pytest
```

Calling that interpreter directly avoids relying on PowerShell activation. On Unix-like systems the environment interpreter is under bin/python instead of Scripts/python.exe. Select the same environment in your editor. A virtual environment isolates Python packages; it is not a security sandbox for untrusted code.

## 3. Record direct dependencies and project boundaries

A requirements file describes package constraints that can be installed with `-m pip install -r path/to/requirements.txt`. Compatibility ranges communicate supported versions; a lock or fully resolved snapshot is needed when reproducing an exact environment. Record the interpreter version too.

Keep reusable source, tests, input samples, and generated output distinguishable. Avoid committing virtual environments and credentials. A clean project should explain the working directory for its commands rather than assuming the reader happens to be in the author's folder.

## 4. Save meaningful versions with Git

`git status --short` shows changed paths and `git diff -- path` shows unstaged content changes for a selected file. Stage the intended source with `git add -- path`, then create a local commit with an informative message. A commit records staged changes; it does not publish to a remote service.

Before a commit, inspect exactly what is staged. A broad add can include generated files or unrelated edits. When a bug appears, a small meaningful history helps locate the change that introduced it. Git is a record of source evolution, not a replacement for demonstrating correct behavior.

References: [Virtual environments](https://docs.python.org/3.13/tutorial/venv.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict which interpreter pip targets when invoked with an explicit environment path.
2. **Explain:** Explain why a successful import in another terminal does not establish this environment's dependencies.
3. **Modify:** Record one direct dependency and its compatible range.
4. **Debug:** Find an editor/terminal interpreter mismatch using sys.executable.

<details>
<summary>Hints</summary>

The environment prefix comparison should use the running process, not a guessed folder name.

</details>

## Independent task: environments, dependencies & git

In `Practice/01_Environments_Dependencies_And_Git.py`, complete this task:

Write `environment_info()` returning a dictionary with `python_major`, `executable`, and `is_venv`, using the current sys module values. Print each field as a labeled line in a guarded demonstration. Run the file with your project environment's interpreter.

Expected behavior: python_major is 3; executable identifies the interpreter actually used; is_venv is True in a conventional venv and False in a base installation. Paths are machine-dependent. The function must inspect the process rather than hardcode these values.
