# Budget-Aware Retry with Exponential Backoff

**Tier:** tier2_patterns  
**Target time:** 25 minutes  
**Topics:** retry, backoff, jitter, exceptions  
**Source:** `openai-primitives-refresher.ipynb` cells 61-64

## Problem

## 8.2 Exercise — Budget-aware retry with exponential backoff + jitter

**Task:** Implement `retry(fn, *, budget, backoff, sleep)` that:
- Calls `fn()` repeatedly
- Catches `RetryableError` → sleeps `backoff(attempt)` and retries
- Catches `TerminalError` → immediately raises
- Tracks attempts against `budget` → raises `BudgetExhausted` when exceeded
- On success, returns the value from `fn`

**Constraints:**
- Use dependency injection for `sleep` (so tests can pass a no-op `sleep`)
- Track the attempt count starting from 0
- If `budget` is 0, don't even call once — raise `BudgetExhausted` immediately

**Why these shapes:** this is exactly the pattern Warm-up 3 asks for. Learn it here, then reuse the pattern on the real problem.

## How to run

```bash
python marathon.py run 017
```

Edit `problem.py`. When `test_problem.py` passes, move on.
