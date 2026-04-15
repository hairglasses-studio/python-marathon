# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier3_canonical/024_dep_graph_warmup/

from problem import *  # noqa: F401,F403

def test_all():
    """Warm-up 1 TESTS — run this after you fill in the scaffold."""
    # Run this cell after the scaffold or solution cell above.

    g = DepGraph()
    g.add_target("a", inputs=[], build_fn=lambda d: "a-out")
    g.add_target("b", inputs=["a"], build_fn=lambda d: d["a"] + "-b")
    g.add_target("c", inputs=["a", "b"], build_fn=lambda d: d["a"] + d["b"] + "-c")

    # Gate 1
    assert g.build("a") == "a-out"
    assert g.build("b") == "a-out-b"
    assert g.build("c") == "a-outa-out-b-c"
    print("Gate 1 passed — basic topological build works.")

    # Gate 2 — rebuild should be cached
    call_count = {"n": 0}
    def counted_a(_: dict[str, object]) -> str:
        call_count["n"] += 1
        return "a-out"

    g2 = DepGraph()
    g2.add_target("a", inputs=[], build_fn=counted_a)
    g2.add_target("b", inputs=["a"], build_fn=lambda d: d["a"] + "-b")
    g2.build("b")
    g2.build("b")
    assert call_count["n"] == 1, f"expected 1 call, got {call_count['n']}"

    # Invalidation should force a rebuild
    g2.invalidate("a")
    g2.build("b")
    assert call_count["n"] == 2
    print("Gate 2 passed — caching + invalidation works.")

    # Gate 4 — cycle detection
    g3 = DepGraph()
    g3.add_target("a", inputs=["b"], build_fn=lambda d: None)
    g3.add_target("b", inputs=["a"], build_fn=lambda d: None)
    try:
        g3.check_cycles()
        raise AssertionError("expected CycleError")
    except CycleError:
        print("Gate 4 passed — cycle detection works.")

    print("\nAll tests passed for the gates you implemented.")
