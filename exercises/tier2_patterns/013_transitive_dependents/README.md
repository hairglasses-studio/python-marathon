# Transitive Dependents (Cache Invalidation)

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** graph, reverse-BFS, defaultdict  
**Source:** `openai-primitives-refresher.ipynb` cells 18-21

## Problem

## 1.5 Exercise — Transitive dependents (for cache invalidation)

**Task:** Implement `transitive_dependents(graph, target)` returning the set of all nodes that **transitively depend on** `target`. These are the nodes whose cached output must be invalidated when `target` changes.

**Setup:** `graph[x]` is `x`'s direct dependencies. So if `graph["api"] == ["db"]`, then `api` *depends on* `db` → `api` is a *dependent* of `db`. If `db` changes, `api` needs to rebuild, and anything depending on `api` also needs to rebuild.

**This is exactly Warm-up 1 gate 2** (`invalidate(target)` propagating through the graph).

**Algorithm:**
1. Invert the graph: `dependents[x] = [everyone who lists x as a dep]`
2. BFS/DFS from `target` in the inverted graph.
3. Return the full set reached.

## How to run

```bash
python marathon.py run 013
```

Edit `problem.py`. When `test_problem.py` passes, move on.
