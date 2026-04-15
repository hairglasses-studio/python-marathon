import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


async def fetch_all(
    urls: list[str],
    fetcher: Callable[[str], Awaitable[T]],
    *,
    concurrency: int = 10,
) -> list[T]:
    """Fetch all URLs concurrently, capped at `concurrency` in flight.

    Preserves input order in the returned list. Raises the first exception
    encountered from any fetch.
    """
    raise NotImplementedError("fill me in")
