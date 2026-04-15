# Tests — do not edit. Run via:
#   python marathon.py run NNN
#   pytest tier2_patterns/016_per_key_locking/

from problem import *  # noqa: F401,F403

def test_all():
    # Tests
    import threading
    import time

    locker = KeyedLocker()
    results: dict[str, list[int]] = {"a": [], "b": []}

    def worker(key: str, value: int) -> None:
        with locker.lock(key):
            # Simulate some work inside the critical section
            current = list(results[key])
            time.sleep(0.001)
            current.append(value)
            results[key] = current

    # Launch many threads on two keys — they should NOT interfere with each other
    threads = []
    for i in range(20):
        threads.append(threading.Thread(target=worker, args=("a", i)))
        threads.append(threading.Thread(target=worker, args=("b", i * 100)))
    for t in threads: t.start()
    for t in threads: t.join()

    # Each key should have exactly 20 results (no lost updates)
    assert len(results["a"]) == 20, f"a got {len(results['a'])}"
    assert len(results["b"]) == 20, f"b got {len(results['b'])}"
    assert set(results["a"]) == set(range(20)), f"a missing values"

    # Two different keys should have different locks
    lock_a = locker._locks["a"]
    lock_b = locker._locks["b"]
    assert lock_a is not lock_b, "each key should have its own lock"

    print("Per-key locker tests passed")
    print(f"  a: {sorted(results['a'])[:5]}...")
    print(f"  b: {sorted(results['b'])[:5]}...")
