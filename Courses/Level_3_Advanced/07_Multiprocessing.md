# Lesson 7: Multiprocessing for CPU-Bound Workloads

When you need true parallel execution across multiple CPU cores for heavy mathematical calculations, data transformation, or cryptography, `multiprocessing` bypasses the GIL by creating independent OS processes.

---

## 🎯 Learning Objectives
By the end of this lesson, you will:
1. Understand why separate OS processes bypass the Global Interpreter Lock.
2. Parallelize heavy CPU workloads using `concurrent.futures.ProcessPoolExecutor`.
3. Share data safely across processes using `Queue` and `Pipe`.
4. Prevent process spawning race conditions on Windows with `if __name__ == '__main__':`.

---

## 1. ProcessPoolExecutor vs Sequential

```python
import concurrent.futures
import time

def cpu_heavy_factorial_sum(n: int) -> int:
    """Simulates CPU-heavy mathematical computation."""
    return sum(i * i for i in range(n))

if __name__ == '__main__':
    numbers = [10_000_000, 10_000_000, 10_000_000, 10_000_000]

    # Parallel processing utilizing all CPU cores:
    start_time = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_heavy_factorial_sum, numbers))

    print(f"Parallel multiprocessing took: {time.perf_counter() - start_time:.2f}s")
```

> [!IMPORTANT]
> On Windows, multiprocessing scripts **must** wrap entry-point execution inside `if __name__ == '__main__':` to prevent endless recursive process spawns!

---

## 📝 Quick Exercise

**Prompt**:
Create a multiprocessing prime factorizer that parallelizes finding prime factors for an array of huge integers across 4 worker processes.

<details>
<summary><b>🔍 View Exercise Solution</b></summary>

```python
import concurrent.futures
import time

def get_prime_factors(n: int) -> list[int]:
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

if __name__ == '__main__':
    huge_numbers = [104729 * 104729, 999999999, 123456789012, 987654321098]
    
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        results = dict(zip(huge_numbers, executor.map(get_prime_factors, huge_numbers)))
        
    for num, factors in results.items():
        print(f"Factors of {num}: {factors}")
    print(f"Finished in {time.perf_counter() - start:.4f}s")
```
</details>
