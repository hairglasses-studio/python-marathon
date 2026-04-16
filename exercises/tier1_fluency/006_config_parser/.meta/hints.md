# Hints for Typed Config Parser

## Hint 1

This is a string parsing problem combined with a custom exception hierarchy. The exception design is the structural challenge: you need a base class `ConfigError` with two specializations, each carrying extra attributes (`line_number` for syntax errors, `key` for duplicate key errors). The stubs are already defined in `problem.py` — your job is to fill in `parse_config`.

## Hint 2

Approach outline for `parse_config`:
- Split `text` into lines, then enumerate them to track the 1-based line number
- Skip lines that are empty (after stripping) or that start with `#`
- For each remaining line, split on `=` with `str.split("=", 1)` — the `maxsplit=1` argument prevents splitting on `=` inside values
- Validate: if no `=` was found (len < 2) or key is empty after stripping, raise `ConfigSyntaxError(msg, line_number)`
- Check for duplicates before inserting into the result dict; raise `ConfigDuplicateKeyError(msg, key)` if the key already exists

## Hint 3

```python
def parse_config(text):
    result = {}
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("=", 1)
        if len(parts) < 2:
            raise ConfigSyntaxError(f"missing '=' on line {lineno}", lineno)
        key, value = parts[0].strip(), parts[1].strip()
        if not key:
            raise ConfigSyntaxError(f"empty key on line {lineno}", lineno)
        if key in result:
            raise ConfigDuplicateKeyError(f"duplicate key '{key}'", key)
        result[key] = value
    return result
```
