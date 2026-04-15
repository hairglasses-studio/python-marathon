# Hints

## Hint 1

`asyncio.gather(*coros)` runs all coroutines concurrently and returns results in input order. But it doesn't cap in-flight concurrency. What stdlib primitive lets you say "only N of these at a time"?

## Hint 2

`asyncio.Semaphore(concurrency)` — use it as an async context manager (`async with semaphore:`) inside a wrapper coroutine. The wrapper acquires the semaphore, awaits the fetcher, releases. Then gather the wrappers.

## Hint 3

```python
semaphore = asyncio.Semaphore(concurrency)
async def bounded(url):
    async with semaphore:
        return await fetcher(url)
return await asyncio.gather(*(bounded(u) for u in urls))
```
