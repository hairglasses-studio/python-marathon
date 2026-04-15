# Parallel Sum with ThreadPoolExecutor

**Tier:** tier1_fluency  
**Target time:** 12 minutes  
**Topics:** threading, ThreadPoolExecutor, chunking  
**Source:** `openai-python-refresher.ipynb` cells 117-120

## Problem

## 10.5 Exercise — Concurrent accumulator

**Task:** Implement `parallel_sum(numbers, chunk_size)` that splits `numbers` into chunks of size `chunk_size`, sums each chunk in a thread pool, and returns the grand total.

**Use:** `concurrent.futures.ThreadPoolExecutor` and `pool.map`. No need for locks — each chunk is independent.

**Why this pattern:** it's the building block for map-reduce-style parallelism in Python. For I/O-bound work (sum-over-fetched-data) it actually speeds things up.

## How to run

```bash
python marathon.py run 009
```

Edit `problem.py`. When `test_problem.py` passes, move on.
