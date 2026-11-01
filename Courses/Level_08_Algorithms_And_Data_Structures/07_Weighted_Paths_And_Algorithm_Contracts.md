# Lesson 7: Weighted Paths & Algorithm Contracts

**Prerequisites:** Levels 1–7 and Lessons 1–6 of this level. **Practice file:** `Practice/07_Weighted_Paths_And_Algorithm_Contracts.py`.

Use a priority-driven search only under its required weight assumptions, and validate the graph separately from interpreting unreachable nodes.

## 1. Add costs to connections

A weighted adjacency list contains destination/weight pairs. A path's cost is the sum of its edge weights, which can differ from its edge count. BFS's first discovered route is therefore not necessarily cheapest.

Dijkstra's algorithm repeatedly processes the unsettled candidate with the smallest known distance. Its correctness depends on nonnegative edge weights. A negative edge can invalidate the reasoning that an already cheapest candidate will not later improve through a more expensive frontier.

## 2. Relax a candidate distance

Start the source distance at zero and others at infinity. For an edge from node to neighbor, compare current distance plus weight with the best known neighbor distance. An improvement updates the distance and adds a new heap candidate.

An older heap entry can become stale when a better route is found later. Ignore entries whose stored distance no longer equals the current best value. Trying to edit an arbitrary heap position in place is unnecessary for this implementation.

## 3. Validate the whole accepted graph

Reject negative weights even in a disconnected component if the public contract says the entire supplied graph must be valid. Validate neighbor names as well. Doing that up front costs O(E); include that cost when describing the public operation.

The task uses plain nonnegative integer weights, keeping equality and comparison exact. Floating-point weights introduce additional numeric considerations, and real routing systems need policies for missing or changing costs that this fixed graph does not model.

## 4. Report unreachable values honestly

Infinity represents no discovered route, not a very expensive actual route. Keep it distinct from a source distance of zero. A disconnected graph can be valid even though some destinations cannot be reached.

Check the algorithm on a graph where a cheap multi-edge path beats a direct edge. A demonstration with only one path cannot expose a failure to relax or ignore stale candidates. Compare a hand-derived small result before benchmarking a larger workload.

## Represent infinity and break heap ties safely

`from math import inf` supplies positive floating-point infinity. Every finite integer distance is smaller than inf; `distance == inf` checks the unreachable marker. Valid path sums remain integers in this task.

Node identifiers need not be sortable just because they are valid dictionary keys. Store heap entries as `(distance, sequence, node)` using a fresh increasing integer sequence for each insertion. Equal distances then compare sequences instead of attempting to order unrelated node objects. This is the same tie-breaking pattern taught for priority jobs. It preserves the cost rule without adding an accidental node-order requirement.

References: [Heap operations](https://docs.python.org/3.13/library/heapq.html).

## Cost model

This lazy-heap implementation can retain stale candidates: at most O(E) improving edge relaxations create entries. A general bound is O(V + E log E) time plus O(V + E) retained state, including validation and stale candidates, under bounded-cost IDs/weights. For a simple graph, the familiar O((V + E) log V) form follows from the relationship between V and E. State those graph assumptions instead of hiding heap duplicates.

## Practice: predict, explain, modify, debug

1. **Predict:** Find a cheaper indirect route than a direct edge by hand.
2. **Explain:** Explain why a stale heap entry can be ignored.
3. **Modify:** Add an unreachable node while keeping the graph valid.
4. **Debug:** Reject a negative edge rather than returning an apparently valid Dijkstra result.

<details>
<summary>Hints</summary>

Use a new heap entry for each improvement and ignore outdated distances.

</details>

## Independent task: weighted paths & algorithm contracts

In `Practice/07_Weighted_Paths_And_Algorithm_Contracts.py`, complete this task:

Implement shortest_distances(graph, start) with heapq and nonnegative plain-integer weights. The input is an adjacency dictionary with hashable node IDs and lists of (neighbor, weight) pairs; IDs need not be mutually sortable. Use (distance, sequence, node) heap entries to break equal-distance ties. Validate the source, neighbor keys, and all weight types/ranges, raising ValueError for invalid data. Return distances for every node, using infinity for unreachable nodes. For `A -> B:4,C:1`, `C -> B:2,D:5`, `B -> D:1`, and isolated E, print D's distance and whether E is infinity.

Expected output:

```text
4
True
```
