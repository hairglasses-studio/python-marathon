import heapq
import itertools
from collections import defaultdict

class InsufficientCredits(Exception):
    pass


class CreditManager:
    def __init__(self) -> None:
        # per-user heap of (expiry_ts, seq, amount)
        self._heaps: dict[str, list[tuple[int, int, int]]] = defaultdict(list)
        self._seq = itertools.count()

    def add(self, user: str, amount: int, expiry_ts: int) -> None:
        raise NotImplementedError("fill me in")

    def deduct(self, user: str, amount: int, now_ts: int) -> None:
        raise NotImplementedError("fill me in")

    def balance(self, user: str, now_ts: int) -> int:
        raise NotImplementedError("fill me in")
