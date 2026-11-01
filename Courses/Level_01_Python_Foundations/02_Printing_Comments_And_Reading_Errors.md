# Lesson 2: Printing, Comments & Reading Errors

**Prerequisites:** Lesson 1. **Save your work:** `Practice/02_learning_receipt.py`.

Output lets a program communicate with its user. Comments communicate with the person reading the source. Error messages communicate what Python could not understand or execute. Keeping these three forms of communication distinct helps you write code that is easier to inspect and repair.

## 1. Read a call to `print()`

```python
print("Python Foundations")
print("Lesson", 2)
print()
print("Ready to learn.")
```

`print` is a built-in function: a named operation Python already provides. You do not need to define it or install anything. Writing parentheses after its name calls it. Values inside the parentheses are its arguments, meaning the values supplied for that call.

In the first call, the argument is a text value. In the second, there are two arguments separated by a comma. With its normal settings, `print()` displays a space between arguments and ends each call with a new line. The third call has no arguments, so it produces a blank line.

The output is:

```text
Python Foundations
Lesson 2

Ready to learn.
```

The comma separating the arguments is Python syntax; it is not printed as a comma. Put punctuation inside a quoted text value when you want that punctuation displayed.

## 2. Quotation marks define text boundaries

You can use either single or double quotes for an ordinary text value. The opening and closing quotes must match. A quote of the other kind can appear inside the text without ending it:

```python
print("I'm learning Python.")
print('The screen says "Ready".')
```

The surrounding quotes tell Python where the text begins and ends. They are not displayed. An apostrophe inside a single-quoted value would end that value unless escaped, so using double quotes is often the simpler choice.

Use straight quotation marks in source code. A word processor may substitute curved quotation marks that Python does not recognize as string delimiters. Editing source in a code editor avoids that problem.

You can deliberately place a newline inside a string using `\n`:

```python
print("Line one\nLine two")
```

The backslash and `n` together form an **escape sequence** representing a newline. The program displays two lines, not the characters `\n`. Later string lessons explore text in more detail; ordinary one-line values are sufficient for this lesson's task.

## 3. Comments explain source code

```python
# Explain the report's purpose to the reader.
print("Learning receipt")
print("Status: Started")  # Show the current study status.
print("# This hash is part of the message.")
```

Outside a string, `#` starts a comment that continues to the end of that line. Python does not execute the comment as an instruction. Inside quotes, the same character is simply part of the text value, so the last call displays it.

A useful comment explains intent, an assumption, or a decision that is not obvious. `# Print a message` beside a simple `print()` call adds little information. `# Use whole pesos because fractional amounts are outside this exercise` explains a meaningful assumption.

Blank lines can separate related groups of statements without changing their output. A blank source line is different from `print()`: the first organizes the source; the second creates a blank output line.

## 4. Read errors as information

If Python cannot parse the program's syntax, it reports a `SyntaxError`. A missing closing quote or parenthesis is a common cause. For example, `print("Ready")` is complete, but `print("Ready"` is missing its final parenthesis.

Inspect the filename, line number, and message. The indicated location is where Python detected a problem; the cause can sometimes begin on an earlier line. Check the surrounding statement rather than adding punctuation at random.

A program can also have valid syntax but fail while running. Calling `pritn("Ready")` uses a name Python does not know, which raises `NameError`. The parentheses and quotes are correct; the function name is misspelled.

```text
NameError: name 'pritn' is not defined
```

The final line identifies the error type and gives a short explanation. The preceding traceback points to the source location and, in larger programs, the sequence of calls that reached it. For now, start at the final line, then find the relevant line in your own script.

## 5. Separate syntax, runtime, and logic mistakes

| Kind | Example | What to inspect |
| --- | --- | --- |
| Syntax mistake | Missing closing quote | The source structure |
| Runtime error | `pritn` instead of `print` | The failing name or operation |
| Logic mistake | Printing `Finished` when the task says `Started` | The requirement and actual result |

A logic mistake may produce no Python error at all. The interpreter can execute a program perfectly while the program does the wrong thing. This is why you compare actual output with requirements instead of considering “it ran” sufficient evidence.

Fix one cause at a time, save the file, and run it again. If the message changes, read the new message; a program can contain more than one mistake.

Reference: [Python's introduction: comments and text](https://docs.python.org/3.13/tutorial/introduction.html).

## Practice: predict, explain, modify, debug

1. **Predict:** What exact lines does `print("A", "B")` followed by `print()` produce? Include the blank line in your prediction.
2. **Explain:** Why does `# learning` disappear as a comment while `print("# learning")` displays a hash?
3. **Modify:** In a scratch file, print a title, a blank line, and a status message. Add a comment explaining the report's purpose.
4. **Debug:** Correct `pritn("Status: Started")` and explain why its original error is about a name rather than missing punctuation.

<details>
<summary>Hints</summary>

Separate `print()` arguments receive a space by default. An empty call still ends a line. Quote boundaries determine whether a hash is text or a comment marker.

</details>

## Independent task: learning receipt

In `Practice/02_learning_receipt.py`, write a program that uses three separate `print()` calls to display:

```text
LEARNING RECEIPT
Course: Python Foundations
Status: Started
```

Add one source comment explaining the purpose of the receipt. The comment must not appear in the output. Do not add blank output lines.
