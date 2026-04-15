from typing import AsyncIterator, TypeVar

T = TypeVar("T")


class AsyncBatcher:
    def __init__(
        self,
        source: AsyncIterator[T],
        batch_size: int,
    ) -> None:
        self.source = source
        self.batch_size = batch_size
        self._exhausted = False

    def __aiter__(self) -> "AsyncBatcher":
        return self

    async def __anext__(self) -> list[T]:
        if self._exhausted:
            raise StopAsyncIteration
        batch: list[T] = []
        while len(batch) < self.batch_size:
            try:
                item = await self.source.__anext__()
            except StopAsyncIteration:
                self._exhausted = True
                break
            batch.append(item)
        if not batch:
            raise StopAsyncIteration
        return batch
