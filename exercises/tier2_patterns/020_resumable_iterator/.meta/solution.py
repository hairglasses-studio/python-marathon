from typing import TypeVar

T = TypeVar("T")


class ListIterator:
    def __init__(self, items: list[T]) -> None:
        self._items = items
        self._index = 0

    def next(self) -> T:
        if self._index >= len(self._items):
            raise StopIteration
        value = self._items[self._index]
        self._index += 1
        return value

    def get_state(self) -> dict:
        # Minimal state to reconstruct position. Not including `items` keeps
        # the snapshot small — the iterator and the state are paired.
        return {"index": self._index}

    def set_state(self, state: dict) -> None:
        idx = state["index"]
        if not (0 <= idx <= len(self._items)):
            raise ValueError(f"index {idx} out of range")
        self._index = idx
