class Account:
    def __init__(self, balance):
        if type(balance) is not int or balance < 0:
            raise ValueError("Invalid balance")
        self.balance = balance

    def withdraw(self, amount):
        if type(amount) is not int or amount <= 0 or amount > self.balance:
            raise ValueError("Invalid withdrawal")
        self.balance -= amount
        return self.balance

account = Account(100)
print(account.withdraw(30))
try:
    account.withdraw(80)
except ValueError:
    print("Rejected")
print(account.balance)
