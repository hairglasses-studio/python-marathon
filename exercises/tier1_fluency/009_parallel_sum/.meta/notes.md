# Notes for Parallel Sum with ThreadPoolExecutor

## Why this matters

`ThreadPoolExecutor` is Python's standard interface for I/O-bound parallelism and the map-reduce decomposition pattern. It appears in batch API calls, parallel file processing, and any pipeline stage that can be chunked and farmed out. Understanding when threads help (I/O-bound) vs. when they don't (CPU-bound with the GIL) is a recurring interview topic.

## Watch out for

- For CPU-bound work like pure arithmetic, threads in Python do not run in true parallel due to the Global Interpreter Lock (GIL); this exercise uses threading for illustration — in production, `ProcessPoolExecutor` would give actual CPU parallelism for CPU-bound summing
- Passing `sum` directly as the callable to `pool.map` works cleanly since `sum` accepts an iterable; you do not need to wrap it in a lambda

## Interview follow-ups

- "When would you use `ProcessPoolExecutor` instead of `ThreadPoolExecutor`, and why?"
- "What does `pool.map` do differently from `pool.submit` in a loop? When would you prefer `submit`?"
- "How would you add a timeout so that if any chunk takes longer than N seconds, the whole operation fails fast?"
