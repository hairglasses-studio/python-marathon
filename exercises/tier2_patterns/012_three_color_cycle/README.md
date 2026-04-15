# Three-Color Cycle Detection

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** graph, DFS, state-coloring  
**Source:** `openai-primitives-refresher.ipynb` cells 14-17

## Problem

## 1.4 Exercise — Three-color cycle detection

**Task:** Implement `has_cycle(graph)` using the three-color DFS algorithm. Return `True` if the graph has any cycle, `False` otherwise.

**The three colors:**
- **WHITE** — unvisited
- **GRAY** — currently on the DFS recursion stack (being explored)
- **BLACK** — fully explored, all descendants processed

**The rule:** during DFS, if you encounter a **GRAY** neighbor, you've found a back-edge — that's a cycle. If you encounter BLACK, it's a cross-edge in a DAG and is fine.

**Why three colors and not just `visited`:** a plain visited set tells you "seen before" but can't distinguish "seen before on this path" from "seen before on a previous path." The GRAY state is the on-the-stack marker that catches back-edges.

**This is exactly what Warm-up 1 gate 4 asks for** in the dependency graph problem.

## How to run

```bash
python marathon.py run 012
```

Edit `problem.py`. When `test_problem.py` passes, move on.
