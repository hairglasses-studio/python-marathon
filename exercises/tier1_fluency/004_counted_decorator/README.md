# Call-Counter Decorator

**Tier:** tier1_fluency  
**Target time:** 10 minutes  
**Topics:** decorator, closure, functools.wraps  
**Source:** `openai-python-refresher.ipynb` cells 51-54

## Problem

## 4.4 Exercise — Call counter decorator

**Task:** Implement a decorator `@counted` that records how many times the wrapped function has been called. After decoration, the function should have a `.call_count` attribute.

Example:
```python
@counted
def greet(name): return f"hi {name}"

greet("a"); greet("b"); greet("c")
print(greet.call_count)   # 3
```

**Hint:** the wrapper function can carry state via an attribute on itself (`wrapper.call_count`).

## How to run

```bash
python marathon.py run 004
```

Edit `problem.py`. When `test_problem.py` passes, move on.
