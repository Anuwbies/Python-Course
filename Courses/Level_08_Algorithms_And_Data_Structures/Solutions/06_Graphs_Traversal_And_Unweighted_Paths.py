from collections import deque

def shortest_path(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError("Unknown endpoint")
    queue = deque([start])
    previous = {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            path = [node]
            while node != start:
                node = previous[node]
                path.append(node)
            return list(reversed(path))
        for neighbor in graph[node]:
            if neighbor not in previous:
                previous[neighbor] = node
                queue.append(neighbor)
    return None

graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": [], "E": []}
print(shortest_path(graph, "A", "D"))
print(shortest_path(graph, "A", "E"))
