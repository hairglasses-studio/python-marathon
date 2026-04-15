import random
from typing import Any, Callable


class ToolError(Exception): pass
class RetryableError(ToolError): pass
class TerminalError(ToolError): pass
class BudgetExhausted(TerminalError): pass


def default_backoff(attempt: int, base: float = 0.1, cap: float = 30.0) -> float:
    ceiling = min(cap, base * (2 ** attempt))
    return random.uniform(0, ceiling)


def retry(
    fn: Callable[[], Any],
    *,
    budget: int,
    backoff: Callable[[int], float] = default_backoff,
    sleep: Callable[[float], None] = None,
) -> Any:
    if sleep is None:
        import time
        sleep = time.sleep
    if budget <= 0:
        raise BudgetExhausted("zero budget")

    attempt = 0
    while attempt < budget:
        try:
            return fn()
        except TerminalError:
            # Don't retry, just propagate
            raise
        except RetryableError:
            attempt += 1
            if attempt >= budget:
                raise BudgetExhausted(f"exhausted after {attempt} attempts")
            sleep(backoff(attempt - 1))

    raise BudgetExhausted(f"exhausted after {attempt} attempts")
