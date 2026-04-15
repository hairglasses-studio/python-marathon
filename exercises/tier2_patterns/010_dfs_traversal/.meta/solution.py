from collections import defaultdict

def dfs(graph: dict[str, list[str]], start: str) -> list[str]:
    """DFS pre-order traversal with a visited set."""
    visited: set[str] = set()
    result: list[str] = []

    def _visit(node: str) -> None:
        if node in visited:
            return
        visited.add(node)
        result.append(node)  # pre-order: record on entry
        for neighbor in graph.get(node, []):
            _visit(neighbor)

    _visit(start)
    return result


# Iterative version (avoids recursion limit on deep graphs):
def dfs_iterative(graph: dict[str, list[str]], start: str) -> list[str]:
    visited: set[str] = set()
    result: list[str] = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        result.append(node)
        # Push in reverse so neighbors are popped in original order
        for neighbor in reversed(graph.get(node, [])):
            stack.append(neighbor)
    return result
