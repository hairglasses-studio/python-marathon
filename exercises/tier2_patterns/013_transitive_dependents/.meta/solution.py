from collections import defaultdict, deque


def transitive_dependents(graph: dict[str, list[str]], target: str) -> set[str]:
    # Step 1: invert the graph.
    # dependents[dep] = [nodes that list dep as a direct dependency]
    dependents: dict[str, list[str]] = defaultdict(list)
    for node, deps in graph.items():
        for dep in deps:
            dependents[dep].append(node)

    # Step 2: BFS from target in the inverted graph.
    result: set[str] = set()
    queue = deque(dependents.get(target, []))
    while queue:
        node = queue.popleft()
        if node in result:
            continue
        result.add(node)
        queue.extend(dependents.get(node, []))

    return result
