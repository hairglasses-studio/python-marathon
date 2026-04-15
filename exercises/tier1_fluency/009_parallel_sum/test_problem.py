# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/009_parallel_sum/

from problem import *  # noqa: F401,F403

def test_all():
    # Basic correctness
    assert parallel_sum([1, 2, 3, 4, 5], chunk_size=2) == 15
    assert parallel_sum(list(range(100)), chunk_size=10) == sum(range(100))
    print("basic pass")

    # Edge cases
    assert parallel_sum([], chunk_size=10) == 0
    assert parallel_sum([42], chunk_size=10) == 42
    print("edge cases pass")

    # Larger input
    big = list(range(10_000))
    assert parallel_sum(big, chunk_size=500) == sum(big)
    print("large input pass")

    # Chunk size larger than input
    assert parallel_sum([1, 2, 3], chunk_size=100) == 6
    print("oversized chunk pass")

    print("\nparallel_sum tests passed")
