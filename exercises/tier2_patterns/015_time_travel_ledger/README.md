# Time-Travel KV Ledger

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** bisect, defaultdict, cumulative-sum  
**Source:** `openai-primitives-refresher.ipynb` cells 35-38

## Problem

## 4.2 Exercise — Time-travel KV query

**Task:** Implement `Ledger` that tracks balances by `(account, timestamp, delta)` and supports `balance_at(account, ts)` — return the balance for `account` as of time `ts` (or `0` if no entries yet).

**Requirements:**
- `record(account, ts, delta)` — append a change; assume timestamps are monotonically increasing *per account* (you don't need to sort).
- `balance_at(account, ts)` — sum of all deltas for `account` where `timestamp <= ts`, in **O(log n)** per query (you need `bisect`).

**Hint:** store a parallel list of cumulative sums. Given an account's cumulative-sum array `cumsum` and its sorted timestamps `ts_list`, `balance_at(ts)` becomes `cumsum[bisect_right(ts_list, ts) - 1]`.

**Why this pattern matters:** any ledger, time-series store, or versioned KV uses exactly this trick to answer time-range queries in log time instead of linear.

## How to run

```bash
python marathon.py run 015
```

Edit `problem.py`. When `test_problem.py` passes, move on.
