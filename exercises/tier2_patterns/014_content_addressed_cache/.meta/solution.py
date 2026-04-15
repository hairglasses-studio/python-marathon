import hashlib
from typing import Any, Callable


class ContentCache:
    def __init__(self) -> None:
        self._cache: dict[str, Any] = {}
        self._miss_count = 0
        self._hit_count = 0

    def _key(self, name: str, inputs: dict) -> str:
        canonical = name + "|" + repr(sorted(inputs.items()))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def compute(
        self,
        name: str,
        inputs: dict,
        fn: Callable[[dict], Any],
    ) -> Any:
        key = self._key(name, inputs)
        if key in self._cache:
            self._hit_count += 1
            return self._cache[key]
        self._miss_count += 1
        result = fn(inputs)
        self._cache[key] = result
        return result

    def stats(self) -> tuple[int, int]:
        return self._hit_count, self._miss_count
