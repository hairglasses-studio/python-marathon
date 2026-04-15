# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier3_canonical/023_in_memory_sql/

from problem import *  # noqa: F401,F403

def test_all():
    """SQL database tests — run after scaffold or solution."""

    db = Database()

    # --- Gate 1: create + insert + select all ---
    db.create_table("users", columns=["id", "name", "age", "role"])
    db.insert("users", {"id": 1, "name": "alice", "age": 30, "role": "eng"})
    db.insert("users", {"id": 2, "name": "bob",   "age": 25, "role": "eng"})
    db.insert("users", {"id": 3, "name": "carol", "age": 40, "role": "pm"})
    db.insert("users", {"id": 4, "name": "dave",  "age": 35, "role": "eng"})

    rows = db.select("users")
    assert len(rows) == 4
    print("Gate 1a pass — select all")

    # Column projection
    rows = db.select("users", columns=["name"])
    assert rows == [{"name": "alice"}, {"name": "bob"}, {"name": "carol"}, {"name": "dave"}]
    print("Gate 1b pass — column projection")

    # Missing table
    try:
        db.select("nope")
        raise AssertionError("expected TableNotFound")
    except TableNotFound:
        pass
    print("Gate 1c pass — missing table")

    # Schema enforcement
    try:
        db.insert("users", {"id": 5, "name": "x", "nonsense": "y"})
        raise AssertionError("expected SchemaError")
    except SchemaError:
        pass
    print("Gate 1d pass — schema enforcement")

    # Partial row is OK (missing columns read as None)
    db.insert("users", {"id": 5, "name": "eve"})
    eve = db.select("users", where=lambda r: r["id"] == 5)[0]
    assert eve["age"] is None and eve["role"] is None
    print("Gate 1e pass — partial row")

    # --- Gate 2: where predicate ---
    eng = db.select("users", where=lambda r: r["role"] == "eng")
    assert len(eng) == 3
    assert {r["name"] for r in eng} == {"alice", "bob", "dave"}
    print("Gate 2a pass — where equality")

    older_than_30 = db.select("users", where=lambda r: (r["age"] or 0) > 30)
    assert {r["name"] for r in older_than_30} == {"carol", "dave"}
    print("Gate 2b pass — where with comparison")

    # Compound predicates
    young_eng = db.select("users", where=lambda r: r["role"] == "eng" and (r["age"] or 99) < 30)
    assert {r["name"] for r in young_eng} == {"bob"}
    print("Gate 2c pass — where with AND")

    # --- Gate 3: order_by ---
    by_age = db.select("users", where=lambda r: r["age"] is not None, order_by=["age"])
    ages = [r["age"] for r in by_age]
    assert ages == sorted(ages)
    print("Gate 3a pass — order_by ascending")

    by_age_desc = db.select("users", where=lambda r: r["age"] is not None, order_by=["-age"])
    ages = [r["age"] for r in by_age_desc]
    assert ages == sorted(ages, reverse=True)
    print("Gate 3b pass — order_by descending")

    # Multi-column: role ascending, age descending
    db2 = Database()
    db2.create_table("t", columns=["role", "age", "name"])
    for role, age, name in [
        ("eng", 30, "a"),
        ("pm",  25, "b"),
        ("eng", 25, "c"),
        ("eng", 35, "d"),
        ("pm",  30, "e"),
    ]:
        db2.insert("t", {"role": role, "age": age, "name": name})

    rows = db2.select("t", order_by=["role", "-age"])
    # Expected: eng rows by age desc, then pm rows by age desc
    # eng: (35, d), (30, a), (25, c)
    # pm:  (30, e), (25, b)
    ordered_names = [r["name"] for r in rows]
    assert ordered_names == ["d", "a", "c", "e", "b"], f"got: {ordered_names}"
    print("Gate 3c pass — multi-column order")

    # Combined: where + order_by + columns
    rows = db.select(
        "users",
        where=lambda r: r["role"] == "eng",
        order_by=["-age"],
        columns=["name", "age"],
    )
    assert rows == [
        {"name": "dave", "age": 35},
        {"name": "alice", "age": 30},
        {"name": "bob", "age": 25},
    ]
    print("Gate 3d pass — combined")

    print("\nDatabase tests passed")
