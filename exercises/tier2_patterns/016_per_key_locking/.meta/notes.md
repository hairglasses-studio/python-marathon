# Notes for Per-Key Locking (KeyedLocker)

## Why this matters

Per-key locking appears in database row-level locking, cache sharding, and any system that needs fine-grained concurrency without a single global bottleneck. It's the correct answer to "make the versioned KV store thread-safe without serializing unrelated writes."

## Watch out for

- **Lock inversion / serialization**: if you hold the global lock while acquiring the per-key lock, all operations are serialized — you've gained nothing. The global lock must be released before acquiring the per-key lock.
- **Lazy initialization is required**: don't pre-create locks for all keys. The point is that locks are created on first use and the dict itself is protected.

## Interview follow-ups

1. What happens if two threads try to acquire locks for keys A and B in opposite orders? Is there a deadlock risk here?
2. How would you add lock timeouts to prevent indefinite blocking?
3. How would you extend this to support read-write locking (multiple concurrent readers, exclusive writers) per key?
