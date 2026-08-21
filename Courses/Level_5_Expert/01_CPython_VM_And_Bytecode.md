# Lesson 1: CPython Internals: VM Architecture & Bytecode Disassembly

To attain true mastery over Python, you must understand what happens under the hood when your script executes. Python is not purely interpreted line-by-line; CPython compiles your human-readable source code into compact bytecode instructions that are executed by a high-speed C-based stack evaluation virtual machine. In this lesson, you will master the CPython compilation pipeline, disassemble bytecode using the `dis` module, inspect Python Code Objects, and explore Python 3.11+ Specialized Adaptive Interpreter optimizations.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Trace the CPython execution pipeline: Tokenization $\to$ Parsing $\to$ AST $\to$ Control Flow Graph $\to$ Bytecode Object.
2. Disassemble and analyze Python functions using the standard `dis` module.
3. Understand the **CPython Stack Machine** and core opcodes (`LOAD_FAST`, `STORE_FAST`, `BINARY_OP`, `CALL`, `RETURN_VALUE`).
4. Inspect Python **Code Objects** (`co_code`, `co_consts`, `co_varnames`, `co_stacksize`).
5. Understand modern Python 3.11+ **Specialized Adaptive Bytecode (Inline Caching)** and Python 3.13 JIT compilation.

---

## 1. The CPython Compilation Pipeline

```
Source (.py) ──> Tokenizer ──> Parser (PEG) ──> AST ──> Bytecode (.pyc) ──> VM Evaluation Loop
```

When Python executes a function, it translates AST nodes into a `code` object containing bytecode opcodes. The CPython evaluation loop (`_PyEval_EvalFrameDefault` in `Python/ceval.c`) iterates through these opcodes on a value stack.

---

## 2. Disassembling Bytecode with `dis`

```python
import dis

def calculate_discount(price: float, rate: float) -> float:
    return price * (1.0 - rate)

dis.dis(calculate_discount)
```

**Disassembly Output Breakdown**:
```text
  1           0 RESUME                   0

  2           2 LOAD_FAST                0 (price)
              4 LOAD_CONST               1 (1.0)
              6 LOAD_FAST                1 (rate)
              8 BINARY_OP               10 (-)
             12 BINARY_OP                5 (*)
             16 RETURN_VALUE
```

### Key Opcodes Explained:
- `RESUME 0`: Internal check for coroutines, generators, and exception handling.
- `LOAD_FAST 0 (price)`: Pushes local variable 0 (`price`) from the fast local array onto the evaluation stack in $\mathcal{O}(1)$ time.
- `LOAD_CONST 1 (1.0)`: Pushes constant `1.0` onto the evaluation stack.
- `BINARY_OP`: Pops top two operands, executes arithmetic, and pushes result.
- `RETURN_VALUE`: Pops top stack value and returns it to the caller frame.

---

## 3. Inspecting Code Objects (`__code__`)

Functions in Python wrap underlying `code` objects containing immutable execution metadata:

```python
code_obj = calculate_discount.__code__

print("Local variables:", code_obj.co_varnames) # ('price', 'rate')
print("Constants:", code_obj.co_consts)         # (None, 1.0)
print("Max Stack Depth:", code_obj.co_stacksize) # 3
print("Raw Bytecode Bytes:", list(code_obj.co_code[:8])) # [151, 0, 124, 0, 100, 1, 124, 1]
```

---

---

## 4. `PyFrameObject` & Stack Execution Internals

When a Python function is invoked, CPython creates a `PyFrameObject` on the C stack/heap:
- `f_localsplus`: A contiguous C array storing both fast local variables and the evaluation stack values in cache-line friendly memory.
- `f_valuestack`: Pointer to top of evaluation stack.
- `f_code`: Reference to the immutable `PyCodeObject`.

### Why `LOAD_FAST` is $3\times$ Faster than `LOAD_GLOBAL`
- **`LOAD_FAST (index)`**: Direct C array index offset access `f_localsplus[index]` (1 CPU cycle).
- **`LOAD_GLOBAL (name)`**: Hash table lookup in the module `__dict__` and built-in `__dict__` (fallback if not cached).

