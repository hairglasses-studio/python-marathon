# Async Retry with Exponential Backoff + Jitter

**Tier:** tier4_async
**Target time:** 20 minutes
**Topics:** asyncio, retry, exponential backoff, jitter, exception hierarchy

## Problem

Implement an async `retry()` that wraps a coroutine factory and retries on `RetryableError`.

**Behavior:**
- `RetryableError` → wait and retry. Delay doubles each attempt: `base_delay * 2**attempt`, capped at `max_delay`. Add `random.uniform(0, jitter)` to the delay.
- `TerminalError` → re-raise immediately. No retry.
- Other exceptions → re-raise (not your problem).
- Exhaust `max_attempts` → raise the last `RetryableError`.
- On first success, return the result.

**Signature:**

```python
async def retry(
    fn: Callable[[], Awaitable[T]],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 1.0,
    jitter: float = 0.1,
) -> T:
```

**Why this matters:** Warm-up 3 of the OpenAI coding round is a synchronous version of this exact problem. Gate 4 asks for an async variant. This exercise IS that gate 4.

## How to run

```bash
python marathon.py run 028
```
