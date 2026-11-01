def factorial(number):
    if type(number) is not int or number < 0:
        raise ValueError("Expected a nonnegative integer")
    if number == 0:
        return 1
    return number * factorial(number - 1)

print(factorial(5))
print(factorial(0))
try:
    factorial(-1)
except ValueError:
    print("Rejected")
