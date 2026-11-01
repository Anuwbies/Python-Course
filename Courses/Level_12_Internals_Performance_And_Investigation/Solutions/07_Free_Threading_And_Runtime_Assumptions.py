import sys
import sysconfig
from threading import Lock, Thread

probe = getattr(sys, "_is_gil_enabled", None)
print(f"Implementation: {sys.implementation.name}")
print(f"GIL enabled: {probe() if probe is not None else None}")
print(f"Free-threaded build flag: {sysconfig.get_config_var('Py_GIL_DISABLED')}")
class Counter:
    def __init__(self):
        self.value = 0
        self.lock = Lock()

    def increment(self):
        with self.lock:
            self.value += 1

def work(counter):
    for _ in range(1000):
        counter.increment()

counter = Counter()
threads = [Thread(target=work, args=(counter,)) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(f"Count: {counter.value}")
