# Lesson 6: Strings & Text Methods

**Prerequisites:** Lessons 1–5. **Save your work:** `Practice/06_text_cleanup.py`.

Strings represent names, labels, messages, and the text users enter. Working with text means paying attention to characters that are easy to overlook, such as leading spaces, line breaks, and differences in letter case. This lesson introduces a few transformations while keeping the original meaning visible.

## 1. A string is a sequence of text characters

```python
name = "Mika Santos"
empty_text = ""
one_space = " "

print(name)
print(len(name))        # 11
print(len(empty_text))  # 0
print(len(one_space))   # 1
```

`len()` returns the length of a string. The space between the first and last names counts, so this example has eleven characters. An empty string contains no characters; a string containing a space is not empty even if it looks blank on the screen.

Python strings support Unicode text, including names such as `José`. For these simple examples, counting characters is straightforward. With some emoji and combining marks, what appears as one visual symbol may consist of several Unicode code points, so `len()` is not a general measurement of display width.

## 2. Combine and repeat text deliberately

```python
first_name = "Mika"
last_name = "Santos"
full_name = first_name + " " + last_name

print(full_name)  # Mika Santos
print("-" * 12)  # ------------
```

With strings, `+` concatenates text: it builds a new string by joining the pieces in order. It does not insert spaces automatically. The explicit `" "` supplies the gap between the names. This differs from separate arguments to `print()`, which normally receive a separating space.

Multiplying a string by a nonnegative integer repeats it. This can create a simple report divider. An operator's meaning depends on its operands' types: numeric addition and string concatenation share a symbol but perform different operations.

You cannot directly concatenate a string and an integer using `+`. `"Days: " + 5` raises `TypeError`. For now use `print("Days:", 5)`; later lessons show f-strings and explicit conversion.

## 3. Methods perform operations on a value

```python
raw_name = "  Mika Santos  "
clean_name = raw_name.strip()
upper_name = clean_name.upper()
lower_name = clean_name.lower()

print(clean_name)  # Mika Santos
print(upper_name)  # MIKA SANTOS
print(lower_name)  # mika santos
```

The dot connects a value or variable to an operation associated with it. A call such as `raw_name.strip()` asks that string to produce a version with surrounding whitespace removed. Whitespace includes ordinary spaces and characters such as tabs and newlines. Internal spaces remain, so the first and last names stay separated.

The parentheses call the method. Writing `raw_name.strip` without parentheses refers to the method itself rather than performing the cleanup. Calling `.strip()` does not remove every space everywhere; it removes whitespace at the two ends with its default behavior.

`.upper()` and `.lower()` return text with the corresponding case transformation. A case change can be useful for a display label or a comparison strategy, but changing a person's supplied spelling automatically is a design choice. The capstone only strips surrounding whitespace from names.

## 4. String methods return new strings

```python
raw_name = "  Mika Santos  "
raw_name.strip()
print(len(raw_name))  # 15: the original binding is unchanged

clean_name = raw_name.strip()
print(len(clean_name)) # 11
```

Strings are **immutable**: these operations do not edit the original string in place. The first call produces a cleaned result, but nothing saves it. The second call assigns that result to `clean_name`, making it available afterward.

If you want the original variable to refer to the cleaned value, write `raw_name = raw_name.strip()`. That assignment replaces the name's binding; it does not mutate the original string. This distinction will become important again when collections and function side effects are introduced.

## 5. Replace a known piece of text

```python
course_label = "Python basics"
updated_label = course_label.replace("basics", "foundations")

print(course_label)   # Python basics
print(updated_label)  # Python foundations
```

`.replace(old, new)` returns text with occurrences of `old` replaced by `new`. The original is unchanged. Matching is case-sensitive, so replacing `"Basics"` would not match the lowercase `"basics"` in this example. Without an additional limit argument, all matching occurrences are replaced.

Use this operation when the replacement rule is explicit. It is not a general spelling corrector or a way to decide whether user input is valid. Avoid combining many unexplained transformations just because a method is available.

## 6. Preserve useful distinctions

Cleanup should solve a specific problem. Stripping accidental outer spaces from a name is different from removing its meaningful internal space. A product code with leading zeros is text that may need to stay exactly as entered. A string containing `"0"` is not the same thing as an empty string.

Before applying a transformation, state what should change and what should remain meaningful. For this level's task, the contract is simple: remove only surrounding whitespace, produce an uppercase display version, count the cleaned characters, and replace one known word in a course label.

## Practice: predict, explain, modify, debug

1. **Predict:** What are the lengths of `""`, `" "`, and `"A B"`? What does `"Go" * 3` display?
2. **Explain:** Why does `.strip()` preserve the space inside `"Mika Santos"`?
3. **Modify:** Change the name in section 3 and display both the untouched source text and its cleaned version between literal `|` markers so the edges are visible.
4. **Debug:** A program calls `raw_name.strip()` and then expects `raw_name` to have changed. Correct the assignment and explain why the original call was insufficient.

<details>
<summary>Hints</summary>

Whitespace is still text. String methods return results that must be used or saved. Concatenation can place `"|"` before and after a value to make its edges easier to see.

</details>

## Independent task: text cleanup

In `Practice/06_text_cleanup.py`, start with `raw_name = "  Mika Santos  "` and `course_label = "Python basics"`.

1. Save a version of the name with surrounding whitespace removed.
2. Save an uppercase version of the cleaned name.
3. Save an updated course label with `basics` replaced by `foundations`.
4. Keep the two original variables unchanged.
5. Print the cleaned name, uppercase name, length of the cleaned name, and updated course label, one per line.

Expected output:

```text
Mika Santos
MIKA SANTOS
11
Python foundations
```
