import asyncio

from problem import RetryableError, TerminalError, retry


def test_all():
    # Success on first try
    async def ok():
        return "yay"

    assert asyncio.run(retry(ok)) == "yay"

    # Recovers after transient failures
    state = {"calls": 0}

    async def flaky():
        state["calls"] += 1
        if state["calls"] < 3:
            raise RetryableError("try again")
        return "finally"

    result = asyncio.run(retry(flaky, max_attempts=5, base_delay=0.001))
    assert result == "finally"
    assert state["calls"] == 3

    # Exhausts retries
    state["calls"] = 0

    async def always_fails():
        state["calls"] += 1
        raise RetryableError("nope")

    try:
        asyncio.run(retry(always_fails, max_attempts=3, base_delay=0.001))
    except RetryableError:
        assert state["calls"] == 3
    else:
        raise AssertionError("expected RetryableError after exhausting attempts")

    # Terminal error stops immediately
    state["calls"] = 0

    async def terminal():
        state["calls"] += 1
        raise TerminalError("no retry for you")

    try:
        asyncio.run(retry(terminal, max_attempts=5, base_delay=0.001))
    except TerminalError:
        assert state["calls"] == 1
    else:
        raise AssertionError("expected TerminalError")

    # Non-retry exceptions pass through
    async def value_err():
        raise ValueError("bad input")

    try:
        asyncio.run(retry(value_err))
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError to pass through")
