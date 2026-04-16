# Hints for Temporary Attribute Override

## Hint 1

This is a context manager problem. The tricky part is handling two distinct cases on exit: restoring an attribute that existed before, versus deleting an attribute that was newly created. You need a sentinel value — a unique object that can't be confused with any real attribute value — to distinguish "attribute existed" from "attribute was absent".

## Hint 2

Approach outline:
- The stub already imports `_SENTINEL = object()` — use that as your "was absent" marker
- In the setup phase (before `yield`): check if `obj` has the attribute with `hasattr(obj, name)` or `getattr(obj, name, _SENTINEL)`; save the original value (or `_SENTINEL` if absent), then set the new value with `setattr(obj, name, value)`
- After `yield`, in the teardown phase (which runs even if an exception occurs): if the original was `_SENTINEL`, call `delattr(obj, name)`; otherwise, call `setattr(obj, name, original)`
- Use `@contextmanager` from `contextlib` and structure your function as a `try/finally` around the `yield`

## Hint 3

```python
@contextmanager
def temp_attr(obj, name, value):
    original = getattr(obj, name, _SENTINEL)
    setattr(obj, name, value)
    try:
        yield
    finally:
        if original is _SENTINEL:
            delattr(obj, name)
        else:
            setattr(obj, name, original)
```
