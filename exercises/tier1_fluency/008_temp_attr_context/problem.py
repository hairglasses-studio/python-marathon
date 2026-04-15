from contextlib import contextmanager
from typing import Any, Iterator

_SENTINEL = object()

@contextmanager
def temp_attr(obj: Any, name: str, value: Any) -> Iterator[None]:
    raise NotImplementedError("fill me in")
