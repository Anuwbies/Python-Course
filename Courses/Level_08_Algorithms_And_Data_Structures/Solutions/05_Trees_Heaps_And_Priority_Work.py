import heapq

def priority_order(jobs):
    heap = []
    for sequence, (priority, label) in enumerate(jobs):
        heapq.heappush(heap, (priority, sequence, label))
    result = []
    while heap:
        priority, sequence, label = heapq.heappop(heap)
        result.append(label)
    return result

print(priority_order([(2, "normal"), (1, "first"), (1, "second")]))
