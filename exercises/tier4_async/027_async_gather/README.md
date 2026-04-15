# Async Gather — Bounded Concurrency

**Tier:** tier4_async
**Target time:** 15 minutes
**Topics:** asyncio, gather, Semaphore, bounded concurrency

## Problem

Implement `fetch_all(urls, fetcher, concurrency=10)` that fetches all URLs in parallel, but caps the number of in-flight fetches at `concurrency`. Returns results in input order. Raises the first exception from any fetch.

**Signature:**

```python
async def fetch_all(
    urls: list[str],
    fetcher: Callable[[str], Awaitable[T]],
    *,
    concurrency: int = 10,
) -> list[T]:
```

**Constraints:**

- Do not launch more than `concurrency` coroutines at a time.
- Order of returned results must match order of input URLs.
- On any exception, the overall call raises (no silent swallowing).

**Why this matters:** openai.md §12.4 notes that async is interview-fair-game. `asyncio.gather` + `Semaphore` is the canonical pattern for bounded parallel I/O — needed for any async web crawler, tool-call fanout, or batch API client.

## How to run

```bash
python marathon.py run 027
```
