# Spreadsheet Formula Evaluator

**Tier:** tier3_canonical  
**Target time:** 45 minutes  
**Topics:** graph, DAG, lazy-eval, regex, cycle-detection

## Problem

Build a `Spreadsheet` class that stores cells containing either literal integers or formula strings (e.g. `"=A1+B2-10"`), evaluates formulas by resolving references recursively, and detects dependency cycles.

### API

- **`set_cell(name: str, value: int | str) -> None`** — store a literal int or a formula string (starts with `=`).
- **`get_cell(name: str) -> int`** — return the current evaluated value. Unset cells return `0`.

A helper `_parse_formula` is provided that parses `"=A1+B2-C3"` into `[('+', 'A1'), ('+', 'B2'), ('-', 'C3')]`.

### Gates

**Gate 1 — Literal values and formula evaluation:**  
Set cells to ints, read them back. Set a cell to a formula referencing other cells, evaluate it. Handle nested references (a formula referencing a cell that is itself a formula). Support formulas mixing cell references and integer literals (e.g. `"=A1+10"`). When a referenced cell is updated, subsequent `get_cell` calls on dependent cells reflect the new value (lazy re-evaluation).

**Gate 2 — Cycle detection:**  
Raise `CycleError` (a `RuntimeError` subclass, provided in the stub) when evaluating a cell that is part of a dependency cycle. Detect direct cycles (`A1 -> B1 -> A1`), transitive cycles (`A1 -> B1 -> C1 -> A1`), and self-references (`A1 -> A1`).

**Gate 3 — Proactive propagation (stretch):**  
When `set_cell` updates a value, eagerly recompute all downstream dependents so that `get_cell` is O(1). This requires tracking a reverse dependency graph.

## How to run

```bash
python marathon.py run 021
```

Edit `problem.py`. When `test_problem.py` passes, move on.
