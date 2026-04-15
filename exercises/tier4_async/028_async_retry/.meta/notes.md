# Notes

This is the async twin of Warm-up 3 (cells 22-26 in `openai-devprod-2026-04-16.ipynb`). Once you've solved this, gate 4 of that warm-up is trivial.

Watch out for:
- Forgetting `await asyncio.sleep(...)` — a bare `sleep` would block the event loop.
- Jitter: `random.uniform(0, jitter)` is additive, not multiplicative. Additive jitter is simpler to reason about and still breaks thundering-herd.
- Re-raising TerminalError without wrapping — don't lose the original traceback.
