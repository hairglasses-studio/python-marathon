import asyncio

from problem import AsyncBatcher


def test_all():
    async def async_range(n: int):
        for i in range(n):
            yield i

    # Basic: 10 items in batches of 3 → [[0,1,2],[3,4,5],[6,7,8],[9]]
    async def collect_basic():
        return [batch async for batch in AsyncBatcher(async_range(10), batch_size=3)]

    batches = asyncio.run(collect_basic())
    assert batches == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]], batches

    # Exact multiple: 6 items in batches of 3 → [[0,1,2],[3,4,5]]
    async def collect_exact():
        return [batch async for batch in AsyncBatcher(async_range(6), batch_size=3)]

    assert asyncio.run(collect_exact()) == [[0, 1, 2], [3, 4, 5]]

    # Empty source
    async def empty():
        if False:
            yield 0

    async def collect_empty():
        return [batch async for batch in AsyncBatcher(empty(), batch_size=3)]

    assert asyncio.run(collect_empty()) == []

    # Single item
    async def one():
        yield 42

    async def collect_one():
        return [batch async for batch in AsyncBatcher(one(), batch_size=3)]

    assert asyncio.run(collect_one()) == [[42]]

    # Batch size 1 (degenerate)
    async def collect_one_by_one():
        return [batch async for batch in AsyncBatcher(async_range(4), batch_size=1)]

    assert asyncio.run(collect_one_by_one()) == [[0], [1], [2], [3]]
