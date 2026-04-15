# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/014_content_addressed_cache/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests
    call_counts = {"doubler": 0}

    def doubler(inputs: dict) -> int:
        call_counts["doubler"] += 1
        return inputs["x"] * 2

    cache = ContentCache()

    # First call: miss + compute
    assert cache.compute("double", {"x": 5}, doubler) == 10
    assert call_counts["doubler"] == 1

    # Second call with same inputs: hit, no recompute
    assert cache.compute("double", {"x": 5}, doubler) == 10
    assert call_counts["doubler"] == 1  # still 1

    # Different inputs: miss + compute
    assert cache.compute("double", {"x": 7}, doubler) == 14
    assert call_counts["doubler"] == 2

    # Same dict, different insertion order → same hash → cache hit
    assert cache.compute("double", {"x": 5}, doubler) == 10
    assert call_counts["doubler"] == 2

    # Different name → different key even if inputs match
    assert cache.compute("other", {"x": 5}, doubler) == 10
    assert call_counts["doubler"] == 3

    hits, misses = cache.stats()
    assert hits == 2 and misses == 3, f"hits={hits} misses={misses}"

    print("Content cache tests passed")
    print(f"  hits={hits} misses={misses}")
