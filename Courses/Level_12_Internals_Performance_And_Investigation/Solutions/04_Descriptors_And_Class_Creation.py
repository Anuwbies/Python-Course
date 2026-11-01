class Nonnegative:
    def __set_name__(self, owner, name):
        self.name = name
        self.storage = "_field_" + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        try:
            return instance.__dict__[self.storage]
        except KeyError:
            raise AttributeError(self.name) from None

    def __set__(self, instance, value):
        if type(value) is not int or value < 0:
            raise ValueError("Expected a nonnegative integer")
        instance.__dict__[self.storage] = value

class FieldMeta(type):
    def __new__(metaclass, name, bases, namespace):
        cls = super().__new__(metaclass, name, bases, namespace)
        cls.field_names = tuple(key for key, value in namespace.items() if isinstance(value, Nonnegative))
        return cls

class Account(metaclass=FieldMeta):
    balance = Nonnegative()
    def __init__(self, balance):
        self.balance = balance

print(Account.field_names)
account = Account(100)
print(account.balance)
try:
    account.balance = -1
except ValueError:
    print("Rejected")
print(account.balance)
