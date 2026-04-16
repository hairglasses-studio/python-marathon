# Notes for Windowed Generator

## Why this matters

Sliding-window iteration is a core primitive in stream processing, time-series analysis, rolling statistics, and N-gram extraction for NLP. The generator form is important: it processes arbitrarily large streams without buffering the whole input in memory.

## Watch out for

- Yielding `list(buf)` instead of `tuple(buf)` — the tests expect tuples; also tuples are immutable and safer to yield from generators
- Using index-based slicing (`seq[i:i+size]`) works for lists but breaks for arbitrary iterables like `range` or file objects; the `deque` approach handles both

## Interview follow-ups

- "How would you implement this without `deque` — say, using only a list?"
- "Can you write a version that yields overlapping windows with a configurable step size?"
- "What does `itertools.islice` buy you here, and when would you reach for it?"
