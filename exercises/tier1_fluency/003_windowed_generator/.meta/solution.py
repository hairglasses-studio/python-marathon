from typing import Iterable, Iterator, TypeVar
from collections import deque

T = TypeVar("T")


def windows(seq: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    """Yield successive `size`-length tuples from `seq`."""
    it = iter(seq)
    window: deque = deque(maxlen=size)
    # Prime the window
    for _ in range(size):
        try:
            window.append(next(it))
        except StopIteration:
            return  # seq shorter than size → no windows
    yield tuple(window)
    # Slide: each new item pushes the oldest out (deque maxlen handles this)
    for item in it:
        window.append(item)
        yield tuple(window)
