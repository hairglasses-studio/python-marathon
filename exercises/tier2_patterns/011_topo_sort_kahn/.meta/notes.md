# Notes for Topological Sort (Kahn's Algorithm)

## Why this matters

Kahn's algorithm is the backbone of every build system (Make, Bazel, Gradle) and package manager dependency resolver. Interviewers ask about it directly or embed it in "build order" / "course schedule" problems.

## Watch out for

- **Edge direction confusion**: `graph[x] = x's dependencies` means the edge runs from `x` toward its deps, not the other way. Getting in-degree direction backwards is the most common mistake.
- **Cycle detection is free**: if the result list is shorter than the graph, you have a cycle — no extra work needed.

## Interview follow-ups

1. How does Kahn's compare to the DFS-based topological sort in terms of cycle detection and output order?
2. If two nodes are both ready at the same time, Kahn's can emit them in any order. How would you force lexicographic output?
3. How would you modify this to return all valid topological orderings, not just one?
