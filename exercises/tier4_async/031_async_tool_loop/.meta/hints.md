# Hints

## Hint 1

Split the problem into two functions: `_invoke_one(call, ...)` handles one call's retry loop, and `invoke_all(calls, ...)` gathers them with `asyncio.gather`. Composing these is the whole exercise.

## Hint 2

`Budget.consume()` needs to be concurrency-safe because multiple calls will hit it simultaneously. Use an `asyncio.Lock` inside the `_lock` field. Note: `asyncio.Lock` is not threadsafe — it's specifically for coroutines in the same event loop. That's what you want.

## Hint 3

`_invoke_one` skeleton:

```python
for attempt in range(1, max_attempts + 1):
    try:
        value = await backend(call)
        return ToolResult(ok=True, value=value, attempts=attempt)
    except TerminalError as e:
        return ToolResult(ok=False, error=..., attempts=attempt)
    except RetryableError as e:
        if attempt == max_attempts:
            return ToolResult(ok=False, ...)
        try:
            await budget.consume()
        except BudgetExhausted as be:
            return ToolResult(ok=False, error=str(be), attempts=attempt)
        await asyncio.sleep(base_delay * 2**(attempt - 1))
```
