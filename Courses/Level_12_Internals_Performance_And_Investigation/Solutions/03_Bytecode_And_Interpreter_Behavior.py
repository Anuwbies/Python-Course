import dis

def add(left, right):
    return left + right

print(f"Result: {add(2, 3)}")
print(f"Arguments: {add.__code__.co_argcount}")
print([instruction.opname for instruction in dis.get_instructions(add)])
