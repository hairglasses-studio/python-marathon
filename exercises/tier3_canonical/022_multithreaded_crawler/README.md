# Multithreaded Web Crawler

**Tier:** tier3_canonical  
**Target time:** 45 minutes  
**Topics:** threading, BFS, ThreadPoolExecutor, graceful-shutdown

## Problem

Implement two web crawler classes that traverse a link graph starting from a seed URL.

### API

A `Fetcher` is a callable `(str) -> list[str]` that takes a URL and returns its outgoing links. Fetchers may raise exceptions (flaky network) — your crawler must handle this gracefully by skipping the failed URL.

**`Crawler`** — single-threaded BFS:
- `crawl(seed: str, *, max_pages: int = 100) -> set[str]` — return the set of URLs successfully fetched, starting BFS from `seed`. Stop after fetching `max_pages` URLs. Handle cycles in the link graph (don't re-fetch visited URLs). If a fetch raises an exception, skip that URL but continue crawling.

**`ThreadedCrawler`** — parallel version:
- `__init__(fetcher, *, workers: int = 4)` — accept a worker count.
- `crawl(seed: str, *, max_pages: int = 100) -> set[str]` — same contract as `Crawler.crawl`, but use `ThreadPoolExecutor` with the configured number of workers. The visited set must be thread-safe. Must actually be faster than sequential on I/O-bound fetchers. Must respect `max_pages` even under concurrent submissions (don't overshoot).

### Gates

**Gate 1** — single-threaded BFS, max_pages cap, flaky fetcher resilience  
**Gate 2** — threaded correctness, measured speedup on slow fetcher  
**Gate 3** — max_pages respected under parallelism (no overshoot)

## How to run

```bash
python marathon.py run 022
```

Edit `problem.py`. When `test_problem.py` passes, move on.
