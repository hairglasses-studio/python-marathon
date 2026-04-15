class IntRange:
    def __init__(self, start: int, stop: int) -> None:
        self.start = start
        self.stop = stop

    def __len__(self) -> int:
        return max(0, self.stop - self.start)

    def __iter__(self):
        current = self.start
        while current < self.stop:
            yield current
            current += 1

    def __contains__(self, item) -> bool:
        # O(1) — no need to iterate
        if not isinstance(item, int):
            return False
        return self.start <= item < self.stop

    def __repr__(self) -> str:
        return f"IntRange({self.start}, {self.stop})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, IntRange):
            return NotImplemented
        return self.start == other.start and self.stop == other.stop

    def __hash__(self) -> int:
        return hash((self.start, self.stop))
