# Notes for Transitive Dependents (Cache Invalidation)

## Why this matters

Cache invalidation by reverse-reachability is used in build systems (which files to recompile when a header changes), React's dependency tree, and any incremental computation engine. Getting this wrong causes stale caches; getting it too aggressive causes full rebuilds.

## Watch out for

- **Graph direction**: the original graph points from consumers to producers. You need to walk in the producer-to-consumer direction, which requires inversion.
- **Don't include the target itself**: the returned set should be nodes that need invalidation, not the source of the change.

## Interview follow-ups

1. How would you extend this to also return nodes in topological order (so they can be rebuilt in the correct sequence)?
2. What if the graph can have cycles (mutual dependencies)? How does that change the algorithm?
3. In a real build system, how would you make this incremental — so you don't rebuild the reverse graph from scratch on every change?
