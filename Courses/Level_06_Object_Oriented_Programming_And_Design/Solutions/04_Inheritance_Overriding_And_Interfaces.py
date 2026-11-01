from abc import ABC, abstractmethod

class AmountReader(ABC):
    @abstractmethod
    def read(self):
        """Return a fresh list of amounts."""
        raise NotImplementedError

class MemoryReader(AmountReader):
    def __init__(self, values):
        self._values = values.copy()

    def read(self):
        return self._values.copy()

reader = MemoryReader([120, 80])
values = reader.read()
print(values)
print(sum(values))
