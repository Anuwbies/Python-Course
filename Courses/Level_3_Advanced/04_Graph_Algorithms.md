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

---

## 4. Directed Acyclic Graphs (DAGs) & Topological Sorting (Kahn's Algorithm)

In build systems (e.g. `make`, Docker multi-stage builds) and package managers (`pip`, `npm`), tasks must execute strictly after their prerequisites. **Topological Sort** provides a linear task ordering:

```
[ Compile C Code ] ──► [ Link Object Files ] ──► [ Generate Binary ]
```

```python
from collections import deque

def topological_sort(dag_graph: dict[str, list[str]]) -> list[str]:
    """Kahn's Algorithm using in-degree calculation."""
    in_degrees = {node: 0 for node in dag_graph}
    for node, neighbors in dag_graph.items():
        for neighbor in neighbors:
            in_degrees[neighbor] = in_degrees.get(neighbor, 0) + 1

    # Seed queue with nodes having 0 prerequisites (in-degree == 0):
    queue = deque([node for node, deg in in_degrees.items() if deg == 0])
    ordered_tasks = []

    while queue:
        task = queue.popleft()
        ordered_tasks.append(task)
        for neighbor in dag_graph.get(task, []):
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                queue.append(neighbor)

    if len(ordered_tasks) != len(dag_graph):
        raise ValueError("Cyclic dependency detected! Cannot topologically sort graph.")
    return ordered_tasks
```

---

## 5. Cycle Detection in Directed Graphs (3-Color DFS)

A directed graph contains a cycle if and only if a DFS encounters a node currently in the active recursion call stack:
- **`WHITE` (0)**: Unvisited node.
- **`GRAY` (1)**: Currently being explored in the active DFS recursion branch.
- **`BLACK` (2)**: Fully processed node.

If a DFS edge leads to a `GRAY` node, a **cycle (deadlock)** is confirmed.

---

## 6. A* Search Algorithm vs Dijkstra

While Dijkstra expands uniformly in all directions ($f(n) = g(n)$ where $g(n)$ is the cost from start), **A* Search** adds an admissible heuristic $h(n)$ (e.g., Euclidean or Manhattan distance to goal):
$$f(n) = g(n) + h(n)$$
A* focuses exploration directly toward the target, reducing explored nodes by up to $90\%$ in robotics and video game pathfinding.

---

## 📝 10-Tier Progressive Mastery Challenges

Work through these 10 challenges to master graph representations, BFS/DFS, shortest paths, DAGs, and topological sorting:

---

### 🟢 Tier 1: Adjacency Lists & Basic Traversal (Exercises 1–3)

#### 🔹 Exercise 1: Adjacency List Edge Counter
* **Goal**: Write `count_total_edges(adj_list: dict) -> int` for both directed and undirected graphs.

#### 🔹 Exercise 2: Breadth-First Search (BFS) Reachability
* **Goal**: Write `can_reach(graph, start, target) -> bool` using a FIFO queue.

#### 🔹 Exercise 3: Depth-First Search (DFS) Component Size
* **Goal**: Count the total number of connected nodes reachable from a given start node using recursive DFS.

---

### 🟡 Tier 2: Pathfinding & Cycle Detection (Exercises 4–6)

#### 🔹 Exercise 4: Shortest Path Hop Counter (BFS)
* **Goal**: Find the exact number of hops between two servers in an unweighted cluster network.

#### 🔹 Exercise 5: Cycle Detection in Undirected Graph
* **Goal**: Implement cycle detection in an undirected graph using parent pointer tracking in BFS/DFS.

#### 🔹 Exercise 6: Number of Islands (2D Grid Graph DFS)
* **Goal**: Count connected components of `'1'`s (land) surrounded by `'0'`s (water) in a 2D binary matrix.

---

### 🟠 Tier 3: Weighted Graphs & Topological Sorts (Exercises 7–9)

