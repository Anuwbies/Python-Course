# Lesson 2: Modes, Streaming & Line Formats

**Prerequisites:** Levels 1–3 and Lesson 1 of this level. **Practice file:** `Practice/02_Modes_Streaming_And_Line_Formats.py`.

Choose a file mode that matches the intended change and process records without accidentally confusing blank lines with end-of-file. Line-oriented text is a small explicit format, not arbitrary text parsing.

## 1. Choose the access contract

Mode `r` reads an existing file, `w` replaces contents or creates a file, `a` appends at the end or creates a file, and `x` creates a new file but fails if it already exists. Opening with w can truncate the old file before your first write, so validate the intended data before choosing it.

Appending does not insert a missing line break for you. If an existing file ends in `120` without a newline, appending `80\n` produces `12080`, not two records. A line format should require each record to end with a newline, including records written by your own append function.

## 2. Iterate over lines

A file handle is iterable. A for loop visits its text lines and avoids allocating the entire raw file as one string. `enumerate(handle, start=1)` supplies a line number and line together, allowing an error message to identify the source position.

```python
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "amounts.txt"
    path.write_text("120\n\n80\n", encoding="utf-8")
    with path.open("r", encoding="utf-8") as handle:
        for number, raw in enumerate(handle, start=1):
            text = raw.strip()
            if text:
                print(number, text)
```

This visits the blank line too, but the explicit condition skips its display. Returning a list of all parsed values still stores that list in memory; streaming the input does not make every downstream operation bounded in memory automatically.

## 3. Give blank records a meaning

For this lesson's amount format, surrounding whitespace is ignored and blank lines are skipped. Each other line contains one nonnegative integer. A different format could treat blank records as corruption; choose the rule before implementing it.

`readline()` returns an empty string at end-of-file, while a blank line usually contains a newline character. Stripping both before testing can erase that distinction in a manually controlled loop. Iterating the handle avoids needing a separate end-of-file sentinel.

## 4. Keep reading and aggregation separate

A loader can return a list of parsed amounts; an existing total function can then aggregate it. Alternatively, a streaming total can accumulate directly without storing the full list. Pick based on whether the caller needs history or only a total.

At this point malformed numeric text raises ValueError rather than being silently dropped. The next lesson teaches how to handle that failure while preserving an honest distinction between no data and unreadable data.

References: [Reading and writing files](https://docs.python.org/3.13/tutorial/inputoutput.html#reading-and-writing-files), [Pathlib](https://docs.python.org/3.13/library/pathlib.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the line numbers displayed when the second line is blank.
2. **Explain:** Explain why append must preserve the newline convention.
3. **Modify:** Calculate a streaming total without keeping the entire result list.
4. **Debug:** Fix an append operation that joins two numeric records into one line.

<details>
<summary>Hints</summary>

Add a newline to every appended record, and keep file input order.

</details>

## Independent task: modes, streaming & line formats

In `Practice/02_Modes_Streaming_And_Line_Formats.py`, complete this task:

Define `append_amount(path, amount)` to append one nonnegative integer and a newline to a UTF-8 file. Define `load_amounts(path)` to read nonblank lines as integers in order. Existing records, if any, end with newlines and contain valid nonnegative integers. In an isolated directory append 120, then 80, load the list, and print it and its total.

Expected output:

```text
[120, 80]
200
```
