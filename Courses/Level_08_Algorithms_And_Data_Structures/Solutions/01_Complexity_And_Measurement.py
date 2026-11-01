def linear_search(values, target):
    comparisons = 0
    for value in values:
        comparisons += 1
        if value == target:
            return True, comparisons
    return False, comparisons

values = [0, 1, 2, 3, 4]
print(linear_search(values, 4))
print(linear_search(values, 9))
