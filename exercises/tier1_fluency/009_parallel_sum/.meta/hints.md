# Hints for Parallel Sum with ThreadPoolExecutor

## Hint 1

This is a map-reduce problem using Python's `concurrent.futures` module. The two steps are: split the input list into fixed-size chunks, then dispatch each chunk to a thread pool where each thread computes a partial sum. The grand total is the sum of all partial sums. Because each chunk is independent, no locking is needed.

## Hint 2

Approach outline:
- Import `ThreadPoolExecutor` from `concurrent.futures` (already imported in the stub)
- Write a chunking helper: use a list comprehension with `range(0, len(numbers), chunk_size)` to produce slices `numbers[i:i+chunk_size]`
- Define a `chunk_sum` function (or lambda) that takes a chunk and returns `sum(chunk)`
- Use `ThreadPoolExecutor(max_workers=max_workers)` as a context manager, then call `pool.map(chunk_sum, chunks)` to get partial sums
- Return `sum(partial_sums)`; handle the empty list edge case (empty input → `sum([])` returns 0 naturally)

## Hint 3

```python
def parallel_sum(numbers, chunk_size, max_workers=4):
    if not numbers:
        return 0
    chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        partial_sums = pool.map(sum, chunks)
    return sum(partial_sums)
```
