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
    """Process items through a worker pool using asyncio.Queue.

    Spawns `num_workers` worker tasks that pull items from a queue, process
    them, and store results. Returns results in input order. All workers
    must exit cleanly when the queue drains — use a sentinel (None) or
    call `queue.join()` and `task.cancel()`.
    """
    raise NotImplementedError("fill me in")
