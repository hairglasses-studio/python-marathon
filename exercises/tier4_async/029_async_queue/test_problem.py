import asyncio
import time

from problem import pipeline


def test_all():
    async def double(x: int) -> int:
        await asyncio.sleep(0.02)
        return x * 2

    # Basic correctness
    result = asyncio.run(pipeline([1, 2, 3, 4, 5], double, num_workers=3))
    assert result == [2, 4, 6, 8, 10], result

    # Empty input
    assert asyncio.run(pipeline([], double)) == []

    # Concurrency — 10 items, 20ms each, 5 workers = ~40ms not 200ms
    start = time.monotonic()
    asyncio.run(pipeline(list(range(10)), double, num_workers=5))
    elapsed = time.monotonic() - start
    assert elapsed < 0.15, f"took {elapsed:.3f}s — workers not parallel"

    # Order preserved even when process times vary
    async def variable(x: int) -> int:
        # Later items finish faster — test that order is by input, not completion
        await asyncio.sleep(0.05 - x * 0.005)
        return x * 10

    result = asyncio.run(pipeline([1, 2, 3, 4, 5], variable, num_workers=5))
    assert result == [10, 20, 30, 40, 50], result
