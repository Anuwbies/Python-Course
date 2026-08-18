# Capstone Project 5.3: CPython Bytecode JIT Transformer & Inliner

## 📌 Project Overview
Build a dynamic **CPython Bytecode Analysis, Decompilation & JIT Optimization Engine**. The project disassembles Python functions into low-level bytecode instruction graphs, performs static data-flow analysis, applies compiler optimization passes (Constant Folding, Dead Code Elimination, Fast Global Inlining, and Small Function Inlining), and reconstructs optimized `types.CodeType` objects that execute transparently in the CPython Virtual Machine.

---

## 🎯 Learning Objectives
- **CPython Virtual Machine & Stack Architecture**: Understanding evaluation stack frames, bytecode opcodes (`LOAD_FAST`, `BINARY_OP`, `STORE_FAST`, `CALL`), and opcode arguments.
- **Bytecode Introspection (`dis` module)**: Extracting and inspecting instruction streams with `dis.get_instructions()`.
- **Compiler Optimization Passes**: Implementing graph-based compiler optimization algorithms:
  - **Constant Folding**: Pre-evaluating deterministic operations (`24 * 60 * 60` $\to$ `86400`) at compile time.
  - **Dead Code Elimination**: Pruning unreachable code blocks following unconditional jumps or `RETURN_VALUE`.
  - **Function Inlining**: Replacing call overhead of small leaf functions with inlined bytecode.
- **Code Object Reconstruction**: Dynamically constructing valid, executable `types.CodeType` instances.
- **Performance Benchmarking**: Measuring microsecond execution time differences and bytecode instruction count reductions.

---

## 🏗️ System Architecture

```text
         [ Target Python Function ]
                     |
                     v
       [ Bytecode Disassembler (dis) ]
                     |
                     v
       [ Control Flow & Basic Blocks Graph ]
                     |
     +---------------+---------------+
     |                               |
     v                               v
[ Constant Folder Pass ]   [ Dead Code Eliminator ]
     |                               |
     +---------------+---------------+
                     |
                     v
         [ Leaf Function Inliner ]
                     |
                     v
        [ CodeType Serializer / JIT ]
                     |
                     v
         [ Optimized Python Function ]
```

---

## 📋 Functional Requirements

### 1. Bytecode Disassembler & Control Flow Graph (CFG)
- Disassemble a callable Python function into a sequence of mutable `Instruction` objects.
- Construct Basic Blocks (sequences of instructions with a single entry point and single exit point).

### 2. Optimization Pass 1: Constant Folding
- Identify consecutive `LOAD_CONST` instructions followed by binary operations (e.g. `BINARY_OP`, `COMPARE_OP`).
- Pre-compute the literal value and replace the sequence with a single `LOAD_CONST` holding the computed result.

### 3. Optimization Pass 2: Dead Code Elimination
- Identify conditional branches with statically known constant conditions (e.g., `if False:` or `if 0:`).
- Remove unreachable basic blocks and repair relative jump offsets (`POP_JUMP_FORWARD_IF_FALSE`, etc.).

### 4. Dynamic Code Object Re-builder
Construct a new `types.CodeType` with updated `co_code`, `co_consts`, `co_names`, and `co_stacksize`:
```python
import types

def rebuild_function(original_func, optimized_code_bytes, new_consts):
    co = original_func.__code__
    new_code = co.replace(
        co_code=optimized_code_bytes,
        co_consts=tuple(new_consts)
    )
    return types.FunctionType(
        new_code,
        original_func.__globals__,
        original_func.__name__,
        original_func.__defaults__,
        original_func.__closure__
    )
```

### 5. `@jit_optimize` Decorator API
Provide an easy-to-use decorator:
```python
@jit_optimize
def compute_seconds():
    # Gets transformed at function definition time!
    return 365 * 24 * 60 * 60
```

---

## 📐 Phased Implementation Guide

### Phase 1: Instruction Representation & Disassembly
```python
import dis
from dataclasses import dataclass
from typing import List, Any

@dataclass
class IrInstruction:
    opname: str
    opcode: int
    arg: Any
    argval: Any
    offset: int

def disassemble_to_ir(func) -> List[IrInstruction]:
    instructions = []
    for instr in dis.get_instructions(func):
        instructions.append(
            IrInstruction(
                opname=instr.opname,
                opcode=instr.opcode,
                arg=instr.arg,
                argval=instr.argval,
                offset=instr.offset
            )
        )
    return instructions
```

### Phase 2: Constant Folding Transformer Pass
Iterate through IR instructions and fold consecutive constant pairs into computed constants.

### Phase 3: Bytecode Assembler & Function Replacement
Recompile IR into raw opcode bytes, update jump targets, and return the optimized callable.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Simple Constant Fold** | `return 10 + 20 * 5` | Optimized bytecode contains only 1 `LOAD_CONST 110` and 1 `RETURN_VALUE` |
| **Dead Code Pruning** | Code following `if False:` block | Unreachable instructions completely omitted from `co_code` |
| **Side-Effect Safety** | Expression with function call `foo() + 5` | Does NOT fold function call; preserves dynamic evaluation order |
| **Identical Output** | Run original vs optimized function with 1,000 arguments | Output return values match 100% identically across all test inputs |

---

## 🚀 Bonus Challenges
- **Built-in Function Inlining**: Inline common pure built-in calls like `len("literal_string")` or `abs(-42)` directly at compile time.
- **Visual Control Flow Graph**: Export the function's Basic Block Graph to a Graphviz `.dot` or Mermaid diagram.
