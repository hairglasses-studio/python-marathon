import asyncio

from problem import (
    Budget,
    BudgetExhausted,
    RetryableError,
    TerminalError,
    ToolCall,
    ToolResult,
    invoke_all,
)


def test_all():
    # --- Helpers: fake backends ---
    def make_success_backend(value: str):
        async def backend(call: ToolCall):
            return f"{value}:{call.name}"
        return backend

    def make_flaky_backend(fail_n: int, value: str):
        state = {"calls": {}}

        async def backend(call: ToolCall):
            n = state["calls"].get(call.name, 0) + 1
            state["calls"][call.name] = n
            if n <= fail_n:
                raise RetryableError(f"flaky #{n}")
            return f"{value}:{call.name}"
        return backend

    async def terminal_backend(call: ToolCall):
        raise TerminalError("permanent")

    calls = [ToolCall(name=f"t{i}") for i in range(3)]

    # Basic success path
    results = asyncio.run(
        invoke_all(calls, make_success_backend("ok"), budget=Budget(total_retries=10))
    )
    assert len(results) == 3
    assert all(r.ok for r in results)
    assert results[0].value == "ok:t0"
    assert results[1].value == "ok:t1"
    assert results[2].value == "ok:t2"

    # Flaky: each call fails twice then succeeds — uses 2 budget per call = 6 total
    results = asyncio.run(
        invoke_all(
            calls,
            make_flaky_backend(fail_n=2, value="ok"),
            budget=Budget(total_retries=10),
            max_attempts=5,
        )
    )
    assert all(r.ok for r in results), results
    assert all(r.attempts == 3 for r in results), [r.attempts for r in results]

    # Terminal error: no retry, ok=False
    results = asyncio.run(
        invoke_all(calls, terminal_backend, budget=Budget(total_retries=10))
    )
    assert all(not r.ok for r in results)
    assert all(r.attempts == 1 for r in results)

    # Budget exhaustion: 3 calls × 2 failures but only 3 budget → some fail with exhaustion
    results = asyncio.run(
        invoke_all(
            calls,
            make_flaky_backend(fail_n=3, value="ok"),
            budget=Budget(total_retries=3),
            max_attempts=5,
        )
    )
    # Not all can succeed — at least one should fail with budget-related error
    assert not all(r.ok for r in results), "expected some failures due to budget"
    # Order must still be preserved
    assert len(results) == 3

    # Preserves input order
    ordered_calls = [ToolCall(name="a"), ToolCall(name="b"), ToolCall(name="c")]
    results = asyncio.run(
        invoke_all(ordered_calls, make_success_backend("v"), budget=Budget(total_retries=10))
    )
    assert [r.value for r in results] == ["v:a", "v:b", "v:c"]
