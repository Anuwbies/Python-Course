class Budget:
    def __init__(self, amount):
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if type(value) is not int or value < 0:
            raise ValueError("Invalid amount")
        self._amount = value

    def __str__(self):
        return f"PHP {self.amount}"

budget = Budget(500)
print(budget)
try:
    budget.amount = -1
except ValueError:
    print("Rejected")
print(budget)
