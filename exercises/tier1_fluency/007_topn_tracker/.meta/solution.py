import heapq


class TopN:
    def __init__(self, n: int) -> None:
        self._n = n
        self._heap: list[int] = []   # min-heap of size ≤ n

    def add(self, value: int) -> None:
        if len(self._heap) < self._n:
            heapq.heappush(self._heap, value)
        elif value > self._heap[0]:
            heapq.heapreplace(self._heap, value)

    def top(self) -> list[int]:
        return sorted(self._heap, reverse=True)
