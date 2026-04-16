# Hints for Word Frequency Counter

## Hint 1

This is a counting problem that maps naturally to a dictionary. Python's `collections` module has a class purpose-built for counting things from an iterable — it eliminates the need to manually check whether a key exists before incrementing.

## Hint 2

Approach outline for `word_freq`:
- Lowercase the text with `.lower()`, then split on whitespace with `.split()`
- `.split()` (no argument) already discards empty strings from multiple spaces
- Use `collections.Counter(words)` to build the frequency dict in one call
- For `top_words`: sort the `Counter.items()` by count descending, then word ascending — use a tuple sort key `(-count, word)`

## Hint 3

```python
from collections import Counter

def word_freq(text):
    words = text.lower().split()
    return dict(Counter(words))

def top_words(text, n):
    counts = Counter(text.lower().split())
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
```
