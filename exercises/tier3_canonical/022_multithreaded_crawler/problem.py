"""Crawler scaffold — implement the crawl() method."""
from __future__ import annotations

import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import Callable

Fetcher = Callable[[str], list[str]]


class Crawler:
    def __init__(self, fetcher: Fetcher) -> None:
        self._fetch = fetcher

    def crawl(self, seed: str, *, max_pages: int = 100) -> set[str]:
        """Return the set of URLs successfully fetched."""
        raise NotImplementedError("gate 1")


class ThreadedCrawler:
    def __init__(self, fetcher: Fetcher, *, workers: int = 4) -> None:
        self._fetch = fetcher
        self._workers = workers

    def crawl(self, seed: str, *, max_pages: int = 100) -> set[str]:
        """Parallel version using ThreadPoolExecutor. Thread-safe visited set."""
        raise NotImplementedError("gates 2-3")
