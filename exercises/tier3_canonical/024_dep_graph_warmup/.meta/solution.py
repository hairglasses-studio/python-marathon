from __future__ import annotations

import hashlib
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any, Callable


class CycleError(RuntimeError):
    """Raised when the DAG has a cycle."""


@dataclass
class Target:
    name: str
    inputs: list[str]
    build_fn: Callable[[dict[str, Any]], Any]


class DepGraph:
    def __init__(self) -> None:
        self._targets: dict[str, Target] = {}
        self._cache: dict[str, Any] = {}
        self._last_input_hash: dict[str, str] = {}
        self._locks: dict[str, threading.Lock] = {}
        self._global_lock = threading.Lock()

    def add_target(
        self,
        name: str,
        inputs: list[str],
        build_fn: Callable[[dict[str, Any]], Any],
    ) -> None:
        self._targets[name] = Target(name=name, inputs=inputs, build_fn=build_fn)

    def _lock_for(self, name: str) -> threading.Lock:
        with self._global_lock:
            if name not in self._locks:
                self._locks[name] = threading.Lock()
            return self._locks[name]

    def _hash_inputs(self, dep_values: dict[str, Any]) -> str:
        raw = repr(sorted(dep_values.items())).encode()
        return hashlib.sha256(raw).hexdigest()

    def build(self, name: str) -> Any:
        if name not in self._targets:
            raise KeyError(name)
        target = self._targets[name]

        # Gate 3: build independent subtrees in parallel.
        dep_values: dict[str, Any] = {}
        if target.inputs:
            with ThreadPoolExecutor(max_workers=len(target.inputs)) as pool:
                futures = {dep: pool.submit(self.build, dep) for dep in target.inputs}
                for dep, fut in futures.items():
                    dep_values[dep] = fut.result()

        # Gate 2: cache hit if input hash unchanged.
        with self._lock_for(name):
            current_hash = self._hash_inputs(dep_values)
            if (
                name in self._cache
                and self._last_input_hash.get(name) == current_hash
            ):
                return self._cache[name]

            result = target.build_fn(dep_values)
            self._cache[name] = result
            self._last_input_hash[name] = current_hash
            return result

    def invalidate(self, name: str) -> None:
        dependents = self._transitive_dependents(name)
        dependents.add(name)
        for dep in dependents:
            self._cache.pop(dep, None)
            self._last_input_hash.pop(dep, None)

    def _transitive_dependents(self, name: str) -> set[str]:
        result: set[str] = set()
        for candidate, target in self._targets.items():
            if name in target.inputs:
                result.add(candidate)
                result.update(self._transitive_dependents(candidate))
        return result

    def check_cycles(self) -> None:
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {name: WHITE for name in self._targets}

        def visit(node: str) -> None:
            color[node] = GRAY
            for dep in self._targets[node].inputs:
                if color.get(dep) == GRAY:
                    raise CycleError(f"cycle via {node} -> {dep}")
                if color.get(dep) == WHITE:
                    visit(dep)
            color[node] = BLACK

        for name in self._targets:
            if color[name] == WHITE:
                visit(name)
