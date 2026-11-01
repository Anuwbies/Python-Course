# Lesson 6: Command-Line Interfaces & Packaging

**Prerequisites:** Levels 1–4 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Command_Line_Interfaces_And_Packaging.py`.

Give a project an explicit launch interface and installation description. A reusable module, a command-line entry point, and packaging metadata solve related but different problems.

## 1. Parse named options

Argparse is a standard-library command-line parser. ArgumentParser creates the parser object; add_argument declares accepted options; parse_args converts an argument list into named attributes. Accessing args.budget reads the parsed budget field.

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--budget", type=int, required=True)
args = parser.parse_args(["--budget", "500"])
print(args.budget)  # 500
```

Supplying a list makes this example independent of the shell. In an actual launcher, parse_args() reads the process arguments. A type converter such as int checks text syntax, while range validation remains the application's responsibility.

## 2. Make a callable launcher

Define `main(argv=None)` so ordinary execution can read real process arguments while tests can pass a controlled list. Keep the entry-point guard at the bottom. Return an exit status where useful; `raise SystemExit(main())` makes that status visible to the shell.

An error status is part of the interface. Printing an error and exiting successfully can mislead a script or CI job that relies on the process status. Argparse's error method reports usage and exits unsuccessfully for invalid command arguments.

## 3. Describe installation with pyproject.toml

A pyproject file can declare the build backend, project name, supported Python version, dependencies, and console-script entry points. A script mapping such as `expense-report = "project:main"` asks installation tooling to expose a command calling main in the project module.

That mapping is not a filesystem path to execute. The module must actually be packaged and importable. Keep a small module list explicit for a flat learning project; larger package layouts can use a dedicated source directory and package discovery.

## 4. Document the complete command

Include the working directory, interpreter or environment, required input format, and expected failure behavior. An installable project is not automatically a published project, and a local editable installation does not upload to a package index.

Do not add packaging complexity merely to make a small experiment look professional. Here the purpose is to let another person install and launch a known interface without editing the source file or guessing which function to call.

## Positional paths and concrete package metadata

`parser.add_argument("path", type=Path)` declares a required positional path; import Path from pathlib. `--budget` is a named option because its declaration starts with dashes. `choices=["reader", "admin"]` can restrict a text option to an explicit set. Neither type=Path nor parsing alone opens the file. Catch file/validation failures around the real load and call parser.error with their message when the CLI should exit unsuccessfully.

This minimal TOML packages one neighboring report.py module and exposes its main function:

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "classroom-report"
version = "0.1.0"
requires-python = ">=3.13"

[project.scripts]
classroom-report = "report:main"

[tool.setuptools]
py-modules = ["report"]
```

TOML sections group settings; strings use quotes, and lists use brackets. The build-system section names the tool used to build/install; project identifies this distribution; project.scripts maps a shell command to an importable module and callable. From that folder, `python -m pip install -e .` makes an editable local installation. Adapt the module and command names together when moving this pattern to another project. Installing it does not publish it.

References: [Argparse](https://docs.python.org/3.13/library/argparse.html), [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the parsed value for the explicit argument list in the example.
2. **Explain:** Explain how main(argv) makes launch behavior reproducible.
3. **Modify:** Add a days option and reject a nonpositive value.
4. **Debug:** Find a console-script mapping that points to a filename instead of a module and callable.

<details>
<summary>Hints</summary>

A named option's type converter does not establish its allowed numeric range.

</details>

## Independent task: command-line interfaces & packaging

In `Practice/06_Command_Line_Interfaces_And_Packaging.py`, complete this task:

Define `main(argv=None)` using argparse with required integer options `--budget` and `--days`. Reject negative budget or nonpositive days through parser.error. Print the whole-unit daily allowance. In the guarded demonstration call main with `['--budget', '500', '--days', '5']` so the supplied script runs without extra shell arguments.

Expected output:

```text
100
```
