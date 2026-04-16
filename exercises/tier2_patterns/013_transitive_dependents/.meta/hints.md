# Hints for Transitive Dependents (Cache Invalidation)

## Hint 1

This is a graph reachability problem on an inverted graph. The original graph maps each node to its dependencies; you need to walk in the reverse direction — from the changed node outward to everything that depends on it. Build a reverse adjacency map first using `collections.defaultdict(list)`, then do a BFS or DFS from `target` on that reversed graph.

## Hint 2

Step-by-step approach:
- Build the inverted graph: for each `node` and each `dep` in `graph[node]`, add `node` to `reverse[dep]` (dep is needed by node, so node is a dependent of dep)
- BFS from `target` using `collections.deque`: start with `deque([target])` and a `visited` set initialized to `{target}`
- Pop a node, look up its dependents in `reverse`, and enqueue any not yet visited
- Return `visited - {target}` (the problem says do not include `target` itself)

## Hint 3

The inversion loop that most learners write backwards:

```python
reverse = defaultdict(list)
for node, deps in graph.items():
    for dep in deps:
        reverse[dep].append(node)  # node depends on dep → node is a dependent of dep
```
