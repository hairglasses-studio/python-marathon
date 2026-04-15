# Hints

## Hint 1

Structure it as a `for attempt in range(max_attempts):` loop with `try/except`. On success, `return`. On `RetryableError`, compute the delay and `await asyncio.sleep(delay)`. On `TerminalError`, `raise`.

## Hint 2

Delay formula: `min(base_delay * (2 ** attempt), max_delay) + random.uniform(0, jitter)`. Don't sleep on the LAST attempt — no point waiting if you're about to give up anyway.

## Hint 3

```python
for attempt in range(max_attempts):
    try:
        return await fn()
    except TerminalError:
        raise
    except RetryableError as e:
        last_err = e
        if attempt == max_attempts - 1:
            break
        await asyncio.sleep(min(base_delay * 2**attempt, max_delay) + random.uniform(0, jitter))
raise last_err
```
