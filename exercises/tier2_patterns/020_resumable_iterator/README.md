# Resumable List Iterator

**Tier:** tier2_patterns  
**Target time:** 20 minutes  
**Topics:** iteration-protocol, state-serialization

## Problem

Implement a `ListIterator` class that wraps a list and supports snapshotting/restoring its position mid-iteration.

### API

- **`next() -> T`** — return the current item and advance. Raise `StopIteration` when exhausted.
- **`get_state() -> dict`** — return a JSON-serializable dict capturing the iterator's current position. The dict must survive `json.dumps` + `json.loads` round-tripping.
- **`set_state(state: dict) -> None`** — restore the iterator to a previously captured position. After restoring, `next()` resumes from wherever the snapshot was taken.

### Example

```python
it = ListIterator(["a", "b", "c", "d", "e"])
it.next()          # "a"
it.next()          # "b"
saved = it.get_state()
it.next()          # "c"
it.next()          # "d"
it.set_state(saved)
it.next()          # "c" (replays from snapshot)
```

### Why this matters

Resumable iteration is the core primitive behind checkpoint/restart in data pipelines, paginated API crawlers, and any system that needs to pick up where it left off after a crash or context switch.

## How to run

```bash
python marathon.py run 020
```

Edit `problem.py`. When `test_problem.py` passes, move on.
