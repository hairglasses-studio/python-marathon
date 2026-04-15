# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/011_topo_sort_kahn/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests — run after scaffold or solution

    # Simple linear chain: a -> b -> c -> d
    # a depends on b, b on c, c on d, d on nothing
    g1 = {"a": ["b"], "b": ["c"], "c": ["d"], "d": []}
    order = topo_sort(g1)
    # d must appear before c, c before b, b before a
    assert order.index("d") < order.index("c") < order.index("b") < order.index("a")
    print("Linear chain:", order)

    # Diamond: app -> [api, frontend], both -> db
    g2 = {
        "app": ["api", "frontend"],
        "api": ["db"],
        "frontend": ["db"],
        "db": [],
    }
    order = topo_sort(g2)
    assert order.index("db") < order.index("api")
    assert order.index("db") < order.index("frontend")
    assert order.index("api") < order.index("app")
    assert order.index("frontend") < order.index("app")
    print("Diamond:", order)

    # Cycle: a -> b -> a
    g3 = {"a": ["b"], "b": ["a"]}
    try:
        topo_sort(g3)
        raise AssertionError("expected ValueError on cycle")
    except ValueError as e:
        assert "cycle" in str(e).lower()
        print("Cycle detected:", e)

    print("\nKahn topological sort tests passed")
