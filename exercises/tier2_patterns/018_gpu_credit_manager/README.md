# GPU Credit Manager with Expiry

**Tier:** tier2_patterns  
**Target time:** 25 minutes  
**Topics:** heapq, expiry, lazy-eviction  
**Source:** `openai-primitives-refresher.ipynb` cells 71-74

## Problem

## 10.2 Exercise — GPU credit manager with expiry

**Task:** Implement `CreditManager` with:
- `add(user, amount, expiry_ts)` — user gets `amount` credits that expire at `expiry_ts`
- `deduct(user, amount, now_ts)` — subtract `amount` credits from user, consuming soonest-to-expire first. If any consumed chunk is already expired (`expiry_ts ≤ now_ts`), skip it. If the user doesn't have enough unexpired credits, raise `InsufficientCredits`.
- `balance(user, now_ts)` — total unexpired credits for user

**Requirements:**
- Use a per-user `heapq` (min-heap on expiry)
- Lazy expiry: don't sweep the heap on every op; only discard expired entries when encountered during a pop

**Why this matters:** this is an exact match for the canonical GPU Credits problem from the OpenAI coding bank. Gate 1–2 of that problem is exactly what this exercise asks for.

## How to run

```bash
python marathon.py run 018
```

Edit `problem.py`. When `test_problem.py` passes, move on.
