# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/005_int_range/

from problem import *  # noqa: F401,F403

def test_all():
    r = IntRange(1, 5)
    assert len(r) == 4
    assert list(r) == [1, 2, 3, 4]
    print("basic pass")

    # Membership
    assert 3 in r
    assert 5 not in r   # stop is exclusive
    assert 1 in r
    assert 0 not in r
    print("membership pass")

    # Repr
    assert repr(r) == "IntRange(1, 5)"
    print("repr pass")

    # Equality
    assert IntRange(1, 5) == IntRange(1, 5)
    assert IntRange(1, 5) != IntRange(1, 6)
    print("eq pass")

    # Hash
    points = {IntRange(0, 5), IntRange(0, 5), IntRange(0, 10)}
    assert len(points) == 2
    print("hash pass")

    # Empty range
    empty = IntRange(5, 5)
    assert len(empty) == 0
    assert list(empty) == []
    print("empty pass")

    print("\nIntRange tests passed")
