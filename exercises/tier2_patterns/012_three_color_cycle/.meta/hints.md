# Hints for Three-Color Cycle Detection

## Hint 1

This is a DFS-based cycle detection problem using a three-state coloring scheme. Unlike a plain `visited` set, you need to distinguish between "currently on the recursion stack" (GRAY) and "fully finished" (BLACK). A cycle exists if and only if DFS encounters a back-edge — an edge pointing to a GRAY node. You must call DFS from every node to catch cycles in disconnected components.

## Hint 2

Approach:
- Define three states: `WHITE`, `GRAY`, `BLACK` (constants or strings)
- Initialize all nodes as WHITE in a `color` dict
- For each WHITE node in `graph`, call a DFS helper
- Inside `_dfs(node)`:
  - Set `color[node] = GRAY`
  - For each neighbor: if GRAY → return `True` (cycle found); if WHITE → recurse and propagate `True`
  - Set `color[node] = BLACK` before returning `False`
- Return `True` if any DFS call returns `True`, else `False`

## Hint 3

The core DFS helper with color transitions:

```python
def _dfs(node):
    color[node] = GRAY
    for neighbor in graph[node]:
        if color[neighbor] == GRAY:
            return True          # back-edge = cycle
        if color[neighbor] == WHITE:
            if _dfs(neighbor):
                return True
    color[node] = BLACK
    return False
```
