# 🟠 Level 3: Advanced Capstone Projects

Welcome to the **Level 3 Advanced Testing Capstones**! These projects test advanced data structures, algorithmic complexity, graph traversal, concurrency models (GIL, threading, multiprocessing), and non-blocking asynchronous programming with `asyncio`.

---

## 📚 Available Projects

| Project | Domain | Key Concepts Tested | Difficulty | Specification |
| :--- | :--- | :--- | :---: | :--- |
| **01: Multi-Process Priority Job Queue** | Systems / Distributed Computing | `multiprocessing.Process`, `Queue`, Custom Min-Heap Priority Queue, Graceful Signal Shutdown | 🟠 Hard | [Project 01 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_3_Advanced/Project_01_Distributed_Job_Queue_With_Worker_Pools.md) |
| **02: Urban Transit Graph Routing Engine** | Algorithms / Spatial Networks | Custom Adjacency List Graph, Min-Heap, Dijkstra, A* Pathfinding, Multi-threaded Traffic Simulator | 🟠 Hard | [Project 02 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_3_Advanced/Project_02_Custom_Graph_Network_Routing_Engine.md) |
| **03: Async Real-Time Market Ticker Stream** | FinTech / Reactive Systems | `asyncio.TaskGroup`, Non-blocking WebSockets/Streams, Ring Buffers, Producer-Consumer Queues | 🟠 Hard | [Project 03 Spec](file:///C:/Users/asiro/Desktop/Capstone/Python/Capstones/Level_3_Advanced/Project_03_Async_RealTime_Stock_Ticker_Aggregator.md) |

---

## 🎯 Learning Evaluation Rubric
When implementing any Level 3 project, ensure your solution satisfies:
- **Algorithmic Efficiency**: Adherence to optimal Big-O bounds ($O(V + E \log V)$, $O(\log N)$ heap operations, etc.).
- **Deadlock & Race Condition Prevention**: Correct synchronization using `threading.Lock`, `multiprocessing.Event`, or non-blocking async primitives.
- **Process & Resource Lifecycle**: Guaranteed cleanup of child processes, thread pools, and event loops upon termination or interrupt signals (`SIGINT`/`SIGTERM`).
- **Scalability**: Capable of processing high-throughput workloads without stalling the main execution thread.
