from __future__ import annotations

import bisect
import threading
from collections import defaultdict
from typing import Generic, TypeVar

V = TypeVar("V")


class VersionedKV(Generic[V]):
    def __init__(self) -> None:
        self._versions: dict[str, list[tuple[int, V]]] = defaultdict(list)
        self._clock = 0
        self._locks: dict[str, threading.RLock] = {}
        self._global_lock = threading.Lock()

    def _tick(self) -> int:
        self._clock += 1
        return self._clock

    def _lock_for(self, key: str) -> threading.RLock:
        with self._global_lock:
            if key not in self._locks:
                self._locks[key] = threading.RLock()
            return self._locks[key]

    def set(self, key: str, value: V) -> int:
        with self._lock_for(key):
            ts = self._tick()
            self._versions[key].append((ts, value))
            return ts

    def get(self, key: str, ts: int | None = None) -> V | None:
        with self._lock_for(key):
            entries = self._versions.get(key, [])
            if not entries:
                return None
            if ts is None:
                return entries[-1][1]
            # bisect_right on the timestamps to find the latest ts <= query.
            tss = [t for t, _ in entries]
            idx = bisect.bisect_right(tss, ts)
            if idx == 0:
                return None
            return entries[idx - 1][1]

    def snapshot(self, ts: int) -> "Snapshot[V]":
        frozen: dict[str, V] = {}
        for key in list(self._versions.keys()):
            val = self.get(key, ts=ts)
            if val is not None:
                frozen[key] = val
        return Snapshot(frozen, ts)


class Snapshot(Generic[V]):
    def __init__(self, data: dict[str, V], ts: int) -> None:
        self._data = data
        self._ts = ts

    def get(self, key: str) -> V | None:
        return self._data.get(key)

    @property
    def ts(self) -> int:
        return self._ts
