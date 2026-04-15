import asyncio
import time

from problem import fetch_all


def test_all():
    async def slow_fetch(url: str) -> str:
        await asyncio.sleep(0.05)
        return f"body:{url}"

    # Basic correctness + order preservation
    urls = [f"https://x/{i}" for i in range(10)]
    result = asyncio.run(fetch_all(urls, slow_fetch, concurrency=5))
    assert result == [f"body:https://x/{i}" for i in range(10)], result

    # Concurrency — 10 fetches of 50ms each with concurrency=5 should take
    # ~100ms, not 500ms. Give generous slack for CI jitter.
    start = time.monotonic()
    asyncio.run(fetch_all(urls, slow_fetch, concurrency=5))
    elapsed = time.monotonic() - start
    assert elapsed < 0.35, f"took {elapsed:.3f}s — not concurrent enough"

    # Exception propagation
    async def flaky(url: str) -> str:
        if "bad" in url:
            raise ValueError(f"bad url: {url}")
        return url

    try:
        asyncio.run(fetch_all(["good1", "bad1", "good2"], flaky))
    except ValueError as e:
        assert "bad1" in str(e)
    else:
        raise AssertionError("expected ValueError from flaky fetch")

    # Empty input
    assert asyncio.run(fetch_all([], slow_fetch)) == []

    # Single item
    assert asyncio.run(fetch_all(["only"], slow_fetch)) == ["body:only"]
