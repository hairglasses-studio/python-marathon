from contextlib import contextmanager
from typing import Any, Iterator

_SENTINEL = object()


@contextmanager
def temp_attr(obj: Any, name: str, value: Any) -> Iterator[None]:
    # Capture the original state — either the current value or a sentinel
    # meaning "the attribute didn't exist."
    original = getattr(obj, name, _SENTINEL)
    setattr(obj, name, value)
    try:
        yield
    finally:
        if original is _SENTINEL:
            delattr(obj, name)
        else:
            setattr(obj, name, original)
