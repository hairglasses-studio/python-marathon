# Notes for Multithreaded Web Crawler

## Why this matters

BFS + thread pool + shared visited set is the exact pattern behind real web crawlers, link checkers, and distributed build systems. In interviews it tests whether you understand GIL limitations (I/O-bound workloads benefit from threads), thread-safe data structures, and how to bound concurrent work.

## Watch out for

- Race condition on the visited set: two threads can both see a URL as "not visited" and both submit it, causing double-fetch and potentially exceeding `max_pages`. Always check-and-add under the same lock acquisition.
- Submitting futures from inside `as_completed` requires keeping the executor alive for the duration — the `with ThreadPoolExecutor(...) as ex:` block must wrap the entire loop, not just the initial submission.

## Interview follow-ups

- "How would you add a per-domain rate limit?" — maintain a `dict[str, threading.Semaphore]` keyed by hostname; acquire before fetching, release after.
- "How would you make this truly distributed across machines?" — replace the in-process queue with a Redis list or Kafka topic; use distributed locking (e.g., Redis `SET NX`) for the visited set.
- "What changes if the fetcher is async instead of blocking?" — replace `ThreadPoolExecutor` with `asyncio.gather` + `asyncio.Semaphore`; the visited-set lock becomes `asyncio.Lock`.
