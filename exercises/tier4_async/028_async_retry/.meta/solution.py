import asyncio
import random
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


class RetryableError(Exception):
    pass


class TerminalError(Exception):
    pass


async def retry(
    fn: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 1.0,
    jitter: float = 0.1,
) -> T:
    last_err: RetryableError | None = None
    for attempt in range(max_attempts):
        try:
            return await fn()
        except TerminalError:
            raise
        except RetryableError as e:
            last_err = e
            if attempt == max_attempts - 1:
                break
            delay = min(base_delay * (2 ** attempt), max_delay)
            delay += random.uniform(0, jitter)
            await asyncio.sleep(delay)
    assert last_err is not None
    raise last_err
