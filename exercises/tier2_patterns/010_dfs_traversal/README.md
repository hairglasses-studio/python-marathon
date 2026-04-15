# Depth-First Search (Pre-order)

**Tier:** tier2_patterns  
**Target time:** 15 minutes  
**Topics:** graph, DFS, recursion  
**Source:** `openai-primitives-refresher.ipynb` cells 6-9

## Problem

## 1.2 Exercise — Depth-first search

**Task:** Implement `dfs(graph, start)` that returns the list of nodes visited in DFS **pre-order** (node recorded when first entered, before recursing into children). Each node should appear exactly once.

**Why this matters:** DFS is the foundation for topological sort and cycle detection. If you can write DFS without thinking, the harder graph exercises become muscle memory.

**Constraints:**
- Visit each node at most once.
- Visit neighbors in the order they appear in the adjacency list.
- Handle disconnected subtrees reachable from the start correctly.

## How to run

```bash
python marathon.py run 010
```

Edit `problem.py`. When `test_problem.py` passes, move on.
