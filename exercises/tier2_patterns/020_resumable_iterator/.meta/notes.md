# Notes for Resumable List Iterator

## Why this matters

Resumable iteration is the core primitive behind checkpoint/restart in data pipelines, paginated API crawlers that survive process crashes, and any system that needs to resume from a known position after a failure or context switch. Kafka consumer offsets are essentially this pattern at scale.

## Watch out for

- **State must be JSON-serializable**: the test explicitly round-trips through `json.dumps` + `json.loads`. Don't store Python-specific types (sets, tuples, custom objects) in the state dict.
- **`set_state` does not reset to the beginning**: it restores to exactly the captured position. After `set_state(saved)`, the next `next()` call returns the item that was current when `get_state()` was called.

## Interview follow-ups

1. How would you extend this to support nested iterators or iterators over generators (not just lists)?
2. If the underlying list can be modified between `get_state()` and `set_state()`, what guarantees can you make about correctness?
3. How would you implement this for a database cursor, where the "state" must survive a network disconnection?
