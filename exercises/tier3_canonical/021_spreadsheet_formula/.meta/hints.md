# Hints for Spreadsheet Formula Evaluator

## Hint 1

This problem has three distinct gates. Gate 1 needs lazy recursive evaluation: `get_cell` should call itself when it encounters a formula referencing another cell. Gate 2 needs cycle detection during that recursion — think about how recursive DFS tracks "currently being visited" nodes. Gate 3 flips the data flow: instead of pulling lazily, push updates eagerly using a reverse-dependency graph built at `set_cell` time.

## Hint 2

- Gate 1: store raw cell values in `self._cells`; in `get_cell`, if the stored value is a formula, call `_parse_formula` and recursively evaluate each operand (either a cell name or an integer literal).
- Gate 2: track a `visiting: set[str]` during `get_cell` recursion; if a cell name appears in `visiting` when you try to recurse into it, raise `CycleError`.
- Gate 3: in `set_cell`, build `self._dependents: dict[str, set[str]]` (reverse edges); on each `set_cell` call, BFS/DFS the dependents and recompute `self._values` in topological order.
- `_parse_formula` is already provided — it returns `[('+', operand), ...]` where operand is either a cell name like `"A1"` or an integer string like `"10"`.

## Hint 3

Gate 2 cycle check inside recursive `get_cell`:

```python
def get_cell(self, name: str, _visiting: frozenset[str] = frozenset()) -> int:
    if name in _visiting:
        raise CycleError(f"cycle detected at {name!r}")
    raw = self._cells.get(name, 0)
    if not self._is_formula(raw):
        return int(raw)
    _visiting = _visiting | {name}
    total = 0
    for op, operand in self._parse_formula(raw):
        val = int(operand) if operand.lstrip("+-").isdigit() else self.get_cell(operand, _visiting)
        total += val if op == "+" else -val
    return total
```
