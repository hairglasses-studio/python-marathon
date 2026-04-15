# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/013_transitive_dependents/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests

    g = {
        "app": ["api", "frontend"],
        "api": ["db", "auth"],
        "frontend": ["api"],
        "db": [],
        "auth": [],
    }

    # Nothing depends on "app"
    assert transitive_dependents(g, "app") == set()
    print("app has no dependents: pass")

    # api is depended on by: frontend (direct), app (via api + via frontend)
    assert transitive_dependents(g, "api") == {"app", "frontend"}
    print("api dependents: pass")

    # db is depended on by: api (direct), frontend (via api), app (via api, via frontend)
    assert transitive_dependents(g, "db") == {"api", "frontend", "app"}
    print("db dependents: pass")

    # auth is depended on by: api, frontend (via api), app
    assert transitive_dependents(g, "auth") == {"api", "frontend", "app"}
    print("auth dependents: pass")

    print("\nTransitive dependents tests passed")
