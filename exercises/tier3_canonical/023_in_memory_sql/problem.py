"""SQL database scaffold."""
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
        raise NotImplementedError("gate 1")

    def insert(self, table: str, row: Row) -> None:
        raise NotImplementedError("gate 1")

    def select(
        self,
        table: str,
        *,
        where: Predicate | None = None,
        order_by: list[str] | None = None,
        columns: list[str] | None = None,
    ) -> list[Row]:
        raise NotImplementedError("gates 1-3")
