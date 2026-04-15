# Async Tool-Call Loop with Shared Budget

**Tier:** tier4_async
**Target time:** 30 minutes
**Topics:** asyncio, gather, retry, shared budget, lock, exception hierarchy

## Problem

Implement `invoke_all(calls, backend, budget, max_attempts, base_delay)` — the async analog of Warm-up 3 from `openai-devprod-2026-04-16.ipynb`.

**Requirements:**
- Each call runs concurrently and independently via the async backend.
- Per-call retry: up to `max_attempts` tries with exponential backoff (`base_delay * 2**(attempt-1)`).
- Shared `Budget` across all calls — each retry consumes 1 unit. If the budget hits zero, remaining retries should fail with `BudgetExhausted`.
- `RetryableError` → retry (consume budget first).
- `TerminalError` → immediate failure, no retry, no budget consumption.
- Unknown exceptions → propagate (your problem).
- Return `list[ToolResult]` in input order. Each result has `ok`, `value`/`error`, `attempts`.

**Composition:** This exercise combines exercises 027 (gather), 028 (retry), and the dataclass/exception patterns from Warm-up 3. If you solved those, this should feel like glue.

**Why this matters:** Tool-call loops with shared retry budgets are the core loop in modern LLM agent frameworks (including Codex). Gate 4 of Warm-up 3 in the canonical coding bank.

## How to run

```bash
python marathon.py run 031
```
