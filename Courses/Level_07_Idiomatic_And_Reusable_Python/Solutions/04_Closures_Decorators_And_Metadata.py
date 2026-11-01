from functools import wraps

def count_calls(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return function(*args, **kwargs)
    wrapper.calls = 0
    return wrapper

@count_calls
def add(left, right):
    return left + right

print(add(1, 2))
print(add(3, 4))
print(add.calls)
