# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/010_dfs_traversal/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests — run after scaffold or solution
    g = {
        "a": ["b", "c"],
        "b": ["d"],
        "c": ["d", "e"],
        "d": [],
        "e": [],
    }
    result = dfs(g, "a")

    # Start node is first
    assert result[0] == "a", f"expected 'a' first, got {result[0]}"

    # Every reachable node appears exactly once
    assert set(result) == {"a", "b", "c", "d", "e"}, f"missing nodes: {result}"
    assert len(result) == len(set(result)), "duplicates in result"

    # b's subtree comes before c's (pre-order + neighbor order)
    assert result.index("b") < result.index("c"), "wrong neighbor order"

    # d should not be visited twice (it's reachable from both b and c)
    assert result.count("d") == 1

    print("DFS tests passed:", result)
