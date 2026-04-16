# Hints for Depth-First Search (Pre-order)

## Hint 1

This is a classic graph traversal problem — use recursion or an explicit stack. The key insight is that "pre-order" means you record a node the moment you first visit it, before recursing into its neighbors. You need a `visited` set to avoid revisiting nodes that are reachable via multiple paths.

## Hint 2

Here is the recursive approach:
- Initialize `visited = set()` and `result = []`
- Define an inner `_dfs(node)` function that:
  - Returns immediately if `node` is already in `visited`
  - Adds `node` to `visited` and appends it to `result` (pre-order: record first)
  - Iterates over `graph[node]` in order and recurses into each neighbor
- Call `_dfs(start)` and return `result`

## Hint 3

The visited-check-before-recurse pattern that prevents duplicate visits:

```python
def _dfs(node):
    if node in visited:
        return
    visited.add(node)
    result.append(node)
    for neighbor in graph[node]:
        _dfs(neighbor)
```
