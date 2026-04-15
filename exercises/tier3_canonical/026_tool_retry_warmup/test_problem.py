# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier3_canonical/026_tool_retry_warmup/

from problem import *  # noqa: F401,F403

def test_all():
    """Warm-up 3 TESTS — run after the scaffold or reference solution cell."""

    # --- Fake backend factories for isolated tests ---
    def make_success_backend(value: str) -> ToolBackend:
        def _backend(call: ToolCall) -> Any:
            return value
        return _backend


    def make_flaky_backend(fail_n_times: int, then_value: str) -> ToolBackend:
        state = {"calls": 0}
        def _backend(call: ToolCall) -> Any:
            state["calls"] += 1
            if state["calls"] <= fail_n_times:
                raise RetryableError(f"flaked attempt {state['calls']}")
            return then_value
        return _backend


    def make_terminal_backend() -> ToolBackend:
        def _backend(call: ToolCall) -> Any:
            raise AuthError("bad creds")
        return _backend


    def make_ratelimit_backend(delays: list[float]) -> ToolBackend:
        state = {"calls": 0}
        def _backend(call: ToolCall) -> Any:
            state["calls"] += 1
            if state["calls"] <= len(delays):
                raise RateLimitError(
                    f"rate limited attempt {state['calls']}",
                    retry_after=delays[state['calls'] - 1],
                )
            return "ok"
        return _backend


    # --- Silent sleep so tests don't wait ---
    def fake_sleep(_s: float) -> None:
        pass


    call = ToolCall(name="read_file", args={"path": "foo.txt"})

    # Gate 1: happy path
    r1 = invoke(call, make_success_backend("hello"), budget=Budget.of(3), sleep=fake_sleep)
    assert r1.ok is True
    assert r1.value == "hello"
    assert r1.attempts == 1
    print("Gate 1 passed — happy path.")

    # Gate 2: retry on RetryableError, then succeed
    r2 = invoke(
        call,
        make_flaky_backend(fail_n_times=2, then_value="eventual"),
        budget=Budget.of(5),
        sleep=fake_sleep,
    )
    assert r2.ok is True
    assert r2.value == "eventual"
    assert r2.attempts == 3
    print("Gate 2 passed — retry with backoff.")

    # Gate 3: AuthError is terminal
    r3 = invoke(
        call, make_terminal_backend(), budget=Budget.of(5), sleep=fake_sleep,
    )
    assert r3.ok is False
    assert "bad creds" in (r3.error or "")
    print("Gate 3a passed — AuthError is terminal.")

    # Gate 3: RateLimitError honors retry_after
    slept: list[float] = []
    def recording_sleep(s: float) -> None:
        slept.append(s)

    r4 = invoke(
        call,
        make_ratelimit_backend([0.5, 1.5]),
        budget=Budget.of(5),
        sleep=recording_sleep,
    )
    assert r4.ok is True
    assert r4.attempts == 3
    assert slept[0] >= 0.5 and slept[1] >= 1.5, f"slept was {slept}"
    print("Gate 3b passed — RateLimitError honored retry_after.")

    # Gate 4: budget exhaustion
    def always_retryable(call: ToolCall) -> Any:
        raise RetryableError("always")

    r5 = invoke(call, always_retryable, budget=Budget.of(3), sleep=fake_sleep)
    assert r5.ok is False
    assert r5.attempts == 3
    print("Gate 4 passed — budget exhaustion terminates cleanly.")

    print("\nAll warm-up 3 tests passed.")
