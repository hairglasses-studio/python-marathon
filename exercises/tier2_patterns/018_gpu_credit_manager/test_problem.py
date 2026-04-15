# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/018_gpu_credit_manager/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests

    cm = CreditManager()

    # Basic add + balance
    cm.add("alice", amount=100, expiry_ts=20)
    assert cm.balance("alice", now_ts=10) == 100
    print("Gate 1 pass — basic add/balance")

    # Deduct from a single bucket
    cm.deduct("alice", amount=30, now_ts=10)
    assert cm.balance("alice", now_ts=10) == 70
    print("Gate 2a pass — single-bucket deduct")

    # Add a second bucket expiring later
    cm.add("alice", amount=50, expiry_ts=40)
    assert cm.balance("alice", now_ts=10) == 120

    # Deduct 80 — should drain the soonest-expiring bucket (70) and take 10 from the later one
    cm.deduct("alice", amount=80, now_ts=10)
    assert cm.balance("alice", now_ts=10) == 40
    print("Gate 2b pass — expiry-ordered deduct")

    # Expired credits don't count toward balance
    cm.add("bob", amount=200, expiry_ts=30)
    assert cm.balance("bob", now_ts=10) == 200
    assert cm.balance("bob", now_ts=30) == 200  # boundary: still valid AT expiry
    assert cm.balance("bob", now_ts=31) == 0
    print("Gate 3 pass — lazy expiry")

    # Insufficient credits
    cm.add("carol", amount=10, expiry_ts=50)
    try:
        cm.deduct("carol", amount=100, now_ts=10)
        raise AssertionError("expected InsufficientCredits")
    except InsufficientCredits:
        pass
    assert cm.balance("carol", now_ts=10) == 10  # unchanged
    print("Gate 4 pass — insufficient credits")

    print("\nCredit manager tests passed")
