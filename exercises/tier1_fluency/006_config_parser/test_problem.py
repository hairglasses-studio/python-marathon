# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/006_config_parser/

from problem import *  # noqa: F401,F403

def test_all():
    # Happy path
    text = """
    name=mitch
    role=eng
    # this is a comment
    email=m@example.com
    """
    result = parse_config(text)
    assert result == {"name": "mitch", "role": "eng", "email": "m@example.com"}, f"got: {result}"
    print("happy path pass")

    # Empty input
    assert parse_config("") == {}
    assert parse_config("\n\n\n") == {}
    print("empty pass")

    # Syntax error: missing =
    try:
        parse_config("name=mitch\ninvalid line")
        raise AssertionError("expected ConfigSyntaxError")
    except ConfigSyntaxError as e:
        assert e.line_number == 2, f"got line {e.line_number}"
        print("syntax error pass")

    # Syntax error: empty key
    try:
        parse_config("=value")
        raise AssertionError("expected ConfigSyntaxError")
    except ConfigSyntaxError as e:
        assert e.line_number == 1
        print("empty key pass")

    # Duplicate key
    try:
        parse_config("a=1\nb=2\na=3")
        raise AssertionError("expected ConfigDuplicateKeyError")
    except ConfigDuplicateKeyError as e:
        assert e.key == "a"
        print("duplicate pass")

    # Catching the base class works
    try:
        parse_config("bad line")
    except ConfigError:
        print("base class catch pass")

    print("\nparse_config tests passed")
