original = [120, 80]
updated = original.copy()
updated.append(50)
total = 0
for amount in updated:
    total = total + amount
print(original)
print(updated)
print(total)
