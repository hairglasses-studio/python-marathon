# Per-Key Locking (KeyedLocker)

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** threading, Lock, contextmanager  
**Source:** `openai-primitives-refresher.ipynb` cells 44-47

## Problem

## 5.3 Exercise — Per-key locking pattern

**Task:** Implement `KeyedLocker` that gives each key its own `threading.Lock`, created lazily on first request. Provide a context-manager method `lock(key)` that can be used as `with keyed.lock("some_key"):`.

**The pattern:**
1. Keep a dict `{key: Lock}`.
2. Use a *global* `Lock` (one, for the whole locker) to guard the dict itself — because dict lookups aren't atomic in the presence of concurrent writes.
3. In `lock(key)`:
   - acquire the global lock
   - look up or create the per-key lock
   - release the global lock
   - return a context manager that acquires/releases the per-key lock

**Why this matters:** Warm-up 2 (versioned KV) gate 3 is "make it thread-safe without serializing all operations through one big lock." Per-key locking is the idiomatic answer — readers/writers on different keys never block each other.

**Gotcha:** if you hold the global lock while acquiring the per-key lock, you've serialized everything. The global lock must be released before the per-key lock is acquired.

## How to run

```bash
python marathon.py run 016
```

Edit `problem.py`. When `test_problem.py` passes, move on.
