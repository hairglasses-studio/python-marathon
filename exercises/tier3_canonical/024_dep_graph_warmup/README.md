# Dependency Graph with Incremental Invalidation (Warm-up 1)

**Tier:** tier3_canonical  
**Target time:** 45 minutes  
**Topics:** graph, hashing, threading, invalidation, 4-gate  
**Source:** `openai-devprod-2026-04-16.ipynb` cells 14-17

## Problem

## Warm-up 1 — Dependency Graph with Incremental Invalidation

**Why:** classic internal build-system problem. Direct fit for Engineering Acceleration.

Build a DAG of targets. `build(target)` walks the DAG, runs each node's build function, and caches the result keyed by `(node_id, input_hash)`. `invalidate(target)` clears the cache entry for a node and all transitive dependents.

### The four gates

1. **Gate 1 — basic DAG + topological build.** `add_target(name, inputs, build_fn)`; `build(name)` runs dependencies first, then the node.
2. **Gate 2 — content-hash caching.** Skip rebuilds when the hash of inputs is unchanged. Use `hashlib.sha256` over `repr(inputs)`.
3. **Gate 3 — concurrent build of independent subtrees.** Use `concurrent.futures.ThreadPoolExecutor` with per-node locking.
4. **Gate 4 — cycle detection.** Three-color DFS (WHITE / GRAY / BLACK); raise a clear `CycleError`.

**Target:** clear 2 gates fully; aim for 3. If you stall, skip ahead to the reference solution to compare.

## How to run

```bash
python marathon.py run 024
```

Edit `problem.py`. When `test_problem.py` passes, move on.
