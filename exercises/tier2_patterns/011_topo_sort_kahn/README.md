# Topological Sort (Kahn's Algorithm)

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** graph, BFS, in-degree  
**Source:** `openai-primitives-refresher.ipynb` cells 10-13

## Problem

## 1.3 Exercise — Topological sort (Kahn's algorithm)

**Task:** Implement `topo_sort(graph)` that returns a topological ordering of all nodes: if `a` depends on `b`, then `b` must appear before `a` in the output. If the graph contains a cycle, raise `ValueError("cycle detected")`.

**Use Kahn's algorithm:**
1. Compute the *in-degree* of every node (count of incoming edges).
2. Start a queue with all nodes that have in-degree 0.
3. Pop from the queue, append to the result, and decrement the in-degree of every neighbor. If a neighbor's in-degree hits 0, push it.
4. If the result has fewer nodes than the graph, there's a cycle.

**Why Kahn over DFS-based topo sort:** Kahn's algorithm gives you cycle detection for free and is more intuitive for build systems ("nodes with no more unbuilt dependencies become available").

> **Convention for this exercise:** the graph stores *dependencies* — `graph[node]` is the list of nodes that `node` depends on. So if `node` has in-degree 0 in the *dependency* DAG, it means nothing depends on it. We'll invert: treat `graph[node]` as "things `node` points to," and output nodes whose dependencies are all resolved first. In other words: a node is emitted once all its dependencies are emitted.

## How to run

```bash
python marathon.py run 011
```

Edit `problem.py`. When `test_problem.py` passes, move on.
