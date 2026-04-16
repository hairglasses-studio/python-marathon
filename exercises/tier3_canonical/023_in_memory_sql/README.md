# In-Memory SQL Database

**Tier:** tier3_canonical  
**Target time:** 45 minutes  
**Topics:** data-modeling, filtering, sorting, Callable

## Problem

Build a `Database` class that supports creating tables, inserting rows, and querying with `where`, `order_by`, and column projection.

### API

- **`create_table(name: str, columns: list[str]) -> None`** — register a table with a fixed column schema.
- **`insert(table: str, row: dict[str, Any]) -> None`** — insert a row. Raise `SchemaError` if the row contains keys not in the schema. Missing columns default to `None`. Raise `TableNotFound` if the table doesn't exist.
- **`select(table, *, where=None, order_by=None, columns=None) -> list[dict]`** — query rows.
  - `where: Callable[[Row], bool] | None` — filter predicate applied to each row.
  - `order_by: list[str] | None` — sort keys. Prefix with `-` for descending (e.g. `["-age"]`). Multi-column sort is supported (e.g. `["role", "-age"]`).
  - `columns: list[str] | None` — project to a subset of columns. `None` returns all columns.

Exception classes `TableNotFound(KeyError)` and `SchemaError(ValueError)` are provided in the stub.

### Gates

**Gate 1** — create, insert, select-all, column projection, missing-table error, schema enforcement, partial rows (missing columns read as `None`)  
**Gate 2** — `where` predicates: equality, comparison, compound `and`/`or`  
**Gate 3** — `order_by`: ascending, descending (with `-` prefix), multi-column, combined `where` + `order_by` + `columns`

## How to run

```bash
python marathon.py run 023
```

Edit `problem.py`. When `test_problem.py` passes, move on.
