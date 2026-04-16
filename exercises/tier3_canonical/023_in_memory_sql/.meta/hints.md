# Hints for In-Memory SQL Database

## Hint 1

Gate 1 is pure data modeling: store schemas and rows in dicts, validate keys against the schema on `insert`, and pad missing columns with `None`. Gate 2 applies a filter function — since `where` is already a `Callable[[Row], bool]`, you just need `filter(where, rows)`. Gate 3 is the sorting challenge: `order_by` is a list of column names where a `-` prefix means descending. Python's `sorted()` with a tuple key handles multi-column sort, but you need to negate numeric values (or use `reverse` per-key) to mix ascending and descending columns.

## Hint 2

- `create_table`: store `self._schemas[name] = columns`; `self._rows[name] = []`.
- `insert`: check `table in self._schemas` (raise `TableNotFound`); validate `set(row) - set(schema) == empty` (raise `SchemaError`); pad missing columns with `None` before appending.
- `select` Gate 2: `result = [r for r in rows if where(r)]` (or `list(filter(where, rows))`).
- `select` Gate 3: parse each `order_by` key — strip leading `-` to get the column name and record direction; build a sort key tuple; use `sorted(..., key=...)`.
- For mixed-direction sort: use `(row[col], ...)` for ascending and `(-row[col], ...)` for descending numeric values; for strings, negate with a wrapper or sort in two passes (Python doesn't support per-key `reverse`).

## Hint 3

Multi-column sort key with direction:

```python
def sort_key(row):
    parts = []
    for col in order_by:
        desc = col.startswith("-")
        key = col.lstrip("-")
        val = row[key]
        # Negate numerics for descending; use a sentinel for None
        if desc and isinstance(val, (int, float)):
            parts.append(-val)
        else:
            parts.append((0 if desc else 1, val))
    return tuple(parts)

result = sorted(result, key=sort_key)
```
