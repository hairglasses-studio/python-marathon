# Notes for Dependency Graph with Incremental Invalidation (Warm-up 1)

## Why this matters

Incremental build systems (Bazel, Gradle, Make) and reactive data pipelines are built on exactly this abstraction: a DAG of tasks with content-addressed caching and invalidation. In developer tooling interviews this pattern signals that you understand why rebuilding from scratch is wasteful and how to scope cache invalidation correctly.

## Watch out for

- Invalidation must be transitive: clearing only the directly-invalidated node leaves stale cached outputs in nodes that depend on it. Collect all transitive dependents via BFS/DFS over a reverse-dependency index.
- Gate 3 concurrency: building a node requires its inputs to be complete first, so you cannot blindly parallelize everything. The safe pattern is to acquire a per-node lock before checking or populating the cache, ensuring each node is built at most once even if two threads race to build it.

## Interview follow-ups

- "How would you handle a build function that has side effects (e.g., writes a file)?" — separate the pure value cache from the artifact store; track artifact hashes separately so you can skip re-running even if the in-memory cache is cold.
- "What's the time complexity of `invalidate` if the graph has N nodes and E edges?" — O(N + E) in the worst case (BFS/DFS over all dependents).
- "How would you scale this to a distributed build cluster?" — replace the in-process dict cache with a content-addressed object store (e.g., S3 + DynamoDB); use a distributed work queue (e.g., Celery, Ray) for parallel task execution.
