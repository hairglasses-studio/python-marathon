# Tool-Call Loop with Retry + Budget (Warm-up 3)

**Tier:** tier3_canonical  
**Target time:** 45 minutes  
**Topics:** retry, backoff, dataclass, exception-hierarchy, 4-gate  
**Source:** `openai-devprod-2026-04-16.ipynb` cells 22-26

## Problem

## Warm-up 3 — Tool-Call Loop with Retry  *(DO THIS TWICE)*

**Why this one twice:** it mirrors the Codex execution loop. This is the single most probable theme for a Developer Productivity coding round because the team's entire product IS a tool-call loop.

Implement an agent's inner loop. `invoke(call, *, budget)` calls out, parses the response, classifies errors (retryable vs terminal), applies exponential backoff with jitter, and tracks a per-session budget that aborts the loop when exhausted.

### The four gates

1. **Gate 1 — happy-path invoke + parse.** Given a `ToolCall`, return a `ToolResult`.
2. **Gate 2 — error classification + backoff.** `RetryableError` → retry with exponential backoff + jitter; `TerminalError` → raise immediately.
3. **Gate 3 — per-error-type policies.** `TimeoutError` → retry with doubled budget; `AuthError` → terminal; `RateLimitError` → retry honoring server-provided `retry_after`.
4. **Gate 4 — budget accounting across a nested call tree.** A tool call that makes sub-tool-calls shares the parent budget.

> **While you do this:** narrate every decision out loud. Why retry. Why not retry. Where the budget lives. What would break under concurrency. Interviewers watch you think as much as they watch your code.

## How to run

```bash
python marathon.py run 026
```

Edit `problem.py`. When `test_problem.py` passes, move on.
