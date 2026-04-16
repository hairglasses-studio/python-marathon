# Notes for Three-Color Cycle Detection

## Why this matters

Three-color DFS is the standard algorithm for detecting cycles in directed graphs. It appears in dependency resolvers, deadlock detection, and compiler analysis. The "course schedule" and "prerequisite" Leetcode problems are direct applications.

## Watch out for

- **Two-color (visited set) is wrong**: a plain `visited` set cannot distinguish a back-edge from a cross-edge. You'll get false positives on DAGs with shared nodes (like a diamond).
- **Must visit all nodes**: if the graph has multiple disconnected components, starting DFS from only one node will miss cycles in other components.

## Interview follow-ups

1. Why does marking a node BLACK (instead of just removing it from GRAY) matter for performance?
2. How would you modify this to return the actual cycle path, not just a boolean?
3. What is the time and space complexity of this algorithm?
