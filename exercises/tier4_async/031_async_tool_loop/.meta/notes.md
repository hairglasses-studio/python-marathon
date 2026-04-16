# Notes for Async Tool-Call Loop with Shared Budget

## Why this matters

This is the async culmination of the entire tier4 sequence: it combines `asyncio.gather` (027), async retry with backoff (028), and the error-classification + budget pattern from Warm-up 3 (026). Modern LLM agent frameworks (Codex, LangChain, Autogen) implement exactly this loop — concurrent tool calls, per-call retry, shared retry budget — as their core execution engine.

## Watch out for

- The shared `Budget` is accessed concurrently by all in-flight coroutines. `Budget.consume()` must acquire an `asyncio.Lock` (not a `threading.Lock`) before checking and decrementing `_used`. Forgetting the lock causes a race where two coroutines both see budget remaining and both decrement past zero.
- `TerminalError` must not consume budget — only `RetryableError` retries consume it. A common mistake is calling `budget.consume()` at the top of every attempt loop rather than only on the retry path.

## Interview follow-ups

- "How would you add a per-call timeout on top of the retry budget?" — wrap each `await backend(call)` with `asyncio.wait_for(..., timeout=T)`; treat `asyncio.TimeoutError` as a `RetryableError`.
- "How would you expose live progress (which calls are in-flight, which have succeeded)?" — use `asyncio.Queue` to stream `(call_index, status)` events; a separate coroutine consumes and renders the progress.
- "What happens if the event loop is shared with other tasks during `invoke_all`?" — `asyncio.gather` yields control on every `await`, so other tasks run between retries; the shared budget lock ensures correctness but does not starve other tasks.
