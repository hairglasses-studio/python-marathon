# Notes for Spreadsheet Formula Evaluator

## Why this matters

Spreadsheet DAGs are a canonical example of lazy evaluation with cycle detection — the same pattern shows up in build systems, reactive UI frameworks, and incremental computation engines. Interviewers use this to probe whether you understand recursive dependency resolution and can articulate the tradeoff between lazy re-evaluation (simple, consistent) and eager propagation (O(1) reads, complex writes).

## Watch out for

- Forgetting that `_parse_formula` returns operands as strings — you must distinguish cell names from integer literals before recursing. Check `operand.isdigit()` (or try `int(operand)`).
- Passing a mutable `visiting` set down the call stack without copying it; later branches will incorrectly see nodes from sibling branches as "visited."

## Interview follow-ups

- "How would you make `get_cell` O(1)?" — push-based propagation on `set_cell`; requires tracking a reverse-dependency graph and topological recompute order.
- "What if two cells form a cycle but neither is ever queried?" — lazy detection only raises on `get_cell`; eager detection would require a cycle check at `set_cell` time using the forward-dependency graph.
- "How would you support multi-sheet references like `Sheet2!A1`?" — extend cell name parsing to include sheet prefix; namespace the `_cells` dict by sheet.
