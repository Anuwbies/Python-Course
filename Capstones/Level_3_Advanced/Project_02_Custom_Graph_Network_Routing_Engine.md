# Capstone Project 3.2: Urban Transit Graph Routing Engine

## 📌 Project Overview
Build a high-performance **Urban Transit & Network Packet Routing Engine**. The application represents city transportation maps (or internet network topographies) as weighted directed graphs, implements pathfinding algorithms (Dijkstra's Algorithm and A* Search with Euclidean/Manhattan heuristics), and features a concurrent multi-threaded traffic congestion simulator that dynamically updates edge weights in real-time.

---

## 🎯 Learning Objectives
- **Graph Data Structures**: Building weighted directed graphs using custom Node and Edge adjacency structures from scratch.
- **Shortest Path Algorithms**: Implementing Dijkstra's Algorithm ($O((V + E) \log V)$) using a custom Min-Heap Priority Queue.
- **Heuristic Pathfinding (A* Search)**: Implementing $A^*$ with admissible heuristic distance functions ($f(n) = g(n) + h(n)$).
- **Multithreading & Synchronization**: Running a background traffic simulator thread that dynamically mutates edge weights while routing queries execute concurrently, guarded by fine-grained `threading.RLock`.
- **Topological Sorting & Cycle Detection**: Detecting network routing loops using Depth-First Search (DFS) coloring (White/Gray/Black).

---

## 🏗️ System Architecture

```text
               +----------------------------------+
               |       Transit Routing Engine     |
               +----------------------------------+
                                 |
         +-----------------------+-----------------------+
         |                       |                       |
+-----------------+     +-----------------+     +-----------------+
|   Graph Model   |     | Path Solvers    |     | Traffic Worker  |
+-----------------+     +-----------------+     +-----------------+
| - nodes: dict   |     | + dijkstra()    |     | (Background)    |
| - edges: list   |     | + a_star()      |     | - mutates edge  |
| + add_node()    |     | + find_all_paths|     |   weights based |
| + add_edge()    |     +-----------------+     |   on congestion |
+-----------------+                             +-----------------+
```

---

## 📋 Functional Requirements

### 1. Custom Graph Data Structure
- `Node`: ID (str), Name (str), Coordinates `(x: float, y: float)`, Transit Type (e.g. Subway, Bus, Road).
- `Edge`: Source (`Node`), Destination (`Node`), Base Distance (km), Speed Limit (km/h), Current Congestion Factor ($1.0 = \text{clear}$, $3.0 = \text{gridlock}$).
- Effective Weight (Traversal Time):
  $$\text{Traversal Time (minutes)} = \left(\frac{\text{Base Distance}}{\text{Speed Limit}} \times \text{Congestion Factor}\right) \times 60$$

### 2. Pathfinding Engine
- **Dijkstra's Shortest Path**: Computes the absolute shortest travel-time path between any starting node and destination node.
- **A\* Pathfinding Algorithm**: Accelerated heuristic search utilizing Euclidean distance between node coordinates divided by maximum possible transit speed.
- **All-Pairs Shortest Path / Multi-Stop Route Optimizer**: Given a list of 5 delivery waypoints, computes an optimal traversal order (Traveling Salesperson heuristic).

### 3. Background Traffic Congestion Simulator
A background thread periodically increases congestion factors on randomized edges (e.g., simulating road construction, accidents, or peak-hour bottlenecks) and restores them when cleared, demonstrating thread-safe concurrent reads and writes on graph nodes.

### 4. Graph Cycle & Reachability Analysis
- Detect disconnected network partitions using Breadth-First Search (BFS).
- Identify directed routing cycles using DFS recursion with cycle stack tracking.

---

## 📐 Phased Implementation Guide

### Phase 1: Node, Edge, and Adjacency List Graph
```python
from dataclasses import dataclass, field
import math
import threading

@dataclass
class Node:
    node_id: str
    name: str
    x: float
    y: float

@dataclass
class Edge:
    source: str
    target: str
    distance_km: float
    speed_limit_kmh: float
    congestion: float = 1.0  # Multiplier >= 1.0

    @property
    def travel_time_minutes(self) -> float:
        speed = self.speed_limit_kmh / self.congestion
        return (self.distance_km / max(1.0, speed)) * 60.0

class TransitGraph:
    def __init__(self):
        self.nodes = {}
        self.adjacency = {}  # Dict[str, List[Edge]]
        self._lock = threading.RLock()
```

### Phase 2: A* Search Implementation
```python
import heapq

def a_star_shortest_path(graph: TransitGraph, start_id: str, goal_id: str) -> tuple[list[str], float]:
    def heuristic(n1_id: str, n2_id: str) -> float:
        n1, n2 = graph.nodes[n1_id], graph.nodes[n2_id]
        euclidean_dist = math.hypot(n1.x - n2.x, n1.y - n2.y)
        # Minimum possible travel time assuming max speed 100 km/h
        return (euclidean_dist / 100.0) * 60.0

    with graph._lock:
        queue = [(0.0, start_id, [start_id])]
        costs = {start_id: 0.0}

        while queue:
            est_cost, current, path = heapq.heappop(queue)

            if current == goal_id:
                return path, costs[current]

            for edge in graph.adjacency.get(current, []):
                new_cost = costs[current] + edge.travel_time_minutes
                if edge.target not in costs or new_cost < costs[edge.target]:
                    costs[edge.target] = new_cost
                    priority = new_cost + heuristic(edge.target, goal_id)
                    heapq.heappush(queue, (priority, edge.target, path + [edge.target]))

        return [], float("inf")
```

### Phase 3: Traffic Simulator & Live Rerouting
Build the background traffic worker and provide an interactive terminal navigator that recalculates paths when traffic incidents occur.

---

## 🧪 Verification Matrix & Edge Cases

| Scenario | Input / Action | Expected Behavior |
| :--- | :--- | :--- |
| **Unreachable Target** | Query path between two disconnected island nodes | Returns empty path `[]` and `cost = infinity` gracefully |
| **Identical Start & End** | Query path where `start == destination` | Returns `[start]` with `cost = 0.0` |
| **Dynamic Congestion Update**| Road congestion surges on Highway 1 during path traversal | Next query automatically reroutes through alternate secondary avenue |
| **Admissibility Check** | Verify heuristic $h(n)$ never overestimates true distance | A* path cost exactly matches Dijkstra optimal cost on all test subgraphs |

---

## 🚀 Bonus Challenges
- **Interactive ASCII Map Visualizer**: Render the transit nodes and calculated optimal path in terminal as an ASCII coordinate grid.
- **K-Shortest Paths (Yen's Algorithm)**: Implement Yen's algorithm to provide 3 alternative fallback routes.
