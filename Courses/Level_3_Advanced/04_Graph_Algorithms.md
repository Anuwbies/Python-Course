# Lesson 4: Network Architectures: Graphs, BFS, DFS & Dijkstra

Many of the most critical real-world computing systems—including GPS navigation, social networks, dependency resolution graphs, computer network routing, and microservice meshes—are modeled as **Graphs**. In this lesson, you will master graph representations (Adjacency Lists), fundamental traversals (**Breadth-First Search** and **Depth-First Search**), and **Dijkstra's Shortest Path Algorithm**.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Model complex relational networks using Graph terminology (Vertices, Edges, Weights, Directionality).
2. Construct memory-efficient **Adjacency Lists** using Python dictionaries and sets.
3. Implement **Breadth-First Search (BFS)** using a FIFO Queue for shortest-hop pathfinding.
4. Implement **Depth-First Search (DFS)** using recursion/stacks for full topology exploration.
5. Solve weighted shortest-path problems using **Dijkstra's Algorithm** with a Min-Heap.

---

## 1. Graph Representation: Adjacency Lists

An **Adjacency List** maps each node to a list or set of its adjacent connected neighbors:

```python
# Unweighted Directed Graph:
network_graph = {
    "Router-A": ["Router-B", "Router-C"],
    "Router-B": ["Router-D"],
    "Router-C": ["Router-D"],
    "Router-D": ["Gateway-E"],
    "Gateway-E": []
}

# Weighted Graph:
weighted_network = {
    "A": [("B", 4), ("C", 2)],
    "B": [("D", 5)],
    "C": [("B", 1), ("D", 8)],
    "D": []
}
```

---

## 2. Breadth-First Search (BFS) vs. Depth-First Search (DFS)

- **BFS (Breadth-First Search)**: Explores all immediate neighbors at depth $d$ before moving to depth $d+1$. Uses a **FIFO Queue** (`collections.deque`). Guarantees the **shortest unweighted path**.
- **DFS (Depth-First Search)**: Explores as far as possible down each branch before backtracking. Uses a **LIFO Stack** or recursion. Ideal for maze solving, cycle detection, and topological sorting.

```python
from collections import deque

def bfs_shortest_path(graph: dict, start_node: str, target_node: str) -> list[str] | None:
    queue = deque([[start_node]])
    visited = {start_node}

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == target_node:
            return path

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return None
```

---

## 3. Dijkstra's Algorithm (Weighted Shortest Path)

Dijkstra's algorithm finds the minimum-weight path from a starting node to all other nodes in a graph with non-negative edge weights using a Min-Heap ($\mathcal{O}((V + E) \log V)$):

```
1. Initialize distances to all nodes as Infinity (∞); start node distance = 0.
2. Push (0, start_node) to a Min-Heap.
3. While the heap is not empty:
   a. Pop the node with the smallest known distance.
   b. For each neighbor: if (current_dist + edge_weight) < known_dist[neighbor],
      update known_dist[neighbor] and push (new_dist, neighbor) to the heap.
```

---

## 💻 Code Example & Reference

The following real-life program models an **International Airline Flight Network & Cheapest Flight Path Routing Engine**, combining adjacency lists, BFS hop routing, and Dijkstra's weighted cost optimization:

```python
# =====================================================================
# REAL-WORLD SYSTEM: Airline Flight Network & Optimal Route Engine
# =====================================================================

import heapq
from collections import deque

class FlightNetworkGraph:
    """Manages an international route network with weighted flight costs."""

    def __init__(self):
        # Adjacency List: { origin_airport: list[(destination_airport, fare_usd)] }
        self._adj_list: dict[str, list[tuple[str, float]]] = {}

    def add_route(self, origin: str, destination: str, fare_usd: float) -> None:
        if origin not in self._adj_list:
            self._adj_list[origin] = []
        if destination not in self._adj_list:
            self._adj_list[destination] = []
        self._adj_list[origin].append((destination, fare_usd))

    # 1. BFS: Fewest Connecting Flight Hops (Lesson 4 BFS)
    def find_fewest_layovers_route(self, start: str, target: str) -> list[str] | None:
        queue = deque([[start]])
        visited = {start}

        while queue:
            path = queue.popleft()
            curr = path[-1]

            if curr == target:
                return path

            for neighbor, _ in self._adj_list.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None

    # 2. Dijkstra: Cheapest Total Fare Routing (Lesson 4 Dijkstra)
    def find_cheapest_flight_route(self, start: str, target: str) -> tuple[float, list[str]]:
        distances: dict[str, float] = {node: float('inf') for node in self._adj_list}
        previous_nodes: dict[str, str | None] = {node: None for node in self._adj_list}
        distances[start] = 0.0

        # Min-Heap stores tuples of: (cumulative_cost, current_airport)
        pq = [(0.0, start)]

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > distances[current_node]:
                continue # Stale heap entry

            if current_node == target:
                break # Shortest path located

            for neighbor, weight in self._adj_list.get(current_node, []):
                distance_through_curr = current_dist + weight
                if distance_through_curr < distances[neighbor]:
                    distances[neighbor] = distance_through_curr
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance_through_curr, neighbor))

        # Reconstruct path
        path = []
        curr = target
        while curr:
            path.append(curr)
            curr = previous_nodes.get(curr)
        path.reverse()

        return distances[target], path


# 3. Route Network Assembly & Execution
network = FlightNetworkGraph()
network.add_route("SFO", "ORD", 250.00)
network.add_route("SFO", "DEN", 120.00)
network.add_route("DEN", "ORD", 90.00)
network.add_route("DEN", "JFK", 350.00)
network.add_route("ORD", "JFK", 180.00)
network.add_route("SFO", "JFK", 600.00) # Direct but expensive

print("=" * 75)
print(f"{'INTERNATIONAL AIRLINE FLIGHT ROUTING DISPATCH':^75}")
print("=" * 75)

# BFS: Fewest Connections
min_hop_path = network.find_fewest_layovers_route("SFO", "JFK")
print(f"✈️ Direct / Min Layovers Route (BFS): {' -> '.join(min_hop_path)}")

# Dijkstra: Minimum Cost
cheapest_cost, cheapest_path = network.find_cheapest_flight_route("SFO", "JFK")
print(f"💰 Cheapest Economic Route (Dijkstra): {' -> '.join(cheapest_path)}")
print(f"   -> Total Ticket Fare: ${cheapest_cost:,.2f} (Savings vs direct: ${600 - cheapest_cost:,.2f})")
print("=" * 75)
```

