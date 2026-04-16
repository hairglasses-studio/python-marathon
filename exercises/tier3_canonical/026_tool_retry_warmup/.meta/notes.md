# Notes for Tool-Call Loop with Retry + Budget (Warm-up 3)

## Why this matters

Every LLM agent framework, RPC client, and API SDK has a retry loop at its core. This exercise captures the exact loop that Codex, LangChain, and similar systems implement: classify errors, backoff, respect server hints (retry_after), and bound total spend via a shared budget. Interviewers at developer tooling companies treat this as a near-guarantee question because it mirrors the product's own implementation.

## Watch out for

- `BudgetExhausted` is a subclass of `TerminalError`, so if you catch `TerminalError` first in a broad except clause, you'll never see `BudgetExhausted` separately. Catch specific subtypes in order (most specific first) or check `isinstance`.
- Jitter must be added *on top of* the exponential backoff delay, not replace it. Forgetting jitter means all retrying clients back off in lockstep, causing thundering herd when the server recovers.

## Interview follow-ups

- "How would you make the budget shared across concurrent async calls?" — replace `budget.consume()` with an `async def consume()` that acquires an `asyncio.Lock` before decrementing; see exercise 031.
- "How would you implement circuit-breaking on top of this?" — track consecutive failure count per backend; once it exceeds a threshold, fail-fast without calling the backend until a probe succeeds.
- "What's the maximum total sleep time this function could impose?" — `sum(min(base_delay * 2**i, max_delay) + jitter for i in range(attempts - 1))`; important to bound for latency SLAs.
