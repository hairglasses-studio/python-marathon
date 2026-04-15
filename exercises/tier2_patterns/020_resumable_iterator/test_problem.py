# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/020_resumable_iterator/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests

    items = ["a", "b", "c", "d", "e"]
    it = ListIterator(items)

    # Basic iteration
    assert it.next() == "a"
    assert it.next() == "b"
    print("Gate 1a pass — basic iteration")

    # Snapshot state mid-iteration
    saved = it.get_state()
    print(f"  saved state: {saved}")

    # Continue from where we were
    assert it.next() == "c"
    assert it.next() == "d"
    print("Gate 1b pass — continue past snapshot")

    # Restore and re-iterate the saved portion
    it.set_state(saved)
    assert it.next() == "c"
    assert it.next() == "d"
    assert it.next() == "e"
    print("Gate 2 pass — restore and replay")

    # StopIteration at end
    try:
        it.next()
        raise AssertionError("expected StopIteration")
    except StopIteration:
        pass
    print("Gate 3 pass — StopIteration at end")

    # State must be JSON-serializable
    import json
    it2 = ListIterator([1, 2, 3])
    it2.next()
    s = it2.get_state()
    roundtrip = json.loads(json.dumps(s))
    it2.set_state(roundtrip)
    assert it2.next() == 2
    print("Gate 4 pass — state is JSON-serializable")

    print("\nResumable iterator tests passed")
