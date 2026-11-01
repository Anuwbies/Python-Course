# Lesson 3: Bytecode & Interpreter Behavior

**Prerequisites:** Levels 1–9 and Lessons 1–2 of this level. **Practice file:** `Practice/03_Bytecode_And_Interpreter_Behavior.py`.

Inspect how a particular interpreter represents execution without treating those details as a portable language contract. Bytecode can explain a hypothesis; it does not by itself prove a speed claim.

## 1. Separate source semantics and implementation

The language defines expressions, scope, and observable behavior. CPython compiles code into an internal representation executed by its interpreter. Instruction names, offsets, caches, and specialization strategies can change between releases.

The dis module presents a supported inspection interface for the selected version. Record sys.version and implementation when sharing an investigation. A bytecode listing from one Python version should not be treated as an exact template for another.

## 2. Inspect a small callable

```python
import dis

def add(left, right):
    return left + right

instructions = list(dis.get_instructions(add))
print(add(2, 3))
print([instruction.opname for instruction in instructions])
```

The result remains the semantic evidence; the instruction list describes this compiled function. Code objects also expose metadata such as argument count, variable names, and constants. Those attributes are useful for inspection but should not become accidental assumptions in unrelated application code.

## 3. Account for adaptation

Modern CPython can specialize execution after observing runtime behavior. Disassembly options can expose adaptive or cache information depending on the version. Warm and cold runs can therefore differ even when the source is unchanged.

Comprehensions have also changed implementation across releases, including inlining choices. Do not assume every comprehension always creates a separate function frame, or that fewer visible instructions always means less actual work. A single instruction can perform substantial C-level operations.

## 4. Use inspection to test a question

If a hypothesis concerns repeated attribute lookup or object creation, inspect the relevant operation and compare an independently correct alternative. Then measure under the workload where the hypothesized cost matters.

Avoid editing raw bytecode or constructing code objects merely to demonstrate expertise. Such changes require version-sensitive invariants and can break tooling or interpreter expectations. A clear source-level improvement is easier to maintain when it solves the problem.

## 5. Keep tooling and application boundaries distinct

A diagnostic tool may reasonably depend on a documented interpreter version. A public business function should not depend on an exact opcode sequence unless that is explicitly its purpose. Fail clearly when an inspection capability is unavailable rather than inventing a listing.

The task reports actual instruction names and metadata. Its expected behavior deliberately avoids a fixed bytecode transcript while keeping the arithmetic result exact.

## Read code metadata by its actual attribute names

A Python function's `__code__` refers to its code object. `add.__code__.co_argcount` is its positional parameter count (including positional-only parameters, excluding keyword-only and variable-length collectors). `co_varnames` and `co_consts` expose local-name and constant tuples for inspection. For the task's simple two-parameter add, co_argcount is 2. This does not count the arguments passed in a particular invocation.

References: [Disassembly](https://docs.python.org/3.13/library/dis.html).

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the function result independently of its instruction list.
2. **Explain:** Explain why opcode count is not an elapsed-time measurement.
3. **Modify:** Record interpreter information beside a disassembly.
4. **Debug:** Find an analysis that assumes a comprehension implementation from an older release.

<details>
<summary>Hints</summary>

Inspect through the versioned library interface and keep the result contract independent of opcode spelling.

</details>

## Independent task: bytecode & interpreter behavior

In `Practice/03_Bytecode_And_Interpreter_Behavior.py`, complete this task:

Define add(left,right) returning their sum. Use dis.get_instructions to obtain its actual opcode names and its code object to obtain the positional argument count. Print Result: 5, Arguments: 2, and the observed opcode-name list. Do not hardcode opcode names or offsets; they are version-specific.
