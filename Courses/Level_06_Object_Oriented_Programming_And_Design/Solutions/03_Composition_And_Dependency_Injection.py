class MemoryStore:
    def __init__(self):
        self._values = []

    def save(self, values):
        self._values = values.copy()

    def load(self):
        return self._values.copy()

class ExpenseService:
    def __init__(self, store):
        self._store = store

    def total(self):
        return sum(self._store.load())

store = MemoryStore()
store.save([120, 80])
service = ExpenseService(store)
print(service.total())
loaded = store.load()
loaded.append(999)
print(service.total())
