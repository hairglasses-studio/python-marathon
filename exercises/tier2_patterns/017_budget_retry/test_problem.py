# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/017_budget_retry/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests
    import time

    # Test harness: a flaky function factory
    def make_flaky(fail_n: int, then_value: str = "ok"):
        state = {"calls": 0}
        def fn():
            state["calls"] += 1
            if state["calls"] <= fail_n:
                raise RetryableError(f"flake attempt {state['calls']}")
            return then_value
        fn.call_count = lambda: state["calls"]
        return fn

    # Silent sleep so tests don't wait
    def silent_sleep(_s): pass

    # 1. Happy path: fn succeeds first try
    happy = lambda: "hello"
    assert retry(happy, budget=3, sleep=silent_sleep) == "hello"
    print("Gate 1 pass — happy path")

    # 2. Retry on RetryableError
    flaky = make_flaky(fail_n=2, then_value="eventual")
    result = retry(flaky, budget=5, sleep=silent_sleep)
    assert result == "eventual"
    assert flaky.call_count() == 3
    print("Gate 2 pass — retries then succeeds")

    # 3. Terminal error raises immediately
    def terminal_fn():
        raise TerminalError("nope")
    try:
        retry(terminal_fn, budget=5, sleep=silent_sleep)
        raise AssertionError("expected TerminalError")
    except TerminalError as e:
        assert "nope" in str(e)
    print("Gate 3 pass — terminal raises immediately")

    # 4. Budget exhaustion
    always_flaky = lambda: (_ for _ in ()).throw(RetryableError("always"))
    try:
        retry(always_flaky, budget=3, sleep=silent_sleep)
        raise AssertionError("expected BudgetExhausted")
    except BudgetExhausted:
        pass
    print("Gate 4 pass — budget exhausted")

    # 5. Zero budget
    try:
        retry(happy, budget=0, sleep=silent_sleep)
        raise AssertionError("expected BudgetExhausted")
    except BudgetExhausted:
        pass
    print("Gate 5 pass — zero budget")

    # 6. Backoff is invoked the right number of times
    slept: list[float] = []
    def recording_sleep(s: float) -> None: slept.append(s)
    flaky = make_flaky(fail_n=2)
    retry(flaky, budget=5, sleep=recording_sleep, backoff=lambda a: 0.01 * (a + 1))
    # Should have slept 2 times (once after each flake, before the successful 3rd call)
    assert len(slept) == 2, f"slept {slept}"
    print("Gate 6 pass — backoff invoked correctly")

    print("\nRetry tests passed")