#### 🔹 Exercise 7: Dijkstra's Single-Source Shortest Path
* **Goal**: Implement Dijkstra with a Min-Heap returning the shortest path array from a source router.

#### 🔹 Exercise 8: Course Schedule / Dependency Ordering (Topological Sort)
* **Goal**: Given $N$ courses and prerequisite pairs $[A, B]$, return a valid course completion order using Kahn's algorithm.

#### 🔹 Exercise 9: Word Ladder Transformation Length (BFS)
* **Goal**: Find the shortest transformation sequence from `beginWord` to `endWord` changing one letter at a time against a dictionary.

---

### 🟣 Tier 4: Enterprise Simulation (Exercise 10)

#### 🔹 Exercise 10: Social Network Degree of Separation Engine
* **Goal**: Build a LinkedIn-style degree-of-separation engine determining 1st, 2nd, and 3rd degree connection paths between users.

---

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
<summary><b>🔍 View Exercise Solutions (Separation Degree & 10 Challenges)</b></summary>

```python
# =====================================================================
# SOLUTION: Social Network Degree of Separation
# =====================================================================
from collections import deque

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

# =====================================================================
# SOLUTIONS: 10-Tier Progressive Challenges
# =====================================================================
# Ex 1: Count Total Edges
def count_edges(adj_list: dict, directed=False) -> int:
    cnt = sum(len(neighbors) for neighbors in adj_list.values())
    return cnt if directed else cnt // 2

# Ex 2: BFS Reachability
def can_reach(graph: dict, start: str, target: str) -> bool:
    q = deque([start])
    visited = {start}
    while q:
        curr = q.popleft()
        if curr == target: return True
        for n in graph.get(curr, []):
            if n not in visited:
                visited.add(n)
                q.append(n)
    return False

# Ex 3: DFS Connected Component Size
def component_size(graph: dict, start: str) -> int:
    visited = set()
    def dfs(node):
        visited.add(node)
        for n in graph.get(node, []):
            if n not in visited: dfs(n)
    dfs(start)
    return len(visited)

# Ex 4: Shortest Path Hop Counter
def min_hops(graph: dict, src: str, dst: str) -> int:
    q = deque([(src, 0)])
    visited = {src}
    while q:
        curr, hops = q.popleft()
        if curr == dst: return hops
        for n in graph.get(curr, []):
            if n not in visited:
                visited.add(n)
                q.append((n, hops + 1))
    return -1

# Ex 5: Cycle Detection in Undirected Graph
def has_cycle_undirected(graph: dict) -> bool:
    visited = set()
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, node): return True
            elif neighbor != parent:
                return True
        return False
    for node in graph:
        if node not in visited:
            if dfs(node, None): return True
    return False

# Ex 6: Number of Islands (2D Grid DFS)
def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1': return
        grid[r][c] = '0' # Mark visited
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]: dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    return count

# Ex 7: Dijkstra's Algorithm
import heapq
def dijkstra(graph: dict, start: str) -> dict:
    distances = {n: float('inf') for n in graph}
    distances[start] = 0.0
    pq = [(0.0, start)]
    while pq:
        d, curr = heapq.heappop(pq)
        if d > distances[curr]: continue
        for neighbor, weight in graph.get(curr, []):
            new_d = d + weight
            if new_d < distances[neighbor]:
                distances[neighbor] = new_d
                heapq.heappush(pq, (new_d, neighbor))
    return distances

# Ex 8: Course Schedule Topological Sort
def can_finish_courses(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    adj = {i: [] for i in range(num_courses)}
    in_deg = [0] * num_courses
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_deg[course] += 1
    q = deque([i for i in range(num_courses) if in_deg[i] == 0])
    order = []
    while q:
        curr = q.popleft()
        order.append(curr)
        for neighbor in adj[curr]:
            in_deg[neighbor] -= 1
            if in_deg[neighbor] == 0: q.append(neighbor)
    return order if len(order) == num_courses else []
```
</details>
