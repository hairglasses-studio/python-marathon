# Hints for GPU Credit Manager with Expiry

## Hint 1

This is a priority-queue (min-heap) problem. Use Python's `heapq` module to maintain a per-user heap ordered by expiry timestamp. Credits that expire soonest should be consumed first (greedy). Expiry is handled lazily: don't sweep the heap on every operation — only discard expired entries when you pop them during `deduct` or `balance`.

## Hint 2

- `add(user, amount, expiry_ts)`: push `(expiry_ts, seq, amount)` onto `self._heaps[user]` using `heapq.heappush`. The `seq` from `itertools.count()` breaks ties and prevents comparison errors on non-comparable types.
- `balance(user, now_ts)`: iterate a copy of the heap (or pop/push), summing amounts where `expiry_ts > now_ts`. Simpler: use a helper that pops expired entries and sums the rest.
- `deduct(user, amount, now_ts)`: first compute how much unexpired credit exists; if < `amount`, raise `InsufficientCredits` without modifying the heap. Otherwise pop from the heap (skipping expired), reduce amount until satisfied, push back any remainder.

## Hint 3

The lazy-expiry pop pattern inside deduct:

```python
heap = self._heaps[user]
while heap:
    expiry, seq, credits = heap[0]
    if expiry <= now_ts:       # expired: discard lazily
        heapq.heappop(heap)
        continue
    break                      # soonest-expiring unexpired bucket is at heap[0]
```
