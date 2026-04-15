# Async Queue — Worker Pool Pipeline

**Tier:** tier4_async
**Target time:** 25 minutes
**Topics:** asyncio.Queue, create_task, sentinel, worker pool, order preservation

## Problem

Implement `pipeline(items, process, num_workers=4)` that processes items through an async worker pool backed by `asyncio.Queue`.

**Requirements:**
- Spawn `num_workers` worker tasks.
- Each worker pulls from the queue, processes items, stores results.
- Workers must exit cleanly when the queue drains.
- Return results in **input order** (not completion order).

**Signature:**

```python
async def pipeline(
    items: list[T],
    process: Callable[[T], Awaitable[R]],
    *,
    num_workers: int = 4,
) -> list[R]:
```

**Why this matters:** Producer-consumer is the async pattern behind most tool-call frameworks, web crawlers, and batch processing systems. `asyncio.Queue` + sentinel pattern is the canonical idiom.

## How to run

```bash
python marathon.py run 029
```
