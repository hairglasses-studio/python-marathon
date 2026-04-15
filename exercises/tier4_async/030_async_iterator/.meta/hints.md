# Hints

## Hint 1

The async iterator protocol: `__aiter__` returns self (unchanged from sync). `__anext__` is a coroutine — it's `async def` and should `await` the source. When you run out, raise `StopAsyncIteration`.

## Hint 2

In `__anext__`, accumulate items until you hit `batch_size` or the source raises `StopAsyncIteration`. If you caught `StopAsyncIteration` mid-batch, return the partial batch this call and set a flag so the NEXT call raises `StopAsyncIteration` itself.

## Hint 3

```python
async def __anext__(self) -> list[T]:
    if self._exhausted:
        raise StopAsyncIteration
    batch = []
    while len(batch) < self.batch_size:
        try:
            batch.append(await self.source.__anext__())
        except StopAsyncIteration:
            self._exhausted = True
            break
    if not batch:
        raise StopAsyncIteration
    return batch
```
