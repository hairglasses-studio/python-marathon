# Notes for Word Frequency Counter

## Why this matters

Word frequency counting is the basis of log analysis, search relevance scoring, and NLP preprocessing. The tie-breaking sort (descending count, ascending alpha) is a pattern that appears in leaderboards, analytics dashboards, and any ranked output that must be deterministic.

## Watch out for

- Forgetting to lowercase before splitting causes "The" and "the" to be counted separately
- Using a plain `dict` with manual `dict[word] = dict.get(word, 0) + 1` works but is slower and more verbose than `Counter`; either is acceptable, but know both

## Interview follow-ups

- "How would you make this stream-friendly so it works on a file too large to fit in memory?"
- "What's the time and space complexity of your solution?"
- "How would you handle punctuation — e.g., 'cat.' and 'cat' should be the same word?"