```python
import types

# Dynamic Code Compilation
raw_code = compile("x * 2 + 1", filename="<dynamic>", mode="eval")
print("Compiled opcodes:", [inst.opname for inst in dis.get_instructions(raw_code)])
```

---

## 5. Python 3.11+ Specialized Adaptive Interpreter & 3.13 JIT

- **PEP 659 Quickening**: The interpreter replaces generic opcodes with specialized inline versions during runtime profiling:
  - `BINARY_OP` $\to$ `BINARY_OP_ADD_FLOAT` or `BINARY_OP_ADD_INT`.
  - `LOAD_ATTR` $\to$ `LOAD_ATTR_MODULE` or `LOAD_ATTR_INSTANCE_VALUE`.
- **Python 3.13 Copy-and-Patch JIT**: Compiles hot bytecode traces directly into native machine code (x86-64 / ARM64 assembly) at runtime without heavy LLVM compile times.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master CPython VM internals, bytecode analysis, opcode transformations, and evaluation frames:

---

### 🟢 Tier 1: Bytecode Inspection & `dis` Basics (Exercises 1–3)

#### 🔹 Exercise 1: Function Disassembly Explorer
* **Goal**: Disassemble a basic function using `dis.dis()` and print the opcodes list.

#### 🔹 Exercise 2: Code Object Attribute Inspection
* **Goal**: Extract `co_varnames`, `co_consts`, and `co_stacksize` from a function.

#### 🔹 Exercise 3: Counting Bytecode Instructions
* **Goal**: Write a function counting total opcodes executed in a given callable using `dis.get_instructions()`.

---

### 🟡 Tier 2: Opcode Tallying & Static Analysis (Exercises 4–6)

#### 🔹 Exercise 4: Local vs Global Variable Audit
* **Goal**: Measure the ratio of `LOAD_FAST` to `LOAD_GLOBAL` instructions in a function.

#### 🔹 Exercise 5: Detecting Constant Folding
* **Goal**: Demonstrate how CPython folds `24 * 60 * 60` into a single `86400` constant at compile time.

#### 🔹 Exercise 6: Forbidden Opcode Sandbox Linter
* **Goal**: Write a linter that rejects any code containing `IMPORT_NAME` or `EXEC_STMT`.

---

### 🟠 Tier 3: Code Objects & Dynamic Execution (Exercises 7–9)

#### 🔹 Exercise 7: Dynamic Bytecode Compilation with `compile()`
* **Goal**: Compile an AST expression string into bytecode mode `"eval"` and execute it via `eval()`.

#### 🔹 Exercise 8: Constructing Custom `CodeType` Objects
* **Goal**: Inspect arguments needed to instantiate `types.CodeType` in modern Python.

#### 🔹 Exercise 9: Branching Jump Analysis (`JUMP_FORWARD` / `POP_JUMP_IF_FALSE`)
* **Goal**: Trace conditional branches and target jump offsets in an `if/else` bytecode stream.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Bytecode Security & Execution Efficiency Profiler
* **Goal**: Build an automated bytecode auditor evaluating local vs global lookup efficiencies and flagging security violations.

---

---

## 💻 Code Example & Reference

The following real-life program models an **Enterprise Bytecode Security Auditor & AST Instruction Validator**, inspecting compiled Python functions at the virtual machine level to detect unsafe opcodes, forbidden global accesses, or excessive stack allocations:

