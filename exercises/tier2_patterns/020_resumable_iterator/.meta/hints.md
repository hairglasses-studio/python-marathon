# Hints for Resumable List Iterator

## Hint 1

This is an iteration-protocol and state-serialization problem. The `ListIterator` wraps a list and tracks a single integer — the current index. `get_state()` serializes that index into a JSON-safe dict; `set_state()` restores it. Because the underlying list doesn't change, the index is all you need to capture the full iterator position.

## Hint 2

- `next()`: check `if self._index >= len(self._items)` and raise `StopIteration`; otherwise return `self._items[self._index]` and increment `self._index`
- `get_state()`: return `{"index": self._index}` — this is already JSON-serializable
- `set_state(state)`: set `self._index = state["index"]`

The JSON round-trip test (`json.loads(json.dumps(state))`) will pass as long as you use only basic types (int, str, list, dict) in the state dict.

## Hint 3

The three methods are just a few lines each:

```python
def next(self):
    if self._index >= len(self._items):
        raise StopIteration
    item = self._items[self._index]
    self._index += 1
    return item

def get_state(self):
    return {"index": self._index}

def set_state(self, state):
    self._index = state["index"]
```
