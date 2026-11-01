# Lesson 1: Paths, Text Files & With

**Prerequisites:** Levels 1–3. **Practice file:** `Practice/01_Paths_Text_Files_And_With.py`.

Persist a value outside the running process and recover it deliberately. A path identifies a location; opening that location creates a resource with an access mode and an encoding.

## 1. Identify the location

`Path` from pathlib represents a filesystem path. Joining with `/` builds a child path using the platform's conventions. A relative path starts from the process's working directory, not automatically from the source file's directory.

```python
from pathlib import Path

folder = Path("data")
file_path = folder / "notes.txt"
print(file_path.name)  # notes.txt
```

Creating a Path does not create a directory or file. `folder.mkdir(parents=True, exist_ok=True)` creates directories when appropriate. `exists()` and `is_file()` answer different questions: a location can exist as a directory rather than a regular file. A pre-check does not guarantee a later open succeeds, because permissions or state can change between operations.

## 2. Open text with an explicit encoding

`open(path, "w", encoding="utf-8")` opens a text file for writing and replaces existing contents. Its handle has a write method that accepts strings. Reading with the same encoding reconstructs text from the stored bytes.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "note.txt"
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("Study café")
    with open(path, "r", encoding="utf-8") as handle:
        print(handle.read())
```

`with` enters a resource's managed block and arranges cleanup on exit, including when a statement raises an exception. For a file this closes the handle. The outer TemporaryDirectory is a standard-library demonstration fixture: it creates an isolated directory and removes its contents on block exit. It is not an expense-file format or application feature.

## 3. Separate contents and presentation

Writing text does not add a newline automatically. Include `"\n"` when the file format requires one. Printing the returned contents can add another newline, so inspect whether a blank output line comes from the file or the display call.

A file handle's read method returns text in text mode. Binary mode returns bytes and is a different interface; do not mix arbitrary binary data with a text encoding. Unicode names are a useful manual case because ASCII-only examples can hide an encoding mismatch.

## 4. Define effects at the interface

A writing function should state whether it overwrites or appends, whether parent directories must already exist, and what happens on failure. A reading function can return the contents without printing so the caller chooses its use.

Closing and flushing a buffered file is not the same as a guarantee that data survives sudden power loss. This lesson teaches correct resource lifetime and ordinary read/write behavior. Later in the level, a temporary replacement avoids truncating a known-good file before the new content is ready.

## Path helpers and the source file's location

`path.open(mode, encoding="utf-8")` opens that Path just like `open(path, ...)`. For a small complete text value, `path.write_text(text, encoding="utf-8")` writes and closes the file; `path.read_text(encoding="utf-8")` reads and closes it. They still overwrite or fail according to filesystem rules. Use a handle and a with block when the task specifically requests one or when processing lines incrementally.

In a saved script, `__file__` identifies that source file. `Path(__file__).resolve()` obtains its absolute resolved path. `.parent` is its containing directory; `.parents[0]` is also that directory and `.parents[1]` is one directory higher. `.with_name("sample.txt")` changes only the final name to locate a sibling. `.as_posix()` renders a path with forward slashes, useful when building a SQLite URL later. These operations identify locations; they do not read the files. Keep a caller-supplied data path separate from a source-relative bundled asset path.

References: [Reading and writing files](https://docs.python.org/3.13/tutorial/inputoutput.html#reading-and-writing-files), [Pathlib](https://docs.python.org/3.13/library/pathlib.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict whether creating a Path alone creates a file.
2. **Explain:** Explain why encoding belongs on both the write and read operations.
3. **Modify:** Round-trip a name containing an accent and a trailing newline.
4. **Debug:** Locate a relative path being interpreted from the wrong working directory.

<details>
<summary>Hints</summary>

Exit the write block before reopening the same path to read.

</details>

## Independent task: paths, text files & with

In `Practice/01_Paths_Text_Files_And_With.py`, complete this task:

Define `write_note(path, text)` to overwrite a UTF-8 text file and return None, and `read_note(path)` to return its text without printing. The parent directory already exists. Demonstrate writing and reading `Study café` in a TemporaryDirectory, then print the returned text. Use with statements for the handles.

Expected output:

```text
Study café
```
