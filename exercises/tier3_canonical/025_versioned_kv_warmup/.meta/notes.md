# Notes for Versioned Key-Value Store (Warm-up 2)

## Why this matters

Versioned KV stores are the storage primitive behind MVCC databases (Postgres, CockroachDB), build caches, and any system that needs time-travel queries or snapshot isolation. Knowing that `bisect.bisect_right` gives O(log n) point-in-time lookup is a specific, signal-rich answer that distinguishes senior engineers from juniors who reach for a linear scan.

## Watch out for

- `bisect_right` returns the index *after* the last entry with `ts <= query_ts`, so you want `idx - 1`. If `idx == 0` there's no version at or before `ts` — return `None`, not `entries[0]`.
- Per-key lock initialization must itself be atomic: two threads calling `set` on the same new key simultaneously will both try to create a lock. Use a global lock to guard the lock-creation step, not the value write.

## Interview follow-ups

- "What's the memory growth behavior of this store?" — unbounded: every `set` adds a new version. In production you'd add compaction (delete versions older than some retention horizon) or use a limit per key.
- "How would you implement `delete(key, ts)`?" — append a tombstone sentinel at `ts`; `get` returns `None` if the latest version at or before `ts` is a tombstone.
- "How does this relate to MVCC in databases?" — MVCC keeps old row versions to serve concurrent readers at older timestamps without blocking writers; GC (vacuum in Postgres) removes versions no reader can still see, analogous to compaction here.
