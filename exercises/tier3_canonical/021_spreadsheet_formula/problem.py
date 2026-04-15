"""Spreadsheet scaffold — fill in the three methods, run the tests cell."""
from __future__ import annotations

import re


class CycleError(RuntimeError):
    """Raised when a formula would create a dependency cycle."""


class Spreadsheet:
    def __init__(self) -> None:
        # You will likely need at least:
        #   self._cells: dict[str, int | str]   # raw storage
        #   self._values: dict[str, int]        # computed values (gate 3)
        #   self._dependents: dict[str, set[str]]  # gate 3
        self._cells: dict[str, int | str] = {}

    def set_cell(self, name: str, value: int | str) -> None:
        """Set a cell to a literal int or a formula string like '=A1+B2'."""
        raise NotImplementedError("gates 1-3")

    def get_cell(self, name: str) -> int:
        """Return the current int value of the named cell (0 if unset)."""
        raise NotImplementedError("gates 1-2")

    # --- Helpers you'll want ---

    @staticmethod
    def _is_formula(value: int | str) -> bool:
        return isinstance(value, str) and value.startswith("=")

    @staticmethod
    def _parse_formula(formula: str) -> list[tuple[str, str]]:
        """Parse '=A1+B2-C3' → [('+', 'A1'), ('+', 'B2'), ('-', 'C3')].

        Operands are either cell names (e.g., 'A1') or integer literals (e.g., '42').
        The leading '+' is implicit for the first term.
        """
        body = formula[1:] if formula.startswith("=") else formula
        # Regex: optional sign + operand (cell name or integer)
        tokens: list[tuple[str, str]] = []
        pattern = re.compile(r"([+-])?([A-Z]+\d*|\d+)")
        for match in pattern.finditer(body):
            op = match.group(1) or "+"
            operand = match.group(2)
            tokens.append((op, operand))
        return tokens
