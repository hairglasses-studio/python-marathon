# Notes

Key building block for any async I/O fanout. `asyncio.Semaphore` is the right primitive — don't try to hand-roll throttling with `asyncio.sleep`.

Common interview follow-ups:
- "Now add a per-host rate limit." → dict of semaphores keyed by host.
- "Handle partial failures without aborting the whole batch." → `asyncio.gather(..., return_exceptions=True)`.
- "Retry failed fetches." → wrap `bounded(url)` with a retry helper (see exercise 028).
