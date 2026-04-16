# Notes for Budget-Aware Retry with Exponential Backoff

## Why this matters

Budget-aware retry with jittered exponential backoff is the industry-standard pattern for calling unreliable external services (APIs, databases, queues). It appears in virtually every production service client and is a common system design interview topic.

## Watch out for

- **TerminalError vs RetryableError hierarchy**: `BudgetExhausted` is a subclass of `TerminalError`. If you catch `TerminalError` before `RetryableError`, you'll correctly re-raise budget exhaustion without special-casing it.
- **Zero-budget edge case**: the spec says don't even call `fn` once if budget is 0. This is easy to miss.
- **Sleep injection**: always accept `sleep` as a parameter so tests can use a no-op. Never hardcode `time.sleep` inside the loop.

## Interview follow-ups

1. Why is jitter (randomness in backoff) important for distributed systems? What problem does it solve?
2. How would you add a total wall-clock timeout in addition to a retry count budget?
3. How would you make this work with async functions (`async def fn()`)?
