# Independent task: weighted paths & algorithm contracts
#
# Implement shortest_distances(graph, start) with heapq and nonnegative plain-integer weights.
# The input is an adjacency dictionary with hashable node IDs and lists of (neighbor, weight)
# pairs; IDs need not be mutually sortable. Use (distance, sequence, node) heap entries to break
# equal-distance ties. Validate the source, neighbor keys, and all weight types/ranges, raising
# ValueError for invalid data. Return distances for every node, using infinity for unreachable
# nodes. For A -> B:4,C:1, C -> B:2,D:5, B -> D:1, and isolated E, print D's distance and
# whether E is infinity.
#
# Expected output:
#
# 4
# True

