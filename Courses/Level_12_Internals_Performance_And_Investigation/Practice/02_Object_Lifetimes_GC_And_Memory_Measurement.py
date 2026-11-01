# Independent task: object lifetimes, gc & memory measurement
#
# Create a weak-referenceable Node whose link refers to itself, remove the external strong
# reference, invoke gc.collect, and print whether the weak reference is cleared. Separately
# start tracemalloc, allocate list(range(10000)), obtain the observed peak, stop tracing in
# finally, and print the actual list length and peak bytes. Do not hardcode a memory size.

