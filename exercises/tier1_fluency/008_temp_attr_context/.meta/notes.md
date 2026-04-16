# Notes for Temporary Attribute Override

## Why this matters

This pattern is the basis of `unittest.mock.patch` and every test-scoped override mechanism in Python. It also appears in configuration management code that needs to temporarily elevate a limit or switch a flag without permanent mutation. Understanding how `finally` guarantees cleanup even through exceptions is essential for writing robust context managers.

## Watch out for

- Using `None` as the sentinel instead of a dedicated `object()` — if `None` is a valid attribute value, you can't distinguish "attribute was None" from "attribute was absent"; always use a private `object()` sentinel
- Forgetting the `try/finally` around the `yield` — without it, an exception in the `with` block will skip teardown and leave the object in the patched state

## Interview follow-ups

- "How does this compare to `unittest.mock.patch`? What does `patch` do that this doesn't?"
- "How would you extend this to temporarily override multiple attributes at once?"
- "What happens if `delattr` raises `AttributeError` in the teardown — e.g., because something else deleted the attribute inside the `with` block? How would you guard against that?"
