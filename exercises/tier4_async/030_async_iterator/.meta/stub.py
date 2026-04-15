from typing import AsyncIterator, TypeVar

T = TypeVar("T")


class AsyncBatcher:
    """Async iterator that groups items from a source into fixed-size batches.

    Wraps an async iterator and yields lists of up to `batch_size` items.
    The final batch may be smaller if the source exhausts mid-batch.
    Implements the async iterator protocol: `__aiter__` + `__anext__`.
    """

    def __init__(
        self,
        source: AsyncIterator[T],
        batch_size: int,
    ) -> None:
        raise NotImplementedError("fill me in")

    def __aiter__(self) -> "AsyncBatcher":
        raise NotImplementedError("fill me in")

    async def __anext__(self) -> list[T]:
        raise NotImplementedError("fill me in")
