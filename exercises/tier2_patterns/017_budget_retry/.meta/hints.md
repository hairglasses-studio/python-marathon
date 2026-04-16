# Hints for Budget-Aware Retry with Exponential Backoff

## Hint 1

This is an exception-handling and control-flow problem. The retry loop tracks an attempt counter, calls `fn()`, and handles three outcomes: success (return the value), `RetryableError` (sleep and retry), and `TerminalError` (re-raise immediately). The budget check happens before each attempt, and `BudgetExhausted` (a subclass of `TerminalError`) is raised when the budget is spent.

## Hint 2

Structure of the `retry` function:
- If `budget == 0`: raise `BudgetExhausted` immediately (don't even call `fn`)
- Loop `attempt` from 0 to `budget - 1`:
  - Try calling `fn()`; on success, return the value
  - Catch `TerminalError`: re-raise as-is (includes `BudgetExhausted` — don't catch it separately)
  - Catch `RetryableError`: if this was the last attempt (`attempt == budget - 1`), raise `BudgetExhausted`; otherwise call `sleep(backoff(attempt))`
- Default `sleep` to `time.sleep` if `None` is passed

## Hint 3

The core retry loop skeleton:

```python
for attempt in range(budget):
    try:
        return fn()
    except TerminalError:
        raise
    except RetryableError:
        if attempt == budget - 1:
            raise BudgetExhausted("budget exhausted")
        sleep(backoff(attempt))
```
