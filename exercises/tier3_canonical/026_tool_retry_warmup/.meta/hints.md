# Hints for Tool-Call Loop with Retry + Budget (Warm-up 3)

## Hint 1

Gate 1 is a direct happy-path call: invoke the backend, wrap the result in `ToolResult(ok=True, value=...)`. Gate 2 adds a retry loop over `RetryableError` with exponential backoff (`base_delay * 2 ** attempt`) plus additive jitter; `TerminalError` breaks out immediately with `ok=False`. Gate 3 handles per-error-type policies: `RateLimitError` uses `error.retry_after` as the sleep duration instead of the computed backoff; `TimeoutError_` is retryable (same as generic). Gate 4 is budget accounting: call `budget.consume()` before each retry attempt; if `BudgetExhausted` is raised, return `ToolResult(ok=False, ...)`.

## Hint 2

- Loop structure: `for attempt in range(1, budget.remaining + 1)` is **wrong** — the budget is shared across nested calls. Instead, use a `while True` loop and call `budget.consume()` at the start of each retry.
- `TerminalError` (including `BudgetExhausted`) should be caught outside the retry loop, not inside — catch it, build `ToolResult(ok=False, error=str(e), attempts=attempt)`, return.
- For `RateLimitError`: it's a subclass of `RetryableError`, so check it *before* the generic `RetryableError` branch and use `sleep(err.retry_after)` instead of the backoff.
- `attempts` in the result counts total tries (1 on first success, N+1 if N retries then success/failure).

## Hint 3

Core retry loop skeleton (Gate 2 + 3):

```python
attempt = 0
while True:
    attempt += 1
    try:
        budget.consume()          # raises BudgetExhausted if empty
        value = backend(call)
        return ToolResult(ok=True, value=value, attempts=attempt)
    except RateLimitError as e:
        sleep(e.retry_after)
    except RetryableError:
        delay = min(base_delay * 2 ** (attempt - 1), max_delay)
        sleep(delay + random.uniform(0, jitter))
    except TerminalError as e:
        return ToolResult(ok=False, error=str(e), attempts=attempt)
    except BudgetExhausted as e:
        return ToolResult(ok=False, error=str(e), attempts=attempt)
```
