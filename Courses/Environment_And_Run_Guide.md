# Environment and run guide

Use the interpreter and dependencies for the level you are studying. Each lesson and practice file states the task; this guide explains how to run saved work and records the limits of the supplied reference runs.

## Standard-library levels

Levels 1–4 and 6–9 use Python's standard library. Level 12 also uses the standard library, with a platform system C library for its native-interop exercise. The examples target Python 3.13; implementation-specific material uses the versioned 3.13 documentation.

From the repository root, run a saved file by its path:

```powershell
python Courses/Level_02_Control_Flow_And_Collections/Practice/01_Comparisons_And_Boolean_Logic.py
```

If Windows provides `py` instead of `python`, substitute that command. Save changes before running. Keep module companions beside their entry scripts, and run multiprocessing examples as files with their main guards. Async launchers own their event loop through `asyncio.run`; they should not be nested inside an already running notebook loop.

Practice files begin with task comments and no completed implementation. Write your program below the comments, then ask the assistant to review that saved file when ready.

## Third-party dependencies

Levels 5, 10, and 11 supply `requirements.txt`. Create a project environment inside the relevant course or capstone folder, then install with that environment's interpreter. For example, from the repository root:

```powershell
python -m venv Courses/Level_10_Backend_Development_And_Databases/.venv
Courses/Level_10_Backend_Development_And_Databases/.venv/Scripts/python.exe -m pip install -r Courses/Level_10_Backend_Development_And_Databases/requirements.txt
```

Use that same interpreter to run the level's saved files. On Unix-like systems the environment's interpreter is `bin/python` rather than `Scripts/python.exe`. Direct interpreter paths avoid requiring PowerShell activation-policy changes.

Requirements express compatibility ranges, not a complete resolved lockfile. For exact reproduction, record the interpreter, platform, and resolved package versions from the environment actually used. Avoid installing unrelated project stacks into your base interpreter.

## Tests as course material

Testing lessons teach how to write and run tests against real application behavior. They are not automatic course graders. A practice test file remains unfinished until you implement its task.

For a teaching file with a lesson-number filename, name it explicitly:

```powershell
python -m pytest Courses/Level_05_Practical_Software_Development/Practice/03_Pytest_And_Behavior_Cases.py
```

Use the appropriate environment interpreter in place of `python`. For capstone `test_project.py`, run pytest from that capstone's `Practice` directory after completing the implementation. Its adjacent `project.py` is then the intended application import. Run reference tests separately from their corresponding `Solutions` directory; do not combine several unrelated `project` modules into one pytest collection.

Passing a reference suite establishes only its stated behavior and environment. It does not mark student progress complete or establish a coverage percentage. Ask for a review of your own saved work, and record the result in [Progress](../Progress/README.md).

## Reference execution environment

The local references were exercised on Windows with CPython 3.13.5. The testing/backend environment used these resolved versions:

| Package | Version |
| --- | --- |
| pytest | 9.2.0 |
| FastAPI | 0.162.0 |
| Pydantic | 2.14.2 |
| HTTPX (older TestClient compatibility) | 0.28.1 |
| HTTPX2 (current TestClient transport) | 2.16.0 |
| SQLAlchemy | 2.0.55 |
| Alembic | 1.20.1 |
| Uvicorn | 0.54.0 |
| PyJWT | 2.15.1 |
| pwdlib | 0.3.1 |
| redis client | 6.4.0 |
| psycopg | 3.3.6 |

The local execution covered the lesson references, SQLite persistence and migrations, in-process HTTP behavior, teaching tests, thread/process/async examples, the system-C-library call, and measured parser experiments. Hardware-dependent timings and memory sizes are observations rather than fixed expected values.

Docker is unavailable on this authoring machine. The Compose configurations and real-service run instructions are supplied, but live PostgreSQL/Redis container behavior, multiworker PostgreSQL locking, and backup/restore procedures still require execution on a Docker-capable machine. The deployment's local tests explicitly use SQLite and a named isolated cache adapter; they do not establish Redis networking or TTL behavior.

The current interpreter is a conventional GIL-enabled build. The runtime-observation exercise runs on it, but free-threaded compatibility and scaling require a separately identified free-threaded interpreter. The native-interop lesson binds an existing system library; it does not claim to compile a new extension module.

## Operational projects

Follow each capstone's working-directory and environment instructions. Run migrations before serving the database API. Generate signing keys locally, keep them out of committed files and logs, and use the operator issuer only in its intended learning deployment.

The Level 11 `ci.yml` is a template kept inside the capstone folder. It is not an activated remote workflow. Docker runtime outcomes, deployment outcomes, and remote CI results should be recorded only after those actual operations occur.
