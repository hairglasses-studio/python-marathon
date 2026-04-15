"""Warm-up 1 SCAFFOLD — fill in the gates, then run the tests cell below."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


class CycleError(RuntimeError):
    """Raised when a cycle is detected."""


@dataclass
class Target:
    name: str
    inputs: list[str]
    build_fn: Callable[[dict[str, Any]], Any]


class DepGraph:
    def __init__(self) -> None:
        self._targets: dict[str, Target] = {}
        self._cache: dict[str, Any] = {}
        # Gate 2: add a hash cache (name -> last_input_hash)
        # Gate 3: add a lock manager (name -> threading.Lock)

    def add_target(
        self,
        name: str,
        inputs: list[str],
        build_fn: Callable[[dict[str, Any]], Any],
    ) -> None:
        self._targets[name] = Target(name=name, inputs=inputs, build_fn=build_fn)

    def build(self, name: str) -> Any:
        """Gate 1: topological build; Gate 2: hash cache; Gate 3: parallel."""
        raise NotImplementedError("Gate 1-3: implement build")

    def invalidate(self, name: str) -> None:
        """Gate 2: invalidate this node + all transitive dependents."""
        raise NotImplementedError("Gate 2: implement invalidate")

    def check_cycles(self) -> None:
        """Gate 4: three-color DFS; raise CycleError on detection."""
        raise NotImplementedError("Gate 4: implement cycle detection")
