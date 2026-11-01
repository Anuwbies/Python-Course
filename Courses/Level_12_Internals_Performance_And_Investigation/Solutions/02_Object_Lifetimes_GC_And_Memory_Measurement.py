import gc
import tracemalloc
import weakref

class Node:
    pass

node = Node()
node.link = node
observed = weakref.ref(node)
del node
gc.collect()
print(f"Cycle collected: {observed() is None}")
tracemalloc.start()
try:
    values = list(range(10000))
    current, peak = tracemalloc.get_traced_memory()
finally:
    tracemalloc.stop()
print(f"Values: {len(values)}")
print(f"Peak traced bytes: {peak}")
