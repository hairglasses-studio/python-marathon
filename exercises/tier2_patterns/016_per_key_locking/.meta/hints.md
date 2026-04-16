# Hints for Per-Key Locking (KeyedLocker)

## Hint 1

This is a concurrency pattern problem using `threading.Lock` and the `contextlib.contextmanager` decorator. The key insight is that you need two levels of locking: a global lock to protect the lock-dictionary itself (since dict writes aren't atomic), and per-key locks for the actual critical sections. The global lock must be released before acquiring the per-key lock — otherwise you've serialized everything.

## Hint 2

In `lock(self, key)` (a `@contextmanager` method):
- Acquire `self._global` to look up or create the per-key lock:
  - `if key not in self._locks: self._locks[key] = threading.Lock()`
  - Capture `key_lock = self._locks[key]`
  - Release `self._global`
- Now acquire `key_lock` and `yield` (the body of the `with` block runs here)
- Release `key_lock` in the finally block

## Hint 3

The two-phase lock acquisition as a context manager:

```python
@contextmanager
def lock(self, key: str):
    with self._global:
        if key not in self._locks:
            self._locks[key] = threading.Lock()
        key_lock = self._locks[key]
    # global lock released here — key_lock acquired next
    with key_lock:
        yield
```
