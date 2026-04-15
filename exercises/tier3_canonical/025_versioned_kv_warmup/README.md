# Versioned Key-Value Store (Warm-up 2)

**Tier:** tier3_canonical  
**Target time:** 45 minutes  
**Topics:** bisect, time-travel, snapshot-isolation, threading, 4-gate  
**Source:** `openai-devprod-2026-04-16.ipynb` cells 18-21

## Problem

## Warm-up 2 — Versioned Key-Value Store

**Why:** build caches and incremental state stores look exactly like this.

`set(key, value)` records a new version at the current monotonic timestamp. `get(key, ts)` returns the value at time `ts` (the latest version with timestamp ≤ `ts`).

### The four gates

1. **Gate 1 — single-key set/get.** Back it with a `defaultdict(list)` of `(ts, value)` entries.
2. **Gate 2 — `bisect.bisect_right` for O(log n) time query.** This is the idiomatic answer — shows you avoid linear scans.
3. **Gate 3 — thread-safe concurrent access.** `threading.RLock` per key (lazy init).
4. **Gate 4 — snapshot isolation.** `snapshot(ts)` returns a frozen read-only view that doesn't observe writes after `ts`.

## How to run

```bash
python marathon.py run 025
```

Edit `problem.py`. When `test_problem.py` passes, move on.
