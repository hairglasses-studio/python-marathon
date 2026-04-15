from __future__ import annotations

import re


class CycleError(RuntimeError):
    """Raised when a formula would create a dependency cycle."""


class Spreadsheet:
    def __init__(self) -> None:
        self._cells: dict[str, int | str] = {}

    def set_cell(self, name: str, value: int | str) -> None:
        self._cells[name] = value

    def get_cell(self, name: str) -> int:
        return self._evaluate(name, visiting=set())

    def _evaluate(self, name: str, visiting: set[str]) -> int:
        if name in visiting:
            raise CycleError(f"cycle detected at {name}")

        value = self._cells.get(name, 0)
        if isinstance(value, int):
            return value

        if self._is_formula(value):
            new_visiting = visiting | {name}
            return self._evaluate_formula(value, new_visiting)

        return 0

    def _evaluate_formula(self, formula: str, visiting: set[str]) -> int:
        total = 0
        for op, operand in self._parse_formula(formula):
            if operand.isdigit():
                val = int(operand)
            else:
                val = self._evaluate(operand, visiting)
            if op == "-":
                total -= val
            else:
                total += val
        return total

    @staticmethod
    def _is_formula(value: int | str) -> bool:
        return isinstance(value, str) and value.startswith("=")

    @staticmethod
    def _parse_formula(formula: str) -> list[tuple[str, str]]:
        body = formula[1:] if formula.startswith("=") else formula
        tokens: list[tuple[str, str]] = []
        pattern = re.compile(r"([+-])?([A-Z]+\d*|\d+)")
        for match in pattern.finditer(body):
            op = match.group(1) or "+"
            operand = match.group(2)
            tokens.append((op, operand))
        return tokens


# --- Gate 3: O(1) get_cell via proactive evaluation + dependents map ---

class FastSpreadsheet(Spreadsheet):
    """Gate 3 extension: recompute on set_cell, so get_cell is O(1).

    Maintains a `dependents` map so updating a cell triggers propagation
    through everything that references it.
    """

    def __init__(self) -> None:
        super().__init__()
        self._computed: dict[str, int] = {}
        self._dependents: dict[str, set[str]] = {}     # name -> cells that reference name
        self._formula_deps: dict[str, set[str]] = {}   # name -> cells this formula reads

    def set_cell(self, name: str, value: int | str) -> None:
        # Update the raw storage
        self._cells[name] = value

        # Rewire the dependency graph: remove old deps, add new.
        for dep in self._formula_deps.get(name, set()):
            self._dependents.get(dep, set()).discard(name)
        self._formula_deps[name] = self._direct_deps(value)
        for dep in self._formula_deps[name]:
            self._dependents.setdefault(dep, set()).add(name)

        # Recompute this cell and everything that transitively depends on it.
        self._recompute_transitive(name)

    def get_cell(self, name: str) -> int:
        if name in self._computed:
            return self._computed[name]
        # Cell is unset but may still be referenced; fall back to base behavior.
        return super().get_cell(name)

    def _direct_deps(self, value: int | str) -> set[str]:
        if not self._is_formula(value):
            return set()
        return {
            operand
            for _, operand in self._parse_formula(value)
            if not operand.isdigit()
        }

    def _recompute_transitive(self, start: str) -> None:
        # BFS through the dependents graph, recomputing each cell in topo order
        # relative to the starting node.
        from collections import deque
        seen: set[str] = set()
        queue: deque[str] = deque([start])
        while queue:
            cell = queue.popleft()
            if cell in seen:
                continue
            seen.add(cell)
            # Recompute this cell's value. Cycle detection uses a fresh visiting set.
            try:
                self._computed[cell] = self._evaluate(cell, visiting=set())
            except CycleError:
                # Cycle-creating set should ideally be rejected at set time,
                # but for simplicity we surface at read time.
                self._computed.pop(cell, None)
            queue.extend(self._dependents.get(cell, set()))
