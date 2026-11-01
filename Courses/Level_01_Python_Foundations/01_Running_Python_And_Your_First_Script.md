# Lesson 1: Running Python & Your First Script

**Prerequisites:** None. **Save your work:** `Practice/01_first_script.py`.

By the end of this lesson, you should be able to save a Python file, run that exact file from a terminal, and distinguish your source code from the output it produces. This is the foundation for every later exercise: an excellent program is not useful if you are accidentally running an older file or entering code into the wrong tool.

## 1. Understand the tools before typing commands

An **editor** is where you write and save source code. VS Code, IDLE, and a plain text editor can all edit Python. A **terminal** is a text interface where you launch programs. On Windows, the terminal may run PowerShell. The **Python interpreter** is the program that reads Python source and executes its instructions.

These tools have different jobs. The editor does not automatically execute every line you type. PowerShell does not interpret ordinary Python expressions as Python. Saving a file writes your changes to disk; running Python asks the interpreter to execute the saved contents.

| Tool or item | Job | Example |
| --- | --- | --- |
| Editor | Create and edit source code | A tab containing `first_program.py` |
| Source file | Store instructions as text | A file whose name ends in `.py` |
| Terminal shell | Launch programs and show their output | PowerShell |
| Python interpreter | Execute Python instructions | The program launched by `python` |
| Program output | Show the results of executed instructions | `Hello, Python!` |

The `.py` extension tells you that a file is intended to contain Python source. Ensure your editor saves it as `first_program.py`, rather than `first_program.py.txt`. A filename is not code: the interpreter needs both the filename and valid contents inside it.

## 2. Find an available Python interpreter

Open the terminal in the repository's main folder, the folder containing `Courses` and `Capstones`. Ask Python to report its version:

```powershell
python --version
```

This course's reference work is checked with Python 3.13. The Level 1 syntax also works on many other Python 3 versions; use Python 3 rather than Python 2. If Windows cannot find `python`, try:

```powershell
py --version
```

If `py` works, use `py` wherever the course commands show `python`. If neither is available, install Python from [python.org](https://www.python.org/downloads/) and reopen your terminal. You do not need third-party packages or a virtual environment for this level.

In VS Code, select the same Python interpreter for the editor that you use in the terminal. Later you may have several interpreters installed; keeping them consistent prevents confusing differences between editor behavior and terminal behavior.

## 3. Save your first instructions

Open `Courses/Level_01_Python_Foundations/Practice/01_first_script.py`. Add these statements below the task comments:

```python
print("Hello, Python!")
print("I can run a saved script.")
```

For now, read `print(...)` as an instruction to display something. The quotation marks identify text in the program; they are not part of the displayed text. The parentheses contain the value you want to display. Lesson 2 explains this instruction more carefully.

Save the file. Then run it from the repository root:

```powershell
python Courses/Level_01_Python_Foundations/Practice/01_first_script.py
```

You should see:

```text
Hello, Python!
I can run a saved script.
```

Python executes these two statements in order. The second statement does not replace the first line; it produces another line after it. When the script finishes, the terminal returns to its normal prompt so you can launch another command.

## 4. Distinguish a script from the interactive interpreter

Running `python` without a filename usually opens an interactive Python session. Its prompt looks like `>>>`. In that session, you enter Python statements directly. Do not copy the `>>>` prompt into a `.py` file; the prompt is an interface marker, not part of the source code.

An interactive session is useful for quick experiments, but saved scripts preserve your work and can be rerun. This course uses saved scripts for submitted tasks. To leave an interactive Python session, enter `exit()`, then run your file at the normal shell prompt.

| What you see | Where you are | What to enter |
| --- | --- | --- |
| A PowerShell prompt with a folder path | Terminal shell | `python path/to/file.py` |
| `>>>` | Python interactive session | Python statements |
| An editor tab with a filename | Source editor | Saved source code |

Do not enter `python first_program.py` inside a Python source file. It is a shell command for launching a program, not a Python statement.

## 5. File paths and the current working directory

The terminal has a **current working directory**, meaning the folder from which relative paths are interpreted. In PowerShell, `Get-Location` shows that directory. A command such as `python Practice/01_first_script.py` works only if the current directory contains that `Practice` folder.

The longer course commands begin with `Courses/...` because they assume you are at the repository root. If you are already inside the lesson's directory, the same file is reached through the shorter path `Practice/01_first_script.py`. Both can identify the same saved file from different starting points.

If a directory name contains spaces, quote the path when entering a command. Keep the supplied practice filenames while working through this edition so the lesson links and progress records identify the correct saved attempt.

## 6. Diagnose the first common problems

**The command is not recognized:** the shell could not find an interpreter using that command name. This happens before your script runs. Try the available interpreter command and check your installation.

**Python cannot open the file:** the interpreter started, but the path does not identify an existing file. Inspect the working directory, spelling, and file extension. Changing the source code will not fix a wrong filename in the launch command.

**Old output appears:** save the file and confirm that you are running the same path you edited. Two tabs with similar names can refer to different files.

**An error points to a line in the file:** Python found the file but could not execute its contents successfully. Read the message and inspect the indicated line. Lesson 2 introduces simple error diagnosis.

Reference: [Using Python on Windows](https://docs.python.org/3.13/using/windows.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Write the two expected output lines before running the example. Does the output contain quotation marks?
2. **Explain:** Describe the sequence “edit → save → launch → output” in your own words. Identify the tool responsible for each step.
3. **Modify:** In a separate scratch file, change the greeting to include your name. Save and rerun it. Explain why changing the editor without saving may leave the old output.
4. **Debug:** A learner saved `first_program.py` in `Practice/` but ran `python first_program.py` from the repository root. Explain how to correct the path.

<details>
<summary>Hints</summary>

The quote characters mark text in the source. The launch command needs a path starting from the terminal's working directory. A saved file and an unsaved editor tab are not necessarily identical.

</details>

## Independent task: first script

In `Practice/01_first_script.py`, write a program that uses two separate `print()` calls to display these lines in this order:

```text
Hello, Python!
I can run a saved script.
```
