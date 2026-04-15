# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier3_canonical/025_versioned_kv_warmup/

from problem import *  # noqa: F401,F403

def test_all():
    """Warm-up 2 TESTS — run after scaffold or reference solution."""
    kv: VersionedKV[int] = VersionedKV()

    # Gate 1: basic set/get
    ts1 = kv.set("a", 1)
    ts2 = kv.set("a", 2)
    ts3 = kv.set("a", 3)
    assert kv.get("a") == 3
    assert kv.get("a", ts=ts1) == 1
    assert kv.get("a", ts=ts2) == 2
    print("Gate 1 passed — single-key set/get.")

    # Gate 2: time-window query across keys
    kv.set("b", 10)
    kv.set("c", 100)
    # Value should be there at current time
    assert kv.get("b") == 10
    # Value should not be visible before its ts
    assert kv.get("b", ts=ts1) is None
    print("Gate 2 passed — time-window query.")

    # Gate 4: snapshot isolation
    snap_ts = kv._clock
    snap = kv.snapshot(snap_ts)
    kv.set("a", 999)
    assert snap.get("a") == 3, "snapshot should not observe post-snapshot writes"
    assert kv.get("a") == 999
    print("Gate 4 passed — snapshot isolation.")

    print("\nAll tests passed for the gates you implemented.")
