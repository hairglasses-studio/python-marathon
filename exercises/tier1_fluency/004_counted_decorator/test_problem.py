# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/004_counted_decorator/

from problem import *  # noqa: F401,F403

def test_all():
    @counted
    def greet(name):
        return f"hi {name}"

    assert greet.call_count == 0
    greet("a")
    greet("b")
    greet("c")
    assert greet.call_count == 3, f"got {greet.call_count}"
    print("basic counting pass")

    # Preserves the return value
    @counted
    def square(x):
        return x * x

    assert square(5) == 25
    assert square.call_count == 1
    print("return-value pass")

    # Preserves name via @wraps
    @counted
    def my_function():
        """My docstring."""
        pass

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "My docstring."
    print("wraps pass")

    print("\ncounted decorator tests passed")
