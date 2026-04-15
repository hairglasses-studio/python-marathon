# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier1_fluency/008_temp_attr_context/

from problem import *  # noqa: F401,F403

def test_all():
    class Config:
        rate = 100
        level = "INFO"

    # Override existing attr
    with temp_attr(Config, "rate", 999):
        assert Config.rate == 999
    assert Config.rate == 100
    print("override existing pass")

    # Set previously-missing attr
    assert not hasattr(Config, "new_field")
    with temp_attr(Config, "new_field", "hello"):
        assert Config.new_field == "hello"
    assert not hasattr(Config, "new_field")
    print("set new pass")

    # Exception inside with: still restores
    try:
        with temp_attr(Config, "rate", 42):
            assert Config.rate == 42
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert Config.rate == 100, f"not restored: {Config.rate}"
    print("exception pass")

    print("\ntemp_attr tests passed")
