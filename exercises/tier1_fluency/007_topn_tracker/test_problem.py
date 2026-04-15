# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/007_topn_tracker/

from problem import *  # noqa: F401,F403

def test_all():
    import random

    # Basic add + top
    t = TopN(3)
    for v in [5, 1, 8, 3, 9, 2, 7]:
        t.add(v)
    assert t.top() == [9, 8, 7], f"got: {t.top()}"
    print("basic pass")

    # Fewer than N elements
    t = TopN(5)
    for v in [3, 1, 2]:
        t.add(v)
    assert t.top() == [3, 2, 1]
    print("under-N pass")

    # Stream of 1000 random values
    random.seed(42)
    t = TopN(10)
    stream = [random.randint(0, 10_000) for _ in range(1000)]
    for v in stream:
        t.add(v)
    expected = sorted(stream, reverse=True)[:10]
    assert t.top() == expected, f"top10 mismatch"
    print("stream pass")

    print("\nTopN tests passed")
