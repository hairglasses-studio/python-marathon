# Content-Addressed Cache

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** hashlib, caching, sha256  
**Source:** `openai-primitives-refresher.ipynb` cells 25-28

## Problem

## 2.2 Exercise — Content-addressed cache

**Task:** Build a `ContentCache` that stores the result of a computation keyed by a hash of the inputs. If `compute(name, inputs)` is called twice with identical inputs, the cached result is returned without recomputing.

**API:**
- `compute(name: str, inputs: dict, fn: Callable) -> Any`

**Behavior:**
- Compute `hash_key = sha256(name + sorted(inputs))` (or any deterministic scheme).
- If `hash_key` is in the cache, return the cached value.
- Otherwise, call `fn(inputs)`, store the result, return it.

**Why this matters:** this is the core primitive behind every build system's incremental compilation. Bazel, Buck, sccache, ccache — all the same pattern.

## How to run

```bash
python marathon.py run 014
```

Edit `problem.py`. When `test_problem.py` passes, move on.
