# Lesson 4: Graph Theory & Graph Traversal Algorithms

Graphs model relationships between entities (social networks, road maps, web link structures, and dependency graphs).

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Represent Graphs using Adjacency Lists and Adjacency Matrices.
2. Implement **Breadth-First Search (BFS)** for shortest path discovery.
3. Implement **Depth-First Search (DFS)** for cycle detection and path exploration.
4. Implement **Dijkstra's Algorithm** for weighted shortest path calculation.

---

## 1. Graph Representation (Adjacency List)

```python
from collections import deque

class Graph:
    def __init__(self):
        self.adj_list: dict[str, list[str]] = {}

    def add_edge(self, u: str, v: str, bidirectional: bool = True) -> None:
        self.adj_list.setdefault(u, []).append(v)
        if bidirectional:
            self.adj_list.setdefault(v, []).append(u)

    def bfs_shortest_path(self, start: str, target: str) -> list[str]:
        """Breadth-First Search: finds shortest path in unweighted graph."""
        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == target:
                return path

            for neighbor in self.adj_list.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path) + [neighbor]
                    queue.append(new_path)
        return []

    def dfs(self, start: str, visited: set = None) -> list[str]:
        """Depth-First Search (Recursive)."""
        if visited is None:
            visited = set()
        visited.add(start)
        traversal = [start]
        for neighbor in self.adj_list.get(start, []):
            if neighbor not in visited:
                traversal.extend(self.dfs(neighbor, visited))
        return traversal
```

---

## 📝 Quick Exercise

**Prompt**:
Build a network routing graph between 5 cities and find the shortest path of hops between `"NYC"` and `"LA"`.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
network = Graph()
network.add_edge("NYC", "Chicago")
network.add_edge("Chicago", "Denver")
network.add_edge("Denver", "LA")
network.add_edge("NYC", "Atlanta")
network.add_edge("Atlanta", "Dallas")
network.add_edge("Dallas", "LA")

shortest_hops = network.bfs_shortest_path("NYC", "LA")
print("Shortest route:", " -> ".join(shortest_hops))
# Output: Shortest route: NYC -> Chicago -> Denver -> LA
```
</details>
