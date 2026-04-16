# Hints for Dependency Graph with Incremental Invalidation (Warm-up 1)

## Hint 1

Gate 1 needs topological build: a node can only run after all its `inputs` have been built. The classic approach is recursive DFS — build each input before building the node itself. Gate 2 adds content-hash caching: skip the build function if the hash of the already-built input values hasn't changed since last time. Gate 3 parallelizes independent subtrees using `ThreadPoolExecutor`; independent nodes are those whose inputs are all already computed. Gate 4 is three-color DFS cycle detection (WHITE/GRAY/BLACK) — if you reach a GRAY node during DFS, you've found a cycle.

## Hint 2

- Gate 1: `build(name)` recursively calls `build(inp)` for each input, collects results into a dict, then calls `target.build_fn(input_dict)` and stores the result in `self._cache`.
- Gate 2: after building all inputs, compute `hashlib.sha256(repr(input_dict).encode()).hexdigest()`; if it matches the stored hash for this node, return the cached output without re-running `build_fn`. On `invalidate(name)`, delete the cache entry for `name` and all nodes that (directly or transitively) depend on it.
- Gate 3: use `concurrent.futures.ThreadPoolExecutor`; protect `self._cache` with a per-node `threading.Lock` to avoid double-builds.
- Gate 4: maintain a `color: dict[str, str]` (WHITE/GRAY/BLACK); DFS sets GRAY on entry, BLACK on exit; finding GRAY raises `CycleError`.

## Hint 3

Three-color DFS for cycle detection (Gate 4):

```python
def check_cycles(self) -> None:
    color = {name: "WHITE" for name in self._targets}
    def dfs(name: str) -> None:
        if color[name] == "GRAY":
            raise CycleError(f"cycle at {name!r}")
        if color[name] == "BLACK":
            return
        color[name] = "GRAY"
        for inp in self._targets[name].inputs:
            if inp in color:
                dfs(inp)
        color[name] = "BLACK"
    for name in list(self._targets):
        if color[name] == "WHITE":
            dfs(name)
```
