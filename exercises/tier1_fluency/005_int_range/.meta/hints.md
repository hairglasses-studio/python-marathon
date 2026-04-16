# Hints for IntRange Class

## Hint 1

This exercise is about Python's data model — implementing the dunder (double-underscore) methods that make your class behave like a built-in type. Think about what each operation needs: `len` needs a numeric formula, iteration needs to yield integers in order, membership testing should not iterate (it should be O(1) arithmetic), and hashability requires consistency with equality.

## Hint 2

Approach outline:
- `__init__`: store `self.start` and `self.stop` as instance attributes
- `__len__`: return `max(0, self.stop - self.start)` to handle empty ranges where stop <= start
- `__iter__`: use `yield from range(self.start, self.stop)` — delegate to Python's built-in range
- `__contains__`: return `self.start <= item < self.stop` — pure arithmetic, O(1)
- `__repr__`: return `f"IntRange({self.start}, {self.stop})"`
- `__eq__`: compare `(self.start, self.stop)` tuples; also check `isinstance(other, IntRange)`
- `__hash__`: return `hash((self.start, self.stop))` — hash the same tuple used for equality

## Hint 3

```python
def __contains__(self, item) -> bool:
    return self.start <= item < self.stop

def __hash__(self) -> int:
    return hash((self.start, self.stop))

def __eq__(self, other) -> bool:
    if not isinstance(other, IntRange):
        return NotImplemented
    return self.start == other.start and self.stop == other.stop
```
