# Notes for Async Queue — Worker Pool Pipeline

## Why this matters

Producer-consumer with a bounded async queue is the backbone of most async I/O pipelines: web crawlers, batch LLM inference runners, and streaming ETL systems all use this pattern. `asyncio.Queue` + sentinel is the canonical Python idiom, and returning results in input order (not completion order) is the common production requirement that catches naive implementations.

## Watch out for

- Results arrive in completion order, not input order. To preserve input order, enqueue `(index, item)` tuples and write results into a pre-allocated list by index, or collect `(index, result)` pairs and sort before returning.
- Workers must drain cleanly: if you use a sentinel value (e.g., `None`) to signal shutdown, enqueue exactly `num_workers` sentinels — one per worker — so every worker sees exactly one and exits. Alternatively, use `queue.join()` + `task.cancel()` after all items are enqueued.

## Interview follow-ups

- "How would you add backpressure so the producer doesn't enqueue faster than workers can consume?" — use `asyncio.Queue(maxsize=N)` which blocks `await queue.put(item)` when full.
- "How would you handle a worker that raises an exception mid-item?" — catch inside the worker, store `(index, exception)` in the result slot, and re-raise or return an error sentinel after all items complete.
- "How does this differ from `asyncio.gather`?" — `gather` fans out a fixed list of coroutines; queue-based workers are better when items arrive dynamically or the total count is unknown upfront.
