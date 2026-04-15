import bisect
from collections import defaultdict

class Ledger:
    def __init__(self) -> None:
        self._ts: dict[str, list[int]] = defaultdict(list)
        self._cumsum: dict[str, list[int]] = defaultdict(list)

    def record(self, account: str, ts: int, delta: int) -> None:
        raise NotImplementedError("fill me in")

    def balance_at(self, account: str, ts: int) -> int:
        raise NotImplementedError("fill me in")
