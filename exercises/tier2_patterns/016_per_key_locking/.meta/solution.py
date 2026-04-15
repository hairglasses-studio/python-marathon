import threading
from contextlib import contextmanager
from typing import Iterator


class KeyedLocker:
    def __init__(self) -> None:
        self._locks: dict[str, threading.Lock] = {}
        self._global = threading.Lock()

    def _lock_for(self, key: str) -> threading.Lock:
        # Minimize global-lock holding: only cover the dict lookup/insert.
        with self._global:
            if key not in self._locks:
                self._locks[key] = threading.Lock()
            return self._locks[key]

    @contextmanager
    def lock(self, key: str) -> Iterator[None]:
        lk = self._lock_for(key)
        lk.acquire()
        try:
            yield
        finally:
            lk.release()
