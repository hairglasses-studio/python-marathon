import asyncio
import random
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class RetryableError(Exception):
    """Transient error — worth retrying."""


class TerminalError(Exception):
    """Permanent error — stop retrying."""


async def retry(
    fn: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 1.0,
    jitter: float = 0.1,
) -> T:
    """Call fn() with exponential backoff + jitter on RetryableError.

    - RetryableError: wait and retry (backoff grows 2x each time, capped at max_delay)
    - TerminalError: raise immediately, no retry
    - Other exceptions: raise immediately
    - Exhausted attempts: raise the last RetryableError
    - Returns fn() result on first success
    """
    raise NotImplementedError("fill me in")
