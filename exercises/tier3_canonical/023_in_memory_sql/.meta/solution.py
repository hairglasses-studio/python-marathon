from __future__ import annotations

from typing import Any, Callable


class TableNotFound(KeyError):
    pass


class SchemaError(ValueError):
    pass


Row = dict[str, Any]
Predicate = Callable[[Row], bool]


class Database:
    def __init__(self) -> None:
        self._schemas: dict[str, list[str]] = {}
        self._rows: dict[str, list[Row]] = {}

    def create_table(self, name: str, columns: list[str]) -> None:
        self._schemas[name] = list(columns)
        self._rows[name] = []

    def insert(self, table: str, row: Row) -> None:
        if table not in self._schemas:
            raise TableNotFound(table)
        schema = set(self._schemas[table])
        extra = set(row.keys()) - schema
        if extra:
            raise SchemaError(f"unknown columns for {table}: {sorted(extra)}")

        # Normalize the row — every column present, missing ones are None.
        normalized: Row = {col: row.get(col) for col in self._schemas[table]}
        self._rows[table].append(normalized)

    def select(
        self,
        table: str,
        *,
        where: Predicate | None = None,
        order_by: list[str] | None = None,
        columns: list[str] | None = None,
    ) -> list[Row]:
        if table not in self._schemas:
            raise TableNotFound(table)

        # Start with a shallow copy so sorting doesn't mutate storage.
        rows = list(self._rows[table])

        # Filter
        if where is not None:
            rows = [r for r in rows if where(r)]

        # Order
        if order_by:
            rows = self._sort(rows, order_by)

        # Project
        if columns is not None:
            rows = [{c: r.get(c) for c in columns} for r in rows]

        return rows

    @staticmethod
    def _sort(rows: list[Row], order_by: list[str]) -> list[Row]:
        # Parse '-col' as descending, 'col' as ascending.
        # Strategy: apply sorts in reverse order using Python's stable sort.
        # (Last sort wins as primary; earlier sorts become tiebreakers.)
        result = list(rows)
        for spec in reversed(order_by):
            if spec.startswith("-"):
                col = spec[1:]
                reverse = True
            else:
                col = spec
                reverse = False
            # Use a default that sorts None last (or first for desc) consistently.
            result.sort(key=lambda r, c=col: (r.get(c) is None, r.get(c)), reverse=reverse)
        return result
