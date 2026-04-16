# Hints for Content-Addressed Cache

## Hint 1

This is a memoization problem where the cache key is a cryptographic hash of the inputs. Use `hashlib.sha256` from the standard library. The tricky part is making the hash deterministic regardless of dict insertion order — use `json.dumps(inputs, sort_keys=True)` to canonicalize the inputs before hashing.

## Hint 2

Approach for `compute(name, inputs, fn)`:
- Build a canonical string from `name` and `inputs`: concatenate `name` with `json.dumps(inputs, sort_keys=True)`
- Hash that string with `hashlib.sha256(raw.encode()).hexdigest()` to get `hash_key`
- If `hash_key` is in `self._cache`: increment `_hit_count` and return the cached value
- Otherwise: call `fn(inputs)`, store in `self._cache[hash_key]`, increment `_miss_count`, return the result

## Hint 3

The hash-key construction that handles dict ordering correctly:

```python
import json, hashlib

raw = name + json.dumps(inputs, sort_keys=True)
hash_key = hashlib.sha256(raw.encode()).hexdigest()
```
