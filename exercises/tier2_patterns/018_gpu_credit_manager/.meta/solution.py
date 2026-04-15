import heapq
import itertools
from collections import defaultdict


class InsufficientCredits(Exception):
    pass


class CreditManager:
    def __init__(self) -> None:
        self._heaps: dict[str, list[tuple[int, int, int]]] = defaultdict(list)
        self._seq = itertools.count()

    def add(self, user: str, amount: int, expiry_ts: int) -> None:
        if amount <= 0:
            return
        heapq.heappush(
            self._heaps[user],
            (expiry_ts, next(self._seq), amount),
        )

    def _drop_expired(self, user: str, now_ts: int) -> None:
        heap = self._heaps[user]
        while heap and heap[0][0] < now_ts:
            heapq.heappop(heap)

    def balance(self, user: str, now_ts: int) -> int:
        self._drop_expired(user, now_ts)
        return sum(amount for _, _, amount in self._heaps[user])

    def deduct(self, user: str, amount: int, now_ts: int) -> None:
        if self.balance(user, now_ts) < amount:
            raise InsufficientCredits(
                f"user {user} has insufficient credits at ts={now_ts}"
            )
        heap = self._heaps[user]
        remaining = amount
        while remaining > 0 and heap:
            expiry, seq, chunk = heapq.heappop(heap)
            if expiry < now_ts:
                continue
            take = min(chunk, remaining)
            remaining -= take
            leftover = chunk - take
            if leftover > 0:
                heapq.heappush(heap, (expiry, seq, leftover))
