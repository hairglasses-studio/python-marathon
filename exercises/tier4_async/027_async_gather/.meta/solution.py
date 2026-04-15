import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


async def fetch_all(
    urls: list[str],
    fetcher: Callable[[str], Awaitable[T]],
    *,
    concurrency: int = 10,
) -> list[T]:
    semaphore = asyncio.Semaphore(concurrency)

    async def bounded(url: str) -> T:
        async with semaphore:
            return await fetcher(url)

    # asyncio.gather preserves order and raises the first exception.
    return await asyncio.gather(*(bounded(u) for u in urls))
