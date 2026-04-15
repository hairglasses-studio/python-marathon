WHITE, GRAY, BLACK = 0, 1, 2


def has_cycle(graph: dict[str, list[str]]) -> bool:
    # Collect all nodes (keys + nodes only appearing as deps)
    nodes: set[str] = set(graph.keys())
    for deps in graph.values():
        nodes.update(deps)
    color: dict[str, int] = {n: WHITE for n in nodes}

    def visit(node: str) -> bool:
        """Return True if a cycle is found starting from `node`."""
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color.get(neighbor, WHITE) == GRAY:
                return True  # back-edge → cycle
            if color.get(neighbor, WHITE) == WHITE:
                if visit(neighbor):
                    return True
        color[node] = BLACK
        return False

    # Must check every component, not just the first node
    for node in nodes:
        if color[node] == WHITE:
            if visit(node):
                return True
    return False
