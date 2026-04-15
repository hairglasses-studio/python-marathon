import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")
R = TypeVar("R")


async def pipeline(
    items: list[T],
    process: Callable[[T], Awaitable[R]],
    *,
    num_workers: int = 4,
) -> list[R]:
    if not items:
        return []

    queue: asyncio.Queue = asyncio.Queue()
    results: list = [None] * len(items)

    async def worker():
        while True:
            task = await queue.get()
            if task is None:
                queue.task_done()
                return
            idx, item = task
            try:
                results[idx] = await process(item)
            finally:
                queue.task_done()

    # Enqueue items with their original index
    for i, item in enumerate(items):
        await queue.put((i, item))
    # One sentinel per worker
    for _ in range(num_workers):
        await queue.put(None)

    workers = [asyncio.create_task(worker()) for _ in range(num_workers)]
    await asyncio.gather(*workers)
    return results
