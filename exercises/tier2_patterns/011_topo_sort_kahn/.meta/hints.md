# Hints for Topological Sort (Kahn's Algorithm)

## Hint 1

This is a BFS-based graph ordering problem. Kahn's algorithm works by repeatedly emitting nodes whose prerequisites are all satisfied. You need to track the in-degree (count of how many other nodes list each node as a dependency) and use a `collections.deque` as a processing queue. When in-degree drops to zero, a node is ready to emit.

## Hint 2

Step-by-step:
- Initialize `in_degree = {node: 0 for node in graph}`
- For each `node` with dependencies, increment `in_degree[node]` for each dep — but think carefully: `graph[node]` lists what `node` depends on; a node becomes "ready" when nothing is still waiting for it. Read the README convention note to get the direction right.
- Seed a `deque` with all nodes where `in_degree[node] == 0`
- While the queue is not empty: pop a node, append to result; for every other node that listed this node as a dependency, decrement their in-degree and enqueue if it hits 0
- If `len(result) < len(graph)`: `raise ValueError("cycle detected")`

## Hint 3

The core queue-processing loop:

```python
queue = deque(n for n in graph if in_degree[n] == 0)
result = []
while queue:
    node = queue.popleft()
    result.append(node)
    for other, deps in graph.items():
        if node in deps:
            in_degree[other] -= 1
            if in_degree[other] == 0:
                queue.append(other)
```
