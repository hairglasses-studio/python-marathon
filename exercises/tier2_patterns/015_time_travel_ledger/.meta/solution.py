import bisect
from collections import defaultdict


class Ledger:
    def __init__(self) -> None:
        # Per-account sorted timestamps and cumulative sums.
        self._ts: dict[str, list[int]] = defaultdict(list)
        self._cumsum: dict[str, list[int]] = defaultdict(list)

    def record(self, account: str, ts: int, delta: int) -> None:
        ts_list = self._ts[account]
        cum = self._cumsum[account]
        running = (cum[-1] if cum else 0) + delta
        ts_list.append(ts)
        cum.append(running)

    def balance_at(self, account: str, ts: int) -> int:
        ts_list = self._ts.get(account, [])
        cum = self._cumsum.get(account, [])
        if not ts_list:
            return 0
        # bisect_right gives insertion point AFTER equals; we want the
        # index of the latest entry with timestamp <= ts.
        idx = bisect.bisect_right(ts_list, ts)
        if idx == 0:
            return 0
        return cum[idx - 1]
