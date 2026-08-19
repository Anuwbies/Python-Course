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

## 4. Modern CPython Optimizations: Quickening & Inline Caching

Starting in Python 3.11 (Faster CPython initiative), the interpreter observes opcodes during execution. If an operation is consistently performed on the same data types (e.g. adding two floats), CPython dynamically rewrites (`super-specializes`) the opcode in-place in memory (e.g. `BINARY_OP` becomes `BINARY_OP_ADD_FLOAT`), bypassing generic type dispatch overhead.

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
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import dis

# 1. Bytecode Profiler (Level 5)
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


# 2. Test Functions
GLOBAL_RATE = 0.08
GLOBAL_TAX = 5.0

def optimized_local_function(price: float) -> float:
    rate = 0.08
    tax = 5.0
    return (price * rate) + tax

def unoptimized_global_function(price: float) -> float:
    return (price * GLOBAL_RATE) + GLOBAL_TAX


# 3. Execution Run
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
```

**Explanation of the Solution:**
- `profile_bytecode_efficiency` inspects the opcode stream via `dis.get_instructions()`.
- Highlights how storing variables locally utilizes CPython's fast array-indexed `LOAD_FAST` instruction instead of dictionary-hashed `LOAD_GLOBAL`.
</details>
