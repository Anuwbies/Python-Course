import heapq
from math import inf

def shortest_distances(graph, start):
    if start not in graph:
        raise ValueError("Unknown source")
    for edges in graph.values():
        for neighbor, weight in edges:
            if neighbor not in graph or type(weight) is not int or weight < 0:
                raise ValueError("Invalid edge")
    distances = {node: inf for node in graph}
    distances[start] = 0
    sequence = 0
    heap = [(0, sequence, start)]
    while heap:
        distance, _, node = heapq.heappop(heap)
        if distance != distances[node]:
            continue
        for neighbor, weight in graph[node]:
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                sequence += 1
                heapq.heappush(heap, (candidate, sequence, neighbor))
    return distances

graph = {"A": [("B", 4), ("C", 1)], "B": [("D", 1)],
         "C": [("B", 2), ("D", 5)], "D": [], "E": []}
result = shortest_distances(graph, "A")
print(result["D"])
print(result["E"] == inf)
