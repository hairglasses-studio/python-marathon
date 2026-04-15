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
    """Base."""


class RetryableError(ToolError):
    """Transient — retry allowed."""


class TerminalError(ToolError):
    """Permanent — give up."""


class BudgetExhausted(ToolError):
    """Total retry budget across all calls is spent."""


ToolBackend = Callable[[ToolCall], Awaitable[Any]]


@dataclass
class Budget:
    total_retries: int
    _used: int = 0

    async def consume(self) -> None:
        # Acquire any needed lock inside here. Raise BudgetExhausted if empty.
        raise NotImplementedError("fill me in")


async def invoke_all(
    calls: list[ToolCall],
    backend: ToolBackend,
    *,
    budget: Budget,
    max_attempts: int = 3,
    base_delay: float = 0.01,
) -> list[ToolResult]:
    """Invoke all tool calls concurrently with per-call retry and shared budget.

    - Each call gets up to `max_attempts` tries.
    - `RetryableError` consumes 1 from the shared `budget`. If budget hits 0,
      the NEXT retry attempt raises BudgetExhausted → that call's ToolResult
      is ok=False with error=str(BudgetExhausted).
    - `TerminalError` records ok=False, no retry.
    - Success records ok=True with the value.
    - Returns results in input order.
    """
    raise NotImplementedError("fill me in")
