# Hints for Windowed Generator

## Hint 1

This is a sliding-window problem over an arbitrary iterable. The key insight is that you need to maintain a fixed-size buffer as you consume the iterable element by element. Python's `collections.deque` with a `maxlen` parameter is the natural fit — it automatically evicts the oldest element when you append past capacity.

## Hint 2

Approach outline:
- Import `deque` from `collections`
- Initialize a `deque(maxlen=size)`
- Iterate over `seq` with a plain `for` loop, appending each element
- Once the deque reaches `size` elements (`len(d) == size`), `yield tuple(d)`
- Handle the edge case where `size` is larger than the sequence automatically — the deque never fills, so nothing is yielded

## Hint 3

```python
from collections import deque

def windows(seq, size):
    buf = deque(maxlen=size)
    for item in seq:
        buf.append(item)
        if len(buf) == size:
            yield tuple(buf)
```
