class Tracker:
    def __init__(self, owner):
        self.owner = owner
        self.amounts = []

first = Tracker("Mika")
second = Tracker("José")
first.amounts.append(10)
print(first.owner, first.amounts)
print(second.owner, second.amounts)
