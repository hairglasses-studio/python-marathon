import hashlib
from typing import Any, Callable

class ContentCache:
    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}
        self._miss_count = 0
        self._hit_count = 0

    def compute(
        self,
        name: str,
        inputs: dict,
        fn: Callable[[dict], Any],
    ) -> Any:
        raise NotImplementedError("fill me in")

    def stats(self) -> tuple[int, int]:
        return self._hit_count, self._miss_count
