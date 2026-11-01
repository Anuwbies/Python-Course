from threading import Lock, Thread

class Counter:
    def __init__(self):
        self.value = 0
        self._lock = Lock()

    def increment(self):
        with self._lock:
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
print(counter.value)
