# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/019_path_normalize/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests

    # Absolute new_dir
    assert normalize("/home/user", "/etc") == "/etc"
    assert normalize("/", "/foo") == "/foo"
    print("Absolute: pass")

    # Simple relative
    assert normalize("/home/user", "docs") == "/home/user/docs"
    assert normalize("/home/user", "a/b/c") == "/home/user/a/b/c"
    print("Relative: pass")

    # Dots
    assert normalize("/home/user", ".") == "/home/user"
    assert normalize("/home/user", "./docs") == "/home/user/docs"
    assert normalize("/home/user", "../") == "/home"
    assert normalize("/home/user", "../../") == "/"
    assert normalize("/home/user", "docs/../photos") == "/home/user/photos"
    print("Dots: pass")

    # Can't go above root
    assert normalize("/", "..") == "/"
    assert normalize("/", "../../..") == "/"
    print("Root boundary: pass")

    # Complex example from the problem statement
    assert normalize("/home/user", "docs/../photos/./img.png") == "/home/user/photos/img.png"
    print("Canonical example: pass")

    # Double slashes
    assert normalize("/home/user", "a//b") == "/home/user/a/b"
    print("Double slashes: pass")

    # Trailing components
    assert normalize("/home/user/docs", ".") == "/home/user/docs"

    print("\nPath normalization tests passed")
