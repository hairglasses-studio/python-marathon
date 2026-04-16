# Notes for Top-N Tracker

## Why this matters

The fixed-size min-heap is the canonical O(N log N) solution for streaming top-K problems — it appears in log aggregation, recommendation systems, leaderboards, and anywhere you need to find the largest N items in a stream too large to sort fully. It is a standard interview question at every level.

## Watch out for

- Calling `sorted(self._heap)` without `reverse=True` returns ascending order; the tests expect descending
- Using `heapq.nlargest(self.n, self._heap)` in `top()` is fine for correctness but is O(N log N) on every call; returning `sorted(self._heap, reverse=True)` is equivalent since the heap is already bounded to N elements

## Interview follow-ups

- "What is the time complexity of `add` and `top` in your implementation? How does it compare to sorting the full stream?"
- "How would you modify this to also track the N smallest values at the same time?"
- "Python's `heapq` is a min-heap. How would you implement a max-heap without importing a third-party library?"
