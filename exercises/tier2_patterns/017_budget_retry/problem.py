import random
from typing import Any, Callable

# Exception classes from the previous section
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
    """Retry `fn` up to `budget` attempts with the given backoff."""
    raise NotImplementedError("fill me in")
