from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable


@dataclass(frozen=True)
class ToolCall:
    name: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    ok: bool
    value: Any = None
    error: str | None = None
    attempts: int = 1


class ToolError(Exception):
    pass


class RetryableError(ToolError):
    pass


class TerminalError(ToolError):
    pass


class BudgetExhausted(ToolError):
    pass


ToolBackend = Callable[[ToolCall], Awaitable[Any]]


@dataclass
class Budget:
    total_retries: int
    _used: int = 0
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)

    async def consume(self) -> None:
        async with self._lock:
            if self._used >= self.total_retries:
                raise BudgetExhausted(f"budget of {self.total_retries} retries spent")
            self._used += 1


async def _invoke_one(
    call: ToolCall,
    backend: ToolBackend,
    budget: Budget,
    max_attempts: int,
    base_delay: float,
) -> ToolResult:
    last_err: Exception | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            value = await backend(call)
            return ToolResult(ok=True, value=value, attempts=attempt)
        except TerminalError as e:
            return ToolResult(ok=False, error=f"terminal: {e}", attempts=attempt)
        except RetryableError as e:
            last_err = e
            if attempt == max_attempts:
                break
            try:
                await budget.consume()
            except BudgetExhausted as be:
                return ToolResult(ok=False, error=str(be), attempts=attempt)
            await asyncio.sleep(base_delay * (2 ** (attempt - 1)))
    return ToolResult(ok=False, error=f"exhausted: {last_err}", attempts=max_attempts)


async def invoke_all(
    calls: list[ToolCall],
    backend: ToolBackend,
    *,
    budget: Budget,
    max_attempts: int = 3,
    base_delay: float = 0.01,
) -> list[ToolResult]:
    tasks = [
        _invoke_one(c, backend, budget, max_attempts, base_delay) for c in calls
    ]
    return await asyncio.gather(*tasks)
