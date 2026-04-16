# Hints for Multithreaded Web Crawler

## Hint 1

Gate 1 is BFS: use a `deque` as your frontier and a `set` as your visited tracker. The tricky part is respecting `max_pages` — stop enqueuing new URLs once `len(visited)` hits the cap, and don't count URLs that fail to fetch. Gate 2 moves to `ThreadPoolExecutor`; the visited set must be protected by a `threading.Lock` because multiple threads update it concurrently. Gate 3 is about not overshooting `max_pages` under concurrency — check the cap before submitting new work, under the lock.

## Hint 2

- Gate 1 `Crawler.crawl`: `from collections import deque`; `queue = deque([seed])`; loop while `queue` and `len(visited) < max_pages`; wrap `self._fetch(url)` in try/except and skip on error.
- Gate 2 `ThreadedCrawler.crawl`: use a `threading.Lock` to guard both `visited` and the submission of new futures; submit with `executor.submit(self._fetch, url)` inside `ThreadPoolExecutor`.
- Gate 3: check `len(visited) < max_pages` under the lock *before* submitting each new URL, so in-flight tasks can't push the count past the cap.
- Use `as_completed(futures)` to process results as they arrive, not in submission order.

## Hint 3

Thread-safe visited check and cap enforcement:

```python
lock = threading.Lock()
visited: set[str] = set()
futures: dict[Future, str] = {}

with ThreadPoolExecutor(max_workers=self._workers) as ex:
    with lock:
        visited.add(seed)
        futures[ex.submit(self._fetch, seed)] = seed
    for fut in as_completed(futures):
        try:
            links = fut.result()
        except Exception:
            continue
        with lock:
            for url in links:
                if url not in visited and len(visited) < max_pages:
                    visited.add(url)
                    futures[ex.submit(self._fetch, url)] = url
```
