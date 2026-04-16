# Hints for Time-Travel KV Ledger

## Hint 1

This is a binary-search-on-sorted-array problem. Store each account's timestamps in a sorted list and maintain a parallel cumulative-sum list. To answer `balance_at(account, ts)`, find the rightmost timestamp <= ts using `bisect.bisect_right`, then index into the cumulative-sum list. This gives O(log n) queries without scanning all records.

## Hint 2

For `record(account, ts, delta)`:
- Append `ts` to `self._ts[account]`
- Compute the new cumulative sum: previous cumsum (last element, or 0 if empty) plus `delta`
- Append that to `self._cumsum[account]`

For `balance_at(account, ts)`:
- If `account` not in `self._ts` or list is empty: return 0
- Use `bisect.bisect_right(self._ts[account], ts)` to get index `i`
- If `i == 0`: no records yet at or before `ts`, return 0
- Otherwise return `self._cumsum[account][i - 1]`

## Hint 3

The query using bisect:

```python
import bisect

i = bisect.bisect_right(self._ts[account], ts)
if i == 0:
    return 0
return self._cumsum[account][i - 1]
```