### 🔍 Code Explanation:
- **BFS Hop Optimization**: BFS uses `collections.deque` to explore level-by-level, guaranteeing that `"SFO -> JFK"` (1 direct hop) is discovered first.
- **Dijkstra Cost Optimization**: By prioritizing path weights via a Min-Heap, Dijkstra discovers that `"SFO -> DEN -> ORD -> JFK"` ($120 + $90 + $180 = \$390$) is significantly cheaper than the direct flight (\$600).
- **Adjacency Structure**: `_adj_list` handles directed weighted graph relationships with constant-time lookup.

---

## 📝 Quick Exercise: Social Network Degree of Separation & Friend Network BFS

### 🏢 Real-Life Scenario
You are developing the recommendation engine for a professional social networking platform (such as LinkedIn). When user A searches for user B, the system calculates the exact "Degree of Separation" (1st degree connection = immediate friends, 2nd degree = friends-of-friends, 3rd degree = 3 hops away) using Breadth-First Search (BFS).

### 📋 Requirements
1. **Define `find_degrees_of_separation(social_graph: dict, start_user: str, target_user: str) -> tuple[int, list[str]] | None`**:
   - `social_graph` is an unweighted undirected Adjacency List:
     ```python
     network = {
         "Alice": {"Bob", "Charlie"},
         "Bob": {"Alice", "David"},
         "Charlie": {"Alice", "Eve"},
         "David": {"Bob", "Frank"},
         "Eve": {"Charlie", "Frank"},
         "Frank": {"David", "Eve"}
     }
     ```
   - Implement BFS using a `collections.deque` storing `(current_user, current_degree, path_list)`.
   - Maintain a `visited = set()` to prevent infinite loops from network cycles.
   - If `current_user == target_user`: Return `(current_degree, path_list)`.
   - If no connection exists: Return `None`.
2. Execute the search from `"Alice"` to `"Frank"` and output the path and degree of separation.

> [!IMPORTANT]
> **Cumulative Constraint**: Combine Level 3 BFS and Graph algorithms with Level 1 sets, dictionaries, deque, and f-strings.

### 🎯 Expected Output
```text
==================================================
        SOCIAL NETWORK DEGREE OF SEPARATION       
==================================================
Start Connection:   Alice
Target Connection:  Frank
--------------------------------------------------
✅ Connection Found!
Degree of Separation: 3rd Degree Connection
Connection Chain:     Alice -> Bob -> David -> Frank
==================================================
```

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
from collections import deque

# 1. Social Network BFS Graph Search (Level 3)
def find_degrees_of_separation(social_graph: dict, start_user: str, target_user: str) -> tuple[int, list[str]] | None:
    if start_user not in social_graph or target_user not in social_graph:
        return None
    if start_user == target_user:
        return (0, [start_user])

    queue = deque([(start_user, 0, [start_user])])
    visited = {start_user}

    while queue:
        current, degree, path = queue.popleft()

        if current == target_user:
            return degree, path

        for neighbor in social_graph.get(current, set()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, degree + 1, path + [neighbor]))

    return None


# 2. Execution Run
social_network = {
    "Alice": {"Bob", "Charlie"},
    "Bob": {"Alice", "David"},
    "Charlie": {"Alice", "Eve"},
    "David": {"Bob", "Frank"},
    "Eve": {"Charlie", "Frank"},
    "Frank": {"David", "Eve"}
}

result = find_degrees_of_separation(social_network, "Alice", "Frank")

print("==================================================")
print("        SOCIAL NETWORK DEGREE OF SEPARATION       ")
print("==================================================")
print(f"Start Connection:   Alice")
print(f"Target Connection:  Frank")
print("--------------------------------------------------")

if result:
    degree, chain = result
    degree_suffix = "st" if degree == 1 else ("nd" if degree == 2 else "rd" if degree == 3 else "th")
    print(f"✅ Connection Found!")
    print(f"Degree of Separation: {degree}{degree_suffix} Degree Connection")
    print(f"Connection Chain:     {' -> '.join(chain)}")
else:
    print("❌ No connection exists between users.")

print("==================================================")
```

**Explanation of the Solution:**
- BFS explores immediate connections (1st degree) before expanding to friends-of-friends (2nd degree).
- `visited = {start_user}` prevents infinite cyclical looping across bidirectional social links.
</details>
