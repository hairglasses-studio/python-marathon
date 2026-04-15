from __future__ import annotations

import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

Fetcher = Callable[[str], list[str]]


class Crawler:
    """Single-threaded BFS crawler."""

    def __init__(self, fetcher: Fetcher) -> None:
        self._fetch = fetcher

    def crawl(self, seed: str, *, max_pages: int = 100) -> set[str]:
        visited: set[str] = set()
        queue: deque[str] = deque([seed])

        while queue and len(visited) < max_pages:
            url = queue.popleft()
            if url in visited:
                continue

            try:
                links = self._fetch(url)
            except Exception:
                # Skip failed fetch — don't mark as visited either
                continue

            visited.add(url)
            for link in links:
                if link not in visited:
                    queue.append(link)

        return visited


class ThreadedCrawler:
    """Thread-pool BFS crawler with lock-guarded visited set."""

    def __init__(self, fetcher: Fetcher, *, workers: int = 4) -> None:
        self._fetch = fetcher
        self._workers = workers

    def crawl(self, seed: str, *, max_pages: int = 100) -> set[str]:
        visited: set[str] = set()
        in_flight: set[str] = set()
        visited_lock = threading.Lock()

        def _claim(url: str) -> bool:
            """Atomically reserve a URL for fetching."""
            with visited_lock:
                if url in visited or url in in_flight:
                    return False
                if len(visited) + len(in_flight) >= max_pages:
                    return False
                in_flight.add(url)
                return True

        def _finish(url: str, links: list[str]) -> list[str]:
            """Commit a fetched URL and return the new URLs to enqueue."""
            with visited_lock:
                in_flight.discard(url)
                visited.add(url)
                new_work: list[str] = []
                for link in links:
                    if (
                        link not in visited
                        and link not in in_flight
                        and len(visited) + len(in_flight) < max_pages
                    ):
                        new_work.append(link)
                return new_work

        with ThreadPoolExecutor(max_workers=self._workers) as pool:
            # Seed the first fetch
            if not _claim(seed):
                return set()
            futures: dict = {pool.submit(self._fetch, seed): seed}

            while futures:
                done = [f for f in list(futures) if f.done()]
                if not done:
                    # Block on the next completion.
                    done = [next(as_completed(futures))]

                for future in done:
                    url = futures.pop(future)
                    try:
                        links = future.result()
                    except Exception:
                        with visited_lock:
                            in_flight.discard(url)
                        continue

                    new_work = _finish(url, links)
                    for link in new_work:
                        if _claim(link):
                            futures[pool.submit(self._fetch, link)] = link

        return visited
