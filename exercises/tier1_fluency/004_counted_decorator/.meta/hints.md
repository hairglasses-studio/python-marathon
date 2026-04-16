# Hints for Call-Counter Decorator

## Hint 1

This is a decorator pattern problem. A decorator is a function that takes a function and returns a new function (the wrapper). The wrapper needs to carry mutable state — the count — that persists across calls. In Python, functions are objects, so you can attach arbitrary attributes to the wrapper function itself.

## Hint 2

Approach outline:
- Define `counted(fn)` that defines and returns an inner `wrapper(*args, **kwargs)`
- Initialize `wrapper.call_count = 0` immediately after defining `wrapper`, before returning it
- Inside `wrapper`, increment `wrapper.call_count` by 1, then call `fn(*args, **kwargs)` and return its result
- Use `@functools.wraps(fn)` on the wrapper to preserve `__name__`, `__doc__`, and other metadata from the original function

## Hint 3

```python
from functools import wraps

def counted(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return fn(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper
```
