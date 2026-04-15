# Windowed Generator

**Tier:** tier1_fluency  
**Target time:** 10 minutes  
**Topics:** generator, deque, typing  
**Source:** `openai-python-refresher.ipynb` cells 40-43

## Problem

## 3.4 Exercise — Windowed generator

**Task:** Implement `windows(seq, size)` that yields successive `size`-length tuples from `seq`. If `seq` is too short, yield nothing.

Example: `windows([1,2,3,4,5], 3)` → `(1,2,3)`, `(2,3,4)`, `(3,4,5)`.

**Why this matters:** moving-window operations are a common primitive in stream processing, rolling averages, and N-gram extraction.

## How to run

```bash
python marathon.py run 003
```

Edit `problem.py`. When `test_problem.py` passes, move on.
