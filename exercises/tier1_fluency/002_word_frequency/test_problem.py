# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/002_word_frequency/

from problem import *  # noqa: F401,F403

def test_all():
    text = "the cat sat on the mat the cat"
    freq = word_freq(text)
    assert freq == {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1}, f"got: {freq}"
    print("word_freq pass")

    # Case insensitive
    freq = word_freq("The THE the")
    assert freq == {"the": 3}, f"got: {freq}"
    print("case insensitive pass")

    # Empty
    assert word_freq("") == {}
    assert word_freq("   ") == {}
    print("empty pass")

    # Top N
    top = top_words("the cat sat the cat on the mat", 3)
    assert top == [("the", 3), ("cat", 2), ("mat", 1)], f"got: {top}"
    print("top_words pass")

    # Tie-break: same count, sorted alphabetically
    top = top_words("b a c a b c", 3)
    # All three appear 2 times; tie break → alphabetical
    assert top == [("a", 2), ("b", 2), ("c", 2)], f"got: {top}"
    print("tie-break pass")

    print("\nAll tests passed")
