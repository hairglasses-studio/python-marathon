# Temporary Attribute Override

**Tier:** tier1_fluency  
**Target time:** 10 minutes  
**Topics:** context-manager, contextlib, sentinel  
**Source:** `openai-python-refresher.ipynb` cells 104-107

## Problem

## 9.3 Exercise — Temporary attribute override

**Task:** Write a context manager `temp_attr(obj, name, value)` that temporarily sets `obj.name = value` for the duration of the `with` block, then restores the original value on exit. Should work even if the attribute didn't originally exist.

**Pattern used for:** mocking in tests, temporarily patching config, overriding defaults for a scoped block.

## How to run

```bash
python marathon.py run 008
```

Edit `problem.py`. When `test_problem.py` passes, move on.
