# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/001_fizzbuzz/

from problem import *  # noqa: F401,F403

def test_all():
    expected = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                "11", "Fizz", "13", "14", "FizzBuzz"]
    assert fizzbuzz(15) == expected, f"got: {fizzbuzz(15)}"
    assert fizzbuzz(1) == ["1"]
    assert fizzbuzz(3) == ["1", "2", "Fizz"]
    print("fizzbuzz tests passed")
