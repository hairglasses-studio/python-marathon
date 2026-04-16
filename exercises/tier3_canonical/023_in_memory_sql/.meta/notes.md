# Notes for In-Memory SQL Database

## Why this matters

In-memory databases appear in mock/test infrastructure, feature flag engines, and embedded analytics. This exercise tests data modeling discipline (schema validation, null handling) and whether you can implement a sort that mixes ascending and descending keys — a real pain point that trips up even experienced engineers.

## Watch out for

- Mixed-direction multi-column sort: Python's `sorted(..., reverse=True)` reverses *all* keys; for mixed directions you must negate numeric values or use `functools.cmp_to_key`. The `-age` convention is common in Django ORM and ORMs broadly.
- Partial row insertion: missing columns should silently default to `None`, not raise an error. Only *extra* (unknown) keys should raise `SchemaError`.

## Interview follow-ups

- "How would you add an index to speed up `where` on a specific column?" — maintain a `dict[col_value, list[row_idx]]` per indexed column; filter by index lookup instead of full scan.
- "How would you support `JOIN` between two tables?" — nested-loop join: iterate rows of one table, filter against the other by a key condition; hash join is the scalable version.
- "How would you make inserts and selects thread-safe?" — a `threading.RLock` per table; acquire for writes and reads, or use a readers-writer lock for higher read concurrency.
