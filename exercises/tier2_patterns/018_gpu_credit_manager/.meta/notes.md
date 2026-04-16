# Notes for GPU Credit Manager with Expiry

## Why this matters

The expiry-ordered credit consumption pattern appears in token bucket rate limiters, trial credit systems (cloud free tiers), and the canonical "GPU Credits" problem from multiple major tech interview banks. Greedy consumption of soonest-expiring units is also used in calendar scheduling and airline reward programs.

## Watch out for

- **Lazy vs eager expiry**: sweeping the entire heap to remove expired entries on every operation is O(n). Lazy expiry (discard on pop) keeps operations O(log n) amortized.
- **Atomicity of deduct**: check that sufficient unexpired credits exist *before* making any changes. If `InsufficientCredits` is raised, the heap must be unchanged.
- **Expiry boundary**: the test shows that credits with `expiry_ts=30` are still valid at `now_ts=30` (boundary is exclusive). Credits expire when `expiry_ts <= now_ts` is false — i.e., they're valid while `expiry_ts > now_ts`.

## Interview follow-ups

1. How would you implement a `refund(user, amount)` that returns credits without an expiry?
2. What changes if you need to support partial deductions (deduct as much as possible rather than all-or-nothing)?
3. How would you make `balance()` O(1) instead of O(n log n)?
