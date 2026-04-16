# Notes for Typed Config Parser

## Why this matters

Custom exception hierarchies are standard practice in library and service code — they let callers catch errors at the right granularity (all config errors vs. only syntax errors) without coupling to implementation details. This pattern appears in ORMs, config libraries, and API clients throughout the Python ecosystem.

## Watch out for

- Using `line.split("=")` without `maxsplit=1` will split values that contain `=` (e.g., `url=https://x.com/a=b`), producing more than two parts and breaking the parser
- Line numbers in the tests are 1-based and count only from the raw text lines — do not skip blank/comment lines before tracking the line number; track it from the beginning of iteration

## Interview follow-ups

- "How would you extend this to support typed values — integers, booleans, lists?"
- "What changes if you need to support multi-line values (value continues on next line with a leading space)?"
- "How would you write a context manager or decorator that wraps any parsing error into a `ConfigError`?"
