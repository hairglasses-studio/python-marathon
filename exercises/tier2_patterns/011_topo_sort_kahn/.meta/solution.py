from collections import defaultdict, deque


def topo_sort(graph: dict[str, list[str]]) -> list[str]:
    # Collect every node (keys + any node that only appears as a dep)
    all_nodes: set[str] = set(graph.keys())
    for deps in graph.values():
        all_nodes.update(deps)

    # in_degree[n] = number of nodes that list n as a dep
    # (i.e. how many things depend on n, inverted from the usual def)
    # We want to emit nodes whose own deps are all already emitted, so we
    # track "unresolved deps remaining" instead.
    unresolved_deps: dict[str, int] = {n: len(graph.get(n, [])) for n in all_nodes}

    # reverse_map[dep] = list of nodes that depend on `dep`
    reverse_map: dict[str, list[str]] = defaultdict(list)
    for node, deps in graph.items():
        for dep in deps:
            reverse_map[dep].append(node)

    # Start with every node that has zero unresolved deps
    queue = deque(n for n, count in unresolved_deps.items() if count == 0)
    result: list[str] = []

    while queue:
        node = queue.popleft()
        result.append(node)
        # Every node that depended on `node` now has one fewer unresolved dep
        for dependent in reverse_map[node]:
            unresolved_deps[dependent] -= 1
            if unresolved_deps[dependent] == 0:
                queue.append(dependent)

    if len(result) != len(all_nodes):
        raise ValueError("cycle detected")
    return result
