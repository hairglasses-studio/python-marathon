# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/003_windowed_generator/

from problem import *  # noqa: F401,F403

def test_all():
    result = list(windows([1, 2, 3, 4, 5], 3))
    assert result == [(1, 2, 3), (2, 3, 4), (3, 4, 5)], f"got: {result}"
    print("size 3 pass")

    # Window size equal to length
    result = list(windows([1, 2, 3], 3))
    assert result == [(1, 2, 3)]
    print("exact length pass")

    # Window size larger than sequence
    result = list(windows([1, 2], 3))
    assert result == []
    print("too-short pass")

    # Size 1
    result = list(windows([1, 2, 3], 1))
    assert result == [(1,), (2,), (3,)]
    print("size 1 pass")

    # Works with any iterable, not just lists
    result = list(windows(range(5), 2))
    assert result == [(0, 1), (1, 2), (2, 3), (3, 4)]
    print("range pass")

    print("\nwindows tests passed")