```python
# =====================================================================
# REAL-WORLD SYSTEM: CPython Bytecode Security & Opcode Sandbox Auditor
# =====================================================================

import dis
import types

class BytecodeSecurityAuditor:
    """Inspects Python code objects at bytecode level to enforce sandbox security."""

    FORBIDDEN_GLOBAL_NAMES = {"eval", "exec", "os", "subprocess", "sys", "__import__"}
    FORBIDDEN_OPCODES = {"IMPORT_NAME", "IMPORT_FROM"}

    @classmethod
    def audit_function(cls, target_fn: types.FunctionType) -> dict:
        code_obj = target_fn.__code__
        violations = []
        opcodes_tally = {}

        # Iterate through disassembled bytecode instructions (Lesson 1)
        for instruction in dis.get_instructions(code_obj):
            opname = instruction.opname
            opcodes_tally[opname] = opcodes_tally.get(opname, 0) + 1

            # Rule 1: Check forbidden opcodes (e.g. importing unauthorized modules inside sandbox)
            if opname in cls.FORBIDDEN_OPCODES:
                violations.append(f"Security Violation: Forbidden opcode '{opname}' at offset {instruction.offset}")

            # Rule 2: Check global identifier access (e.g. calling eval or accessing OS)
            if opname in {"LOAD_GLOBAL", "LOAD_NAME"}:
                var_name = instruction.argval
                if var_name in cls.FORBIDDEN_GLOBAL_NAMES:
                    violations.append(f"Security Violation: Access to restricted global symbol '{var_name}' at offset {instruction.offset}")

        is_safe = len(violations) == 0
        return {
            "function_name": target_fn.__name__,
            "total_opcodes": sum(opcodes_tally.values()),
            "distinct_opcodes": len(opcodes_tally),
            "max_stack_depth": code_obj.co_stacksize,
            "constants": code_obj.co_consts,
            "local_variables": code_obj.co_varnames,
            "is_sandbox_approved": is_safe,
            "violations": violations,
        }


# Target Functions to Audit
def safe_math_computation(a: float, b: float) -> float:
    multiplier = 2.5
    return (a + b) * multiplier

def dangerous_script_payload(payload: str) -> None:
    import os # Triggers IMPORT_NAME
    eval(payload) # Triggers LOAD_GLOBAL 'eval'


# Run Bytecode Security Audit
print("=" * 80)
print(f"{'CPYTHON VIRTUAL MACHINE BYTECODE SECURITY AUDITOR':^80}")
print("=" * 80)

for fn in (safe_math_computation, dangerous_script_payload):
    report = BytecodeSecurityAuditor.audit_function(fn)
    status_tag = "✅ APPROVED" if report["is_sandbox_approved"] else "🚨 REJECTED (VULNERABILITY DETECTED)"
    
    print(f"\nTarget Function: def {report['function_name']}() -> {status_tag}")
    print(f"  • Total Bytecode Instructions: {report['total_opcodes']}")
    print(f"  • Local Variables (co_varnames): {report['local_variables']}")
    print(f"  • Constants (co_consts):        {report['constants']}")
    print(f"  • Evaluation Stack Size:        {report['max_stack_depth']}")
    
    if report["violations"]:
        print("  • Violations Flagged:")
        for v in report["violations"]:
            print(f"    - {v}")

print("\n" + "=" * 80)
```

### 🔍 Code Explanation:
- **`dis.get_instructions(code_obj)`**: Streams structured `Instruction` objects detailing offset, opcode name (`LOAD_FAST`, `LOAD_GLOBAL`), and resolved argument values.
- **Code Object Inspection**: Analyzes `co_varnames`, `co_consts`, and `co_stacksize` directly from CPython VM memory frames.
- **Security Sandboxing**: Validates that sandbox user routines do not compile unauthorized imports or global system invocations.

---

## 📝 Quick Exercise: Bytecode Instruction Complexity & Global Access Profiler

### 🏢 Real-Life Scenario
You are developing a static analysis compiler plugin that evaluates function efficiency. In CPython, accessing local variables (`LOAD_FAST`) takes $\mathcal{O}(1)$ pointer array access, whereas global variable lookups (`LOAD_GLOBAL`) require dictionary hash-table lookups. You will write a tool that counts local vs global lookups across functions to recommend optimizations.

### 📋 Requirements
1. **Define `profile_bytecode_efficiency(target_fn) -> dict`**:
   - Uses `dis.get_instructions(target_fn.__code__)`.
   - Counts total occurrences of:
     - `local_lookups`: `LOAD_FAST` and `STORE_FAST`
     - `global_lookups`: `LOAD_GLOBAL` and `STORE_GLOBAL`
     - `constant_lookups`: `LOAD_CONST`
     - `arithmetic_ops`: `BINARY_OP`
   - Computes `fast_local_ratio`: $\frac{\text{local\_lookups}}{\text{local\_lookups} + \text{global\_lookups}}$ (if sum > 0, else 1.0).
   - Returns dictionary summary.
2. Profile two test functions (one using local variables, one using repeated global lookups).

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 5 CPython VM bytecode inspection with Level 2 introspection and Level 1 dictionaries and formatting.

