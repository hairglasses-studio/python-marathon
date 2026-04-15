# IntRange Class

**Tier:** tier1_fluency  
**Target time:** 12 minutes  
**Topics:** OOP, dunders, iteration-protocol  
**Source:** `openai-python-refresher.ipynb` cells 66-69

## Problem

## 5.6 Exercise — `Range` as a class

**Task:** Implement `IntRange(start, stop)` representing a half-open interval `[start, stop)`. It should support:
- `__len__` — the number of integers in the range
- `__iter__` — iteration yields each integer in order
- `__contains__` — `x in r` for O(1) membership
- `__repr__` — `IntRange(start, stop)`
- `__eq__` — equal if start and stop match
- `__hash__` — hashable

**Follow-up:** make it work with negative step? (Optional — stretch goal.)

## How to run

```bash
python marathon.py run 005
```

Edit `problem.py`. When `test_problem.py` passes, move on.
