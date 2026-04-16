# Notes for Call-Counter Decorator

## Why this matters

Decorators are Python's primary mechanism for cross-cutting concerns: logging, rate limiting, caching, authentication checks, and metrics. The call-counter pattern specifically appears in profiling tools, circuit breakers, and test doubles that assert a function was called a specific number of times.

## Watch out for

- Storing count in a closure variable (e.g., `count = [0]`) instead of as an attribute on `wrapper` — the closure approach works but makes the count inaccessible from outside, which is what the tests require via `fn.call_count`
- Forgetting `@wraps(fn)` — without it, `wrapper.__name__` returns `"wrapper"` instead of the original function's name, which breaks introspection and some testing frameworks

## Interview follow-ups

- "How would you reset the counter between test runs without redecorating the function?"
- "How would you write a decorator that limits a function to at most N calls before raising an exception?"
- "What's the difference between a decorator implemented as a function vs. as a class with `__call__`?"
