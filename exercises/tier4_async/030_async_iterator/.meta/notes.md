# Notes for Async Iterator Protocol — AsyncBatcher

## Why this matters

The async iterator protocol (`__aiter__` / `__anext__` / `StopAsyncIteration`) is the async twin of the sync protocol and powers `async for` loops throughout Python's async ecosystem — streaming HTTP responses, database cursors, message queue consumers. Batching is the most common transformation applied to async streams before passing data to downstream processors.

## Watch out for

- `__aiter__` must return `self` (not a new object) so that `async for` can call `__anext__` on the same instance across iterations. Forgetting this breaks the protocol silently if the caller only iterates once but loudly if they try to reuse the iterator.
- When the source exhausts mid-batch, you must yield the partial batch first and then raise `StopAsyncIteration` on the next call. If you raise `StopAsyncIteration` as soon as the source is exhausted without flushing the partial batch, you silently drop trailing items.

## Interview follow-ups

- "How would you implement a timeout on each `__anext__` call?" — wrap `await source.__anext__()` with `asyncio.wait_for(..., timeout=seconds)`; catch `asyncio.TimeoutError` and raise `StopAsyncIteration` or propagate as appropriate.
- "What's the difference between an async generator and a class implementing this protocol?" — an `async def __anext__` class gives you explicit state and `close()`/`athrow()` control; an `async def` function with `yield` (async generator) is more concise but less customizable.
- "How would you add a `peek()` method that returns the next item without consuming it?" — buffer one item in `__init__`; `peek()` returns the buffer; `__anext__` pops the buffer and refills it.
