# Notes for Time-Travel KV Ledger

## Why this matters

Time-range queries with O(log n) lookup appear in financial ledgers, time-series databases (InfluxDB, Prometheus), versioned key-value stores, and any system that needs to reconstruct state at a past point in time. The bisect + cumulative-sum pattern is the go-to solution at interview scale.

## Watch out for

- **bisect_right vs bisect_left**: you want the rightmost index <= ts, so `bisect_right(ts_list, ts) - 1`. Using `bisect_left` would exclude entries at exactly `ts`.
- **Empty list edge case**: if no entries exist for an account, `balance_at` must return 0 without indexing into an empty list.

## Interview follow-ups

1. How would you support out-of-order insertions (timestamps not guaranteed monotonically increasing)?
2. How would you extend this to support range queries: sum of deltas between `ts_start` and `ts_end`?
3. What's the memory trade-off of storing cumulative sums vs recomputing them on each query?
