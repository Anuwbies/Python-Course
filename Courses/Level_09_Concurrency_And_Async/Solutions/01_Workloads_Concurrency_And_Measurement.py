from time import perf_counter_ns

def measure(operation):
    start = perf_counter_ns()
    result = operation()
    return result, perf_counter_ns() - start

result, elapsed = measure(lambda: sum(range(1000)))
print(f"Result: {result}")
print(f"Nonnegative duration: {elapsed >= 0}")
