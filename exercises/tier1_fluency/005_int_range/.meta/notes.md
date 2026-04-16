# Notes for IntRange Class

## Why this matters

Implementing the iteration protocol and container dunders is how you make custom types feel native in Python. This pattern appears whenever you build domain objects — date ranges, IP address blocks, version intervals — that users expect to behave like sequences or sets.

## Watch out for

- If you define `__eq__` without `__hash__`, Python sets `__hash__ = None`, making the class unhashable — always define both together, and make sure `hash` is consistent with equality (same inputs to `__eq__` must produce the same hash)
- Returning `False` instead of `NotImplemented` from `__eq__` when the other type is unknown — `NotImplemented` lets Python try the reflected operation on the other object, which is the correct protocol

## Interview follow-ups

- "What would you need to change to support negative steps or a step parameter like Python's built-in `range`?"
- "Why is O(1) membership testing important here, and what would happen if you used `in list(self)` instead?"
- "How do `__eq__` and `__hash__` interact with sets and dict keys?"
