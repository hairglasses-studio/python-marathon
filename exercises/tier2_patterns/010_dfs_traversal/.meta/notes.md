# Notes for Depth-First Search (Pre-order)

## Why this matters

DFS pre-order is the foundation for topological sort, cycle detection, and serialization of tree/graph structures. In interviews, if you can write this cleanly in under 5 minutes it signals strong graph fluency.

## Watch out for

- **Visiting a node twice**: happens when two paths lead to the same node (e.g., diamond graph). Always check `if node in visited` before recording, not after.
- **Neighbor order matters**: the test asserts `b` comes before `c` because neighbors are visited in adjacency-list order. Don't sort or shuffle.

## Interview follow-ups

1. How would you convert this to an iterative (stack-based) DFS without changing the output order?
2. What changes if the graph has nodes that are not reachable from `start`? Should they appear in the output?
3. How would you detect a cycle using this same DFS skeleton?
