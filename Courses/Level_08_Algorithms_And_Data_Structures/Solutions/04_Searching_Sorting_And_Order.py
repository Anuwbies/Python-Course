def leftmost_index(values, target):
    low = 0
    high = len(values)
    while low < high:
        middle = (low + high) // 2
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle
    if low < len(values) and values[low] == target:
        return low
    return -1

values = [1, 3, 5, 5, 8]
print(leftmost_index(values, 5))
print(leftmost_index(values, 4))
