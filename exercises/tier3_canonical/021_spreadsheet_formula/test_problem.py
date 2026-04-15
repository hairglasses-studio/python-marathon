# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier3_canonical/021_spreadsheet_formula/

from problem import *  # noqa: F401,F403

def test_all():
    """Spreadsheet tests — run after scaffold or reference solution."""

    sheet = Spreadsheet()

    # --- Gate 1: literal + simple references ---
    sheet.set_cell("A1", 5)
    sheet.set_cell("A2", 10)
    assert sheet.get_cell("A1") == 5
    assert sheet.get_cell("A2") == 10
    assert sheet.get_cell("A99") == 0    # unset cell reads as 0
    print("Gate 1a pass — literal values")

    sheet.set_cell("B1", "=A1+A2")
    assert sheet.get_cell("B1") == 15
    print("Gate 1b pass — simple formula")

    # Nested references
    sheet.set_cell("C1", "=B1+A1")      # 15 + 5 = 20
    assert sheet.get_cell("C1") == 20
    print("Gate 1c pass — nested reference")

    # Formula with a literal
    sheet.set_cell("D1", "=A1+10")
    assert sheet.get_cell("D1") == 15
    print("Gate 1d pass — formula with literal")

    # Update propagation via lazy get_cell
    sheet.set_cell("A1", 100)
    assert sheet.get_cell("B1") == 110    # 100 + 10
    assert sheet.get_cell("C1") == 210    # 110 + 100
    print("Gate 1e pass — lazy re-evaluation")

    # --- Gate 2: cycle detection ---
    sheet2 = Spreadsheet()
    sheet2.set_cell("A1", "=B1")
    sheet2.set_cell("B1", "=A1")    # cycle: A1 → B1 → A1
    try:
        sheet2.get_cell("A1")
        raise AssertionError("expected CycleError")
    except CycleError:
        pass
    print("Gate 2a pass — direct cycle")

    sheet3 = Spreadsheet()
    sheet3.set_cell("A1", "=B1")
    sheet3.set_cell("B1", "=C1")
    sheet3.set_cell("C1", "=A1")    # cycle via 3 nodes
    try:
        sheet3.get_cell("A1")
        raise AssertionError("expected CycleError")
    except CycleError:
        pass
    print("Gate 2b pass — transitive cycle")

    # Self-reference
    sheet4 = Spreadsheet()
    sheet4.set_cell("A1", "=A1")
    try:
        sheet4.get_cell("A1")
        raise AssertionError("expected CycleError")
    except CycleError:
        pass
    print("Gate 2c pass — self-reference")

    # --- Gate 3: O(1) get_cell via proactive propagation ---
    # (Skipped if you didn't implement gate 3; leave the ref solution to cover it.)
    # A correctness check: even with proactive evaluation, values should still update.
    sheet5 = Spreadsheet()
    sheet5.set_cell("A", 1)
    sheet5.set_cell("B", "=A+A")
    sheet5.set_cell("C", "=B+A")
    assert sheet5.get_cell("C") == 3

    sheet5.set_cell("A", 10)
    assert sheet5.get_cell("B") == 20
    assert sheet5.get_cell("C") == 30
    print("Gate 3 pass — propagation on update")

    print("\nSpreadsheet tests passed")