### 🎯 Expected Output
```text
==================================================
        CPYTHON BYTECODE EFFICIENCY PROFILER      
==================================================
Function: optimized_local_function
  - Local Lookups (LOAD/STORE_FAST):   4
  - Global Lookups (LOAD/STORE_GLOBAL):0
  - Fast Local Execution Ratio:        100.0% [OPTIMAL]
--------------------------------------------------
Function: unoptimized_global_function
  - Local Lookups (LOAD/STORE_FAST):   1
  - Global Lookups (LOAD/STORE_GLOBAL):3
  - Fast Local Execution Ratio:        25.0% [GLOBAL OVERHEAD]
==================================================
```

<details>
<summary><b>🔍 View Exercise Solutions (Bytecode Profiler & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: CPython Bytecode Efficiency Profiler
# =====================================================================
import dis

def profile_bytecode_efficiency(target_fn) -> dict:
    stats = {
        "local_lookups": 0,
        "global_lookups": 0,
        "constant_lookups": 0,
        "arithmetic_ops": 0,
    }

    for inst in dis.get_instructions(target_fn.__code__):
        if inst.opname in {"LOAD_FAST", "STORE_FAST"}:
            stats["local_lookups"] += 1
        elif inst.opname in {"LOAD_GLOBAL", "STORE_GLOBAL"}:
            stats["global_lookups"] += 1
        elif inst.opname == "LOAD_CONST":
            stats["constant_lookups"] += 1
        elif inst.opname == "BINARY_OP":
            stats["arithmetic_ops"] += 1

    total_var = stats["local_lookups"] + stats["global_lookups"]
    ratio = (stats["local_lookups"] / total_var * 100.0) if total_var > 0 else 100.0
    stats["fast_local_ratio"] = ratio
    return stats


GLOBAL_RATE = 0.08
GLOBAL_TAX = 5.0

def optimized_local_function(price: float) -> float:
    rate = 0.08
    tax = 5.0
    return (price * rate) + tax

def unoptimized_global_function(price: float) -> float:
    return (price * GLOBAL_RATE) + GLOBAL_TAX


print("==================================================")
print("        CPYTHON BYTECODE EFFICIENCY PROFILER      ")
print("==================================================")

for fn in (optimized_local_function, unoptimized_global_function):
    res = profile_bytecode_efficiency(fn)
    tag = "[OPTIMAL]" if res["fast_local_ratio"] >= 80.0 else "[GLOBAL OVERHEAD]"
    print(f"Function: {fn.__name__}")
    print(f"  - Local Lookups (LOAD/STORE_FAST):   {res['local_lookups']}")
    print(f"  - Global Lookups (LOAD/STORE_GLOBAL):{res['global_lookups']}")
    print(f"  - Fast Local Execution Ratio:        {res['fast_local_ratio']:.1f}% {tag}")
    print("--------------------------------------------------")

print("==================================================")

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Disassemble Function
def sample_add(a, b): return a + b
# dis.dis(sample_add)

# Ex 2: Code Object Attributes
def inspect_code(fn):
    c = fn.__code__
    return {"varnames": c.co_varnames, "consts": c.co_consts, "stack": c.co_stacksize}

# Ex 3: Instruction Counter
def count_instructions(fn):
    return len(list(dis.get_instructions(fn)))

# Ex 4: Local vs Global
# Tested in main exercise solution above.

# Ex 5: Constant Folding
def calc_seconds(): return 60 * 60 * 24
# dis.dis(calc_seconds) -> LOAD_CONST 86400 (pre-folded)

# Ex 6: Sandbox Linter
def lint_sandbox(fn):
    return not any(i.opname in {"IMPORT_NAME", "IMPORT_FROM"} for i in dis.get_instructions(fn))

# Ex 7: Dynamic compile
compiled = compile("x * 2 + 1", "<string>", "eval")
# eval(compiled, {"x": 5}) -> 11

# Ex 8: CodeType Construction
# types.CodeType(0, 0, 0, 0, 1, 67, b'...', (None,), (), (), '<str>', 'fn', 1, b'')

# Ex 9: Branch Jump Analysis
def branch_fn(x):
    if x > 0: return 1
    return 0
# [i.argval for i in dis.get_instructions(branch_fn) if 'JUMP' in i.opname]
```
</details>
