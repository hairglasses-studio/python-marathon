from typing import TypeVar

T = TypeVar("T")


class ListIterator:
    def __init__(self, items: list[T]) -> None:
        self._items = items
        self._index = 0

    def next(self) -> T:
        raise NotImplementedError("fill me in")

    def get_state(self) -> dict:
        raise NotImplementedError("fill me in")

    def set_state(self, state: dict) -> None:
        raise NotImplementedError("fill me in")
