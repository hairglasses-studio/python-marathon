# Top-N Tracker

**Tier:** tier1_fluency  
**Target time:** 12 minutes  
**Topics:** heapq, min-heap  
**Source:** `openai-python-refresher.ipynb` cells 95-98

## Problem

## 8.5 Exercise — Top-N tracker

**Task:** Implement `TopN(n)` that tracks the N largest values seen so far. `add(x)` inserts a value; `top()` returns the current top-N as a sorted-desc list.

Use a min-heap of size N. When a new value arrives and the heap is full, compare to `heap[0]` (the min): if the new value is larger, pop + push to replace the min.

**Why a min-heap for top-N:** the min tells you the current "cutoff" — any new value larger than it deserves to enter. Memory usage is O(N) regardless of input size.

## How to run

```bash
python marathon.py run 007
```

Edit `problem.py`. When `test_problem.py` passes, move on.
