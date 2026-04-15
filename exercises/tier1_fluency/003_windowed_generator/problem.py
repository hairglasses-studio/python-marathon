from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")

def windows(seq: Iterable[T], size: int) -> Iterator[tuple[T, ...]]:
    raise NotImplementedError("fill me in")
