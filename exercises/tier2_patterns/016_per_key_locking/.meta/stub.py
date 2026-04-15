import threading
from contextlib import contextmanager
from typing import Iterator

class KeyedLocker:
    def __init__(self) -> None:
        self._locks: dict[str, threading.Lock] = {}
        self._global = threading.Lock()

    @contextmanager
    def lock(self, key: str) -> Iterator[None]:
        raise NotImplementedError("fill me in")
