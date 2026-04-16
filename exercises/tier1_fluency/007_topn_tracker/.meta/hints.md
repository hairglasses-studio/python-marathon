# Hints for Top-N Tracker

## Hint 1

This is a heap problem. To track the N largest values seen so far with O(log N) insertions, use a min-heap of fixed size N. The key insight: the minimum of your heap is the current "cutoff" — any new value larger than that minimum displaces it. Python's `heapq` module implements a min-heap directly on a list.

## Hint 2

Approach outline for `TopN`:
- `__init__`: store `self.n` and initialize `self._heap = []`
- `add(value)`: two cases:
  - If `len(self._heap) < self.n`: use `heapq.heappush(self._heap, value)` to grow the heap freely
  - Else if `value > self._heap[0]` (the current minimum): use `heapq.heapreplace(self._heap, value)` to atomically pop the min and push the new value
- `top()`: return `sorted(self._heap, reverse=True)` — the heap itself is not sorted

## Hint 3

```python
import heapq

def add(self, value):
    if len(self._heap) < self.n:
        heapq.heappush(self._heap, value)
    elif value > self._heap[0]:
        heapq.heapreplace(self._heap, value)

def top(self):
    return sorted(self._heap, reverse=True)
```
