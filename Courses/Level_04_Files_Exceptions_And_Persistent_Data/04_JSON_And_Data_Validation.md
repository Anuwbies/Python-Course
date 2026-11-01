# Lesson 4: JSON & Data Validation

**Prerequisites:** Levels 1–3 and Lessons 1–3 of this level. **Practice file:** `Practice/04_JSON_And_Data_Validation.py`.

Use a structured format to preserve values and their relationships, then validate the structure that was actually loaded. Successfully parsing JSON does not establish that it contains valid expense data.

## 1. Serialize structure instead of display text

`json.dump(value, handle)` writes a JSON representation to an open text file. `json.load(handle)` reconstructs supported values from that file. The string counterparts dumps and loads work without file handles. Use UTF-8 when the file is text.

```python
import json

text = json.dumps({"amounts": [0, 25]}, ensure_ascii=False)
loaded = json.loads(text)
print(loaded["amounts"])  # [0, 25]
```

JSON supports objects, arrays, strings, numbers, Booleans, and null. Python tuples become JSON arrays and load as lists. Object keys are strings in JSON, so an arbitrary Python dictionary is not automatically preserved with every original key type. This is data interchange, not a way to save arbitrary running Python objects.

## 2. Validate the loaded shape

A file containing `{}` is valid JSON but not a list of amounts. `isinstance(value, list)` asks whether a value is a list or compatible subclass. For this task use `type(amount) is int` to require a plain integer and reject JSON true/false, which otherwise behave as Python Booleans and are also int subclasses.

Validate the outer container before iterating its intended records. Validate a value's type before comparing it numerically; a string and an integer do not support the same range comparisons. Short-circuit conditions can keep those checks in the right order.

## 3. Distinguish syntax, schema, and storage failures

Malformed JSON raises JSONDecodeError. A loaded value with an invalid application shape should raise a documented ValueError. Missing files and permission failures are storage concerns with their own error types. Catch only what the caller can interpret appropriately.

A missing first-use file can be treated as an empty tracker under an explicit policy. A corrupt existing file must not be silently treated as empty and then overwritten on the next save. That would turn a parsing error into data loss.

## 4. Validate before opening for replacement

Opening a destination in write mode truncates it. Check all input values before opening it so a late invalid item does not erase a known-good file. This still does not prevent an I/O failure during writing; the last lesson introduces temporary replacement for that separate risk.

JSON's ensure_ascii=False keeps readable non-ASCII characters in the encoded text when the output encoding supports them. It is a readability option rather than a security or validation feature. Formatting with indent changes presentation while preserving the data model.

## Match string and file JSON APIs

`json.dumps(value)` returns JSON text and `json.loads(text)` parses text. In contrast, `json.dump(value, handle)` writes to an already opened text handle and `json.load(handle)` reads one complete JSON document from it. Use a UTF-8 handle on both paths. A loader should parse first and validate the returned Python value before returning it to the caller.

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as folder:
    path = Path(folder) / "labels.json"
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(["café"], handle, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as handle:
        labels = json.load(handle)
    print(labels)  # ['café']
```

JSONDecodeError is a ValueError subtype. Type and range validation still happen after parsing. Check dictionary keys with membership or an exact key set before indexing required fields, so an invalid schema raises the documented validation error rather than an accidental KeyError.

References: [JSON module](https://docs.python.org/3.13/library/json.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the type loaded from a JSON array and from a JSON object.
2. **Explain:** Explain why parseable data may still violate a schema.
3. **Modify:** Reject a Boolean amount even though True can participate in integer arithmetic.
4. **Debug:** Move validation ahead of opening a known-good destination in write mode.

<details>
<summary>Hints</summary>

Check the container, then each type, then its numeric range.

</details>

## Independent task: json & data validation

In `Practice/04_JSON_And_Data_Validation.py`, complete this task:

Define `validate_amounts(value)` to require a list of plain nonnegative integers, raising ValueError otherwise. Return a copy of valid data. Define JSON save/load functions using UTF-8 and validation on both paths. Round-trip `[0, 25]` in an isolated directory and print it. Demonstrate rejecting `[True]` with the line `Boolean rejected`.

Expected output:

```text
[0, 25]
Boolean rejected
```
