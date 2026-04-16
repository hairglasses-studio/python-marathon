# Notes for Content-Addressed Cache

## Why this matters

Content-addressed storage is the core primitive behind Bazel, Buck, sccache, ccache, and Git's object store. Any system that needs to avoid recomputing identical work uses this pattern. In ML contexts it shows up in dataset caching and model artifact deduplication.

## Watch out for

- **Dict ordering**: `{"x": 1, "y": 2}` and `{"y": 2, "x": 1}` are semantically identical but produce different `str()` representations. Always use `json.dumps(sort_keys=True)` or `sorted(inputs.items())` to canonicalize.
- **Name must be part of the key**: two different operations with the same input dict should not collide. The test explicitly checks `"double"` vs `"other"` with identical inputs.

## Interview follow-ups

1. What are the collision risks of SHA-256 in practice, and when would you use a weaker hash for performance?
2. How would you add TTL (time-to-live) expiry to this cache?
3. How would you make this cache persistent across process restarts?
