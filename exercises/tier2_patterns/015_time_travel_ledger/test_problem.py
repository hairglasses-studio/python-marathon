# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/015_time_travel_ledger/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests

    ledger = Ledger()
    ledger.record("alice", ts=10, delta=100)    # +100 at t=10
    ledger.record("alice", ts=20, delta=-30)    # -30 at t=20
    ledger.record("alice", ts=30, delta=50)     # +50 at t=30

    # Balance at various times
    assert ledger.balance_at("alice", 5) == 0,   f"pre-first: {ledger.balance_at('alice', 5)}"
    assert ledger.balance_at("alice", 10) == 100, f"after first: {ledger.balance_at('alice', 10)}"
    assert ledger.balance_at("alice", 15) == 100, f"mid-gap: {ledger.balance_at('alice', 15)}"
    assert ledger.balance_at("alice", 20) == 70,  f"after second: {ledger.balance_at('alice', 20)}"
    assert ledger.balance_at("alice", 30) == 120, f"after third: {ledger.balance_at('alice', 30)}"
    assert ledger.balance_at("alice", 999) == 120, "after all"

    # Unknown account
    assert ledger.balance_at("bob", 100) == 0

    # Second account doesn't interfere
    ledger.record("bob", ts=15, delta=500)
    assert ledger.balance_at("bob", 15) == 500
    assert ledger.balance_at("alice", 15) == 100  # alice unchanged

    print("Ledger time-travel tests passed")
