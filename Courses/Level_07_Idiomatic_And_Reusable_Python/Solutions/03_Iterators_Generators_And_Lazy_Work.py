def nonnegative_values(values):
    for value in values:
        if type(value) is not int or value < 0:
            raise ValueError("Invalid value")
        yield value

stream = nonnegative_values([0, 2, 5])
print(list(stream))
print(list(stream))
