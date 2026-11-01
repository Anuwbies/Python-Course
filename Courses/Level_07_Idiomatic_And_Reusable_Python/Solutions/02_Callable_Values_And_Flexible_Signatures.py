def transform_at_least(values, operation, *, minimum=0):
    return [operation(value) for value in values if value >= minimum]

def double(value):
    return value * 2

values = [-1, 0, 2]
print(transform_at_least(values, double, minimum=0))
print(values)
