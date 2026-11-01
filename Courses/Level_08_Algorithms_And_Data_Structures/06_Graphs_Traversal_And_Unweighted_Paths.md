# Lesson 6: Graphs, Traversal & Unweighted Paths

**Prerequisites:** Levels 1–7 and Lessons 1–5 of this level. **Practice file:** `Practice/06_Graphs_Traversal_And_Unweighted_Paths.py`.

Represent connections explicitly, distinguish visited nodes from pending work, and choose traversal order according to the question being asked.

## 1. Describe directed edges

An adjacency dictionary maps each node to its outgoing neighbors. A directed edge from A to B does not automatically imply an edge from B to A. Decide whether every mentioned node must also have its own key, including nodes with no outgoing edges.

```python
graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
print(graph["A"])
```

Duplicate edges and cycles are possible in general input. A traversal must mark visited state or it can repeat work indefinitely. The neighbor order can affect which equally short path is returned, so state whether list order or a separate sorting rule resolves ties.

## 2. Breadth-first search explores layers

A FIFO queue visits nodes at increasing edge distance from the start. Mark a node when it is enqueued so several parents do not repeatedly add it before its first visit. Record a predecessor when discovering it to reconstruct a path later.

For unweighted graphs, this layer order yields a path with the fewest edges. It does not minimize an arbitrary weighted cost. Treating every edge as one unit is a meaningful assumption, not a free property of all graphs.

## 3. Depth-first search explores a branch

A stack or recursive calls follow a branch before returning to alternatives. DFS is useful for reachability, structural exploration, and cycle analysis with additional state. A single visited set establishes reachability, but directed cycle detection needs to distinguish active-path nodes from finished nodes.

Both BFS and DFS can visit each node and edge a bounded number of times with adjacency lists and appropriate visited structures. Storing whole copied paths for every queue entry can add memory beyond the usual predecessor representation.

## 4. Define absence and invalid endpoints

An unreachable destination is different from a node name absent from the graph. This lesson's interface raises ValueError for an unknown endpoint and returns None for a known but disconnected destination. Start equal to goal returns the one-node path.

When reconstructing, start with the goal and follow predecessors until the current node equals the source, then reverse the collected sequence. Stop by comparing with the source rather than assuming a special value cannot be a node ID. Do not modify the caller's graph to store visited state; repeated searches should see the same relationships.

## Reverse a reconstructed path

`reversed(path)` returns an iterator visiting a sequence from last to first. `list(reversed(path))` materializes that reversed order without mutating path. Alternatively, `path.reverse()` reverses a list in place and returns None. Predecessor reconstruction first builds goal-to-source order, so choose one of these operations explicitly before returning the path.

References: [Deque for BFS](https://docs.python.org/3.13/library/collections.html#collections.deque).

## Cost model

With adjacency lists and expected constant-time visited lookups, BFS/DFS visit a reachable component in O(V + E) time. The predecessor/visited state and BFS queue use O(V) auxiliary space. Copying complete paths into every queue entry would change the space analysis; the supplied algorithm reconstructs one path only after discovery.

## Practice: predict, explain, modify, debug

1. **Predict:** Predict the BFS layers from A in the example.
2. **Explain:** Explain why marking on enqueue avoids repeated pending work.
3. **Modify:** Add a disconnected node and distinguish it from an unknown node.
4. **Debug:** Repair a traversal that follows a cycle without a visited structure.

<details>
<summary>Hints</summary>

A predecessor dictionary can also identify nodes already discovered.

</details>

## Independent task: graphs, traversal & unweighted paths

In `Practice/06_Graphs_Traversal_And_Unweighted_Paths.py`, complete this task:

Implement shortest_path(graph, start, goal) using BFS and predecessors. Assume all neighbor names are keys. Raise ValueError for an unknown endpoint; return None if a known goal is unreachable. Preserve adjacency-list order for tied paths. Print paths from A to D and A to E in the graph below:

`{"A":["B","C"],"B":["D"],"C":["D"],"D":[],"E":[]}`.

Expected output:

```text
['A', 'B', 'D']
None
```
