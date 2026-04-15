# Hints

## Hint 1

Put items on the queue tagged with their index: `await queue.put((idx, item))`. Use that index to write to a pre-allocated results list. This way order is preserved regardless of worker scheduling.

## Hint 2

Sentinel pattern: after enqueuing all items, push `None` once per worker. Each worker treats `None` as "drain and exit." Otherwise workers would block forever on `queue.get()`.

## Hint 3

Worker skeleton:

```python
async def worker():
    while True:
        task = await queue.get()
        if task is None:
            queue.task_done()
            return
        idx, item = task
        results[idx] = await process(item)
        queue.task_done()
```
