from dataclasses import dataclass

@dataclass(frozen=True)
class Expense:
    category: str
    amount: int

    def __post_init__(self):
        if not isinstance(self.category, str) or not self.category.strip():
            raise ValueError("Invalid category")
        if type(self.amount) is not int or self.amount < 0:
            raise ValueError("Invalid amount")

expense = Expense("food", 120)
print(expense.category, expense.amount)
try:
    Expense("food", True)
except ValueError:
    print("Rejected")
