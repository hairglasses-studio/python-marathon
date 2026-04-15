# Async Iterator Protocol — AsyncBatcher

**Tier:** tier4_async
**Target time:** 20 minutes
**Topics:** async iterator protocol, `__aiter__`, `__anext__`, `StopAsyncIteration`

## Problem

Implement `AsyncBatcher(source, batch_size)` — an async iterator that wraps an async iterator and yields lists of up to `batch_size` items. Final batch may be smaller if the source exhausts mid-batch.

**Requirements:**
- Implement the async iterator protocol: `__aiter__(self) -> self` and `async def __anext__(self) -> list[T]`.
- `async for batch in AsyncBatcher(src, 3):` should yield batches of 3.
- Raise `StopAsyncIteration` when the source is exhausted and no partial batch remains.
- Empty source → no iterations (immediate `StopAsyncIteration`).

**Why this matters:** The async iterator protocol is the async twin of the sync iterator protocol. Mirror of exercise 020 (`ResumableRange`). Gate 4 of the canonical resumable iterator problem in `openai.md` §12.4.

## How to run

```bash
python marathon.py run 030
```
