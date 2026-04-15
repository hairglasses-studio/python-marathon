# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/012_three_color_cycle/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests

    # No cycle: linear chain
    assert has_cycle({"a": ["b"], "b": ["c"], "c": []}) is False
    print("No-cycle linear: pass")

    # No cycle: diamond
    assert has_cycle({
        "app": ["api", "frontend"],
        "api": ["db"],
        "frontend": ["db"],
        "db": [],
    }) is False
    print("No-cycle diamond: pass")

    # Cycle: 2-node
    assert has_cycle({"a": ["b"], "b": ["a"]}) is True
    print("2-node cycle: pass")

    # Cycle: 3-node
    assert has_cycle({"a": ["b"], "b": ["c"], "c": ["a"]}) is True
    print("3-node cycle: pass")

    # Self-loop
    assert has_cycle({"a": ["a"]}) is True
    print("Self-loop: pass")

    # Multiple components, one has a cycle
    assert has_cycle({
        "a": ["b"], "b": [],
        "x": ["y"], "y": ["x"],  # cycle here
    }) is True
    print("Multi-component: pass")

    print("\nCycle detection tests passed")
