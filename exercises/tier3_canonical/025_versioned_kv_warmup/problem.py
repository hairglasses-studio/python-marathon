"""Warm-up 2 SCAFFOLD — fill in the gates, then run the tests cell."""
from __future__ import annotations

from collections import defaultdict
from typing import Generic, TypeVar

V = TypeVar("V")


class VersionedKV(Generic[V]):
    def __init__(self) -> None:
        self._versions: dict[str, list[tuple[int, V]]] = defaultdict(list)
        self._clock = 0
        # Gate 3: add per-key locks + a global lock for the lock map

    def _tick(self) -> int:
        self._clock += 1
        return self._clock

    def set(self, key: str, value: V) -> int:
        """Append a new (ts, value) version. Returns the ts."""
        raise NotImplementedError("Gate 1-3: implement set")

    def get(self, key: str, ts: int | None = None) -> V | None:
        """Return the latest value at time ts (or latest overall if ts is None)."""
        raise NotImplementedError("Gate 1-2: implement get")

    def snapshot(self, ts: int) -> "Snapshot[V]":
        """Return a frozen read-only view at time ts."""
        raise NotImplementedError("Gate 4: implement snapshot")


class Snapshot(Generic[V]):
    def __init__(self, data: dict[str, V], ts: int) -> None:
        self._data = data
        self._ts = ts

    def get(self, key: str) -> V | None:
        return self._data.get(key)

    @property
    def ts(self) -> int:
        return self._ts
